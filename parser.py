# -*- coding: utf-8 -*-
"""Massachusetts general-election precinct results from electionstats.state.ma.us.

Usage:
    python parser.py 2024 20241105
    python parser.py 2022 20221108 --cache .cache

Writes <year>/<date>__ma__general__precinct.csv with the columns
town, ward, precinct, office, district, party, candidate, votes
and prints a validation report.

For every office it searches electionstats for that year's general elections, downloads
each election's precinct CSV, and writes one row per precinct per candidate column
(including All Others, Blanks and Total Votes Cast).

Notes:
* The electionstats TOTALS line is not written as a row. It is used as a checksum: for each
  election the precinct rows are summed and compared with TOTALS, and any mismatch is reported.
* Special elections are skipped (the "stage: General" search also returns specials).
* Party comes from the party line under each candidate in the downloaded CSV, except that
  candidates the search results list as write-ins get "(Write-In)", as in earlier files.
* Towns without wards ("-") get an empty ward; single-precinct towns get precinct "1".
* After redistricting, electionstats sometimes prints a precinct that sits in a different
  district from the rest of its town as "Town,," with no ward or precinct. The label is
  recovered when exactly one precinct of that town is missing from that office and has the same
  ballot total in the top-of-ticket race (President or Governor). Anything else is left blank
  and reported.
"""
import argparse
import csv
import io
import os
import time

import requests
from bs4 import BeautifulSoup

BASE = "https://electionstats.state.ma.us"
OFFICES = [  # (electionstats office_id, office name, has district)
    (1, "President", False), (6, "U.S. Senate", False), (3, "Governor", False),
    (45, "Secretary", False), (53, "Treasurer", False), (90, "Auditor", False),
    (12, "Attorney General", False), (529, "Governor's Council", True),
    (5, "U.S. House", True), (9, "State Senate", True), (8, "State House", True),
]


def num(x):
    x = (x or "").replace(",", "").strip()
    return int(x) if x not in ("", "-") else None


def elections(session, year, office_id):
    """(election id, district, write-in names) for each non-special general election of this office."""
    url = f"{BASE}/elections/search/year_from:{year}/year_to:{year}/office_id:{office_id}/stage:General"
    soup = BeautifulSoup(session.get(url, timeout=60).text, "html.parser")
    table = soup.find("table", id="search_results_table")
    out = []
    for tr in (table.find_all("tr") if table else []):
        rid = tr.get("id") or ""
        if not rid.startswith("election-id-"):
            continue
        if "special" in tr.get_text(" ", strip=True).lower():
            continue
        tds = tr.find_all("td")
        writeins = set()
        for td in tr.find_all("td", {"class": "candidate"}):
            a, party = td.find("a"), td.find("div", {"class": "party"})
            if a and party and "write-in" in party.get_text().lower():
                writeins.add(a.get_text().strip())
        out.append((rid.split("-")[-1], tds[2].get_text(" ", strip=True).replace(" Congressional", ""), writeins))
    return out


def download(session, eid, cache):
    path = os.path.join(cache, f"{eid}.csv") if cache else None
    if path and os.path.exists(path):
        with open(path, encoding="utf-8-sig") as fh:
            return fh.read()
    r = session.get(f"{BASE}/elections/download/{eid}/precincts_include:1/", timeout=120)
    r.raise_for_status()
    time.sleep(0.3)
    if path:
        with open(path, "wb") as fh:
            fh.write(r.content)
    return r.content.decode("utf-8-sig")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("year")
    ap.add_argument("date", help="election date as YYYYMMDD, used in the output file name")
    ap.add_argument("--cache", help="directory to cache downloaded electionstats CSVs")
    args = ap.parse_args()
    cache = os.path.join(args.cache, args.year) if args.cache else None
    if cache:
        os.makedirs(cache, exist_ok=True)

    session = requests.Session()
    rows, problems, n_el = [], [], 0
    for office_id, office, has_district in OFFICES:
        for eid, district, writeins in elections(session, args.year, office_id):
            n_el += 1
            lines = list(csv.reader(io.StringIO(download(session, eid, cache))))
            header, parties, body = lines[0], lines[1], lines[2:]
            cands = header[3:]
            party_of = {c: (parties[3 + i].strip() if 3 + i < len(parties) else "") for i, c in enumerate(cands)}
            for c in cands:   # write-in candidates are labelled "(Write-In)", as in earlier files
                if c.strip() in writeins:
                    party_of[c] = "(Write-In)"
            sums = {c: 0 for c in cands}
            totals = None
            for r in body:
                if not r or not r[0].strip():
                    continue
                town, ward, pct = r[0].strip(), r[1].strip(), r[2].strip()
                vals = {c: num(r[3 + i]) if 3 + i < len(r) else None for i, c in enumerate(cands)}
                if town.upper() == "TOTALS":
                    totals = vals
                    continue
                for c in cands:
                    sums[c] += vals[c] or 0
                    rows.append([town, "" if ward == "-" else ward, pct, office, district if has_district else "",
                                 party_of[c], c.replace("/", " and"), vals[c]])
            if totals is None:
                problems.append(f"  {office} {district} (election {eid}): no TOTALS line")
            else:
                for c in cands:
                    if (totals[c] or 0) != sums[c]:
                        problems.append(f"  {office} {district} (election {eid}) {c}: "
                                        f"precincts {sums[c]:,} vs TOTALS {totals[c] or 0:,}")

    # Recover precinct labels printed as "Town,," (see module docstring).
    top = "President" if any(r[3] == "President" for r in rows) else "Governor"
    top_total = {(r[0], r[1], r[2]): r[7] for r in rows if r[3] == top and r[6] == "Total Votes Cast"}
    fixes, unresolved = [], []
    for office in sorted({r[3] for r in rows if r[3] != top}):
        off_rows = [r for r in rows if r[3] == office]
        labelled = {(r[0], r[1], r[2]) for r in off_rows if r[2]}
        blanks = {(r[0], r[4]): r[7] for r in off_rows if not r[2] and r[6] == "Total Votes Cast"
                  and (r[0], "", "") not in top_total}
        for (town, dist), tot in blanks.items():
            matches = [k for k, v in top_total.items() if k[0] == town and k not in labelled and v == tot]
            if len(matches) == 1:
                _, ward, pct = matches[0]
                for r in off_rows:
                    if r[0] == town and r[4] == dist and not r[2]:
                        r[1], r[2] = ward, pct
                labelled.add(matches[0])
                fixes.append(f"  {office} {dist}: {town} -> ward '{ward}' precinct {pct} ({tot:,} ballots)")
            else:
                unresolved.append(f"  {office} {dist}: {town} left blank ({len(matches)} candidates, {tot:,} ballots)")

    # Single-precinct towns: electionstats leaves Pct blank; earlier files use "1".
    single = {k[0] for k in top_total if k[1] == "" and k[2] == ""}
    for r in rows:
        if r[0] in single and r[1] == "" and r[2] == "":
            r[2] = "1"

    os.makedirs(args.year, exist_ok=True)
    out = os.path.join(args.year, f"{args.date}__ma__general__precinct.csv")
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["town", "ward", "precinct", "office", "district", "party", "candidate", "votes"])
        w.writerows(rows)

    print(f"{n_el} elections, {len(rows):,} rows -> {out}")
    print(f"Precinct sums vs. TOTALS: {len(problems)} mismatches")
    print("\n".join(problems))
    print(f"Precinct labels recovered: {len(fixes)}; left blank: {len(unresolved)}")
    print("\n".join(fixes + unresolved))


if __name__ == "__main__":
    main()
