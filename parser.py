 # -*- coding: utf-8 -*-

import unicodecsv as csv
import requests
from BeautifulSoup import BeautifulSoup

def parse_president():
    url = "http://electionstats.state.ma.us/elections/search/year_from:2016/year_to:2016/office_id:1/stage:General/show_details:1"
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    president_candidates = []
    election_links = []
    districts = {}
    table = soup.find('table', id="search_results_table")
    for row in table.findAll('tr')[1:]:
        election_link = next((x for x in row.findAll('a') if "/elections/view/" in x['href']), None)
        if election_link:
            download_url = "http://electionstats.state.ma.us/elections/download/%s/precincts_include:1/" % election_link['href'].split('/')[3]
            election_links.append(download_url)
            try:
                district = row.findAll('td')[2].text
            except:
                districts[download_url] = district
        if row.text != '':
            president_candidates.append([{x.find('a').text : x.find('div', {'class': 'party'}).text} for x in row.findAll('td', {'class' : "candidate"}) if x.find('a') and x.find('a').text != ''])

    final_cands = {}
    final_cands['All Others'] = None
    final_cands['Blank Votes'] = None
    final_cands['No Preference'] = None
    final_cands['Total Votes Cast'] = None
    for cand in president_candidates:
        if cand != []:
            final_cands[cand[0].keys()[0]] = cand[0][cand[0].keys()[0]]

    with requests.Session() as s:
        for link in election_links:
            download = s.get(link)
            decoded_content = download.content.decode('utf-8')
            reader = csv.DictReader(decoded_content.splitlines(), delimiter=',')
            for row in reader:
                cols = [x for x in row.keys() if x not in ['City/Town', 'Ward', 'Pct']]
                for col in cols:
                    party = final_cands[col.replace('/', ' and')]
                    results.append([row['City/Town'], row['Ward'], row['Pct'], 'President', None, party, col.replace('/', ' and'), int(row[col].replace(',',''))])

def parse_governor():
    url = "http://electionstats.state.ma.us/elections/search/year_from:2010/year_to:2010/office_id:3/stage:General/show_details:1"
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    president_candidates = []
    election_links = []
    districts = {}
    table = soup.find('table', id="search_results_table")
    for row in table.findAll('tr')[1:]:
        election_link = next((x for x in row.findAll('a') if "/elections/view/" in x['href']), None)
        if election_link:
            download_url = "http://electionstats.state.ma.us/elections/download/%s/precincts_include:1/" % election_link['href'].split('/')[3]
            election_links.append(download_url)
            try:
                district = row.findAll('td')[2].text
            except:
                districts[download_url] = district
        if row.text != '':
            president_candidates.append([{x.find('a').text : x.find('div', {'class': 'party'}).text} for x in row.findAll('td', {'class' : "candidate"}) if x.find('a') and x.find('a').text != ''])

    final_cands = {}
    final_cands['All Others'] = None
    final_cands['Blank Votes'] = None
    final_cands['No Preference'] = None
    final_cands['Total Votes Cast'] = None
    for cand in president_candidates:
        if cand != []:
            final_cands[cand[0].keys()[0]] = cand[0][cand[0].keys()[0]]

    with requests.Session() as s:
        for link in election_links:
            download = s.get(link)
            decoded_content = download.content.decode('utf-8')
            reader = csv.DictReader(decoded_content.splitlines(), delimiter=',')
            for row in reader:
                cols = [x for x in row.keys() if x not in ['City/Town', 'Ward', 'Pct']]
                for col in cols:
                    party = final_cands[col.replace('/', ' and')]
                    results.append([row['City/Town'], row['Ward'], row['Pct'], 'Governor', None, party, col.replace('/', ' and'), int(row[col].replace(',',''))])

def parse_us_senate():
    url = "http://electionstats.state.ma.us/elections/search/year_from:2010/year_to:2010/office_id:6/stage:General"
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    state_house_candidates = []
    election_links = []
    districts = {}
    table = soup.find('table', id="search_results_table")
    for row in table.findAll('tr')[1:]:
        election_link = next((x for x in row.findAll('a') if "/elections/view/" in x['href']), None)
        if election_link:
            download_url = "http://electionstats.state.ma.us/elections/download/%s/precincts_include:1/" % election_link['href'].split('/')[3]
            election_links.append(download_url)
        if row.text != '':
            state_house_candidates.append([{x.find('a').text : x.find('div', {'class': 'party'}).text} for x in row.findAll('td', {'class' : "candidate"}) if x.find('a') and x.find('a').text != ''])

    final_cands = {}
    final_cands['All Others'] = None
    final_cands['Blank Votes'] = None
    final_cands['Total Votes Cast'] = None
    for cand in state_house_candidates:
        if cand != []:
            final_cands[cand[0].keys()[0]] = cand[0][cand[0].keys()[0]]

    with requests.Session() as s:
        for link in election_links:
            download = s.get(link)
            decoded_content = download.content.decode('utf-8')
            reader = csv.DictReader(decoded_content.splitlines(), delimiter=',')
            for row in reader:
                cols = [x for x in row.keys() if x not in ['City/Town', 'Ward', 'Pct']]
                for col in cols:
                    party = final_cands[col]
                    results.append([row['City/Town'], row['Ward'], row['Pct'], 'U.S. Senate', None, party, col, int(row[col].replace(',',''))])

def parse_secretary():
    url = "http://electionstats.state.ma.us/elections/search/year_from:2010/year_to:2010/office_id:45/stage:General"
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    state_house_candidates = []
    election_links = []
    districts = {}
    table = soup.find('table', id="search_results_table")
    for row in table.findAll('tr')[1:]:
        election_link = next((x for x in row.findAll('a') if "/elections/view/" in x['href']), None)
        if election_link:
            download_url = "http://electionstats.state.ma.us/elections/download/%s/precincts_include:1/" % election_link['href'].split('/')[3]
            election_links.append(download_url)
        if row.text != '':
            state_house_candidates.append([{x.find('a').text : x.find('div', {'class': 'party'}).text} for x in row.findAll('td', {'class' : "candidate"}) if x.find('a') and x.find('a').text != ''])

    final_cands = {}
    final_cands['All Others'] = None
    final_cands['Blank Votes'] = None
    final_cands['Total Votes Cast'] = None
    for cand in state_house_candidates:
        if cand != []:
            final_cands[cand[0].keys()[0]] = cand[0][cand[0].keys()[0]]

    with requests.Session() as s:
        for link in election_links:
            download = s.get(link)
            decoded_content = download.content.decode('utf-8')
            reader = csv.DictReader(decoded_content.splitlines(), delimiter=',')
            for row in reader:
                cols = [x for x in row.keys() if x not in ['City/Town', 'Ward', 'Pct']]
                for col in cols:
                    party = final_cands[col]
                    results.append([row['City/Town'], row['Ward'], row['Pct'], 'Secretary', None, party, col, int(row[col].replace(',',''))])

def parse_treasurer():
    url = "http://electionstats.state.ma.us/elections/search/year_from:2010/year_to:2010/office_id:53/stage:General"
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    state_house_candidates = []
    election_links = []
    districts = {}
    table = soup.find('table', id="search_results_table")
    for row in table.findAll('tr')[1:]:
        election_link = next((x for x in row.findAll('a') if "/elections/view/" in x['href']), None)
        if election_link:
            download_url = "http://electionstats.state.ma.us/elections/download/%s/precincts_include:1/" % election_link['href'].split('/')[3]
            election_links.append(download_url)
        if row.text != '':
            state_house_candidates.append([{x.find('a').text : x.find('div', {'class': 'party'}).text} for x in row.findAll('td', {'class' : "candidate"}) if x.find('a') and x.find('a').text != ''])

    final_cands = {}
    final_cands['All Others'] = None
    final_cands['Blank Votes'] = None
    final_cands['Total Votes Cast'] = None
    for cand in state_house_candidates:
        if cand != []:
            final_cands[cand[0].keys()[0]] = cand[0][cand[0].keys()[0]]

    with requests.Session() as s:
        for link in election_links:
            download = s.get(link)
            decoded_content = download.content.decode('utf-8')
            reader = csv.DictReader(decoded_content.splitlines(), delimiter=',')
            for row in reader:
                cols = [x for x in row.keys() if x not in ['City/Town', 'Ward', 'Pct']]
                for col in cols:
                    party = final_cands[col]
                    results.append([row['City/Town'], row['Ward'], row['Pct'], 'Treasurer', None, party, col, int(row[col].replace(',',''))])

def parse_auditor():
    url = "http://electionstats.state.ma.us/elections/search/year_from:2010/year_to:2010/office_id:90/stage:General"
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    state_house_candidates = []
    election_links = []
    districts = {}
    table = soup.find('table', id="search_results_table")
    for row in table.findAll('tr')[1:]:
        election_link = next((x for x in row.findAll('a') if "/elections/view/" in x['href']), None)
        if election_link:
            download_url = "http://electionstats.state.ma.us/elections/download/%s/precincts_include:1/" % election_link['href'].split('/')[3]
            election_links.append(download_url)
        if row.text != '':
            state_house_candidates.append([{x.find('a').text : x.find('div', {'class': 'party'}).text} for x in row.findAll('td', {'class' : "candidate"}) if x.find('a') and x.find('a').text != ''])

    final_cands = {}
    final_cands['All Others'] = None
    final_cands['Blank Votes'] = None
    final_cands['Total Votes Cast'] = None
    for cand in state_house_candidates:
        if cand != []:
            final_cands[cand[0].keys()[0]] = cand[0][cand[0].keys()[0]]

    with requests.Session() as s:
        for link in election_links:
            download = s.get(link)
            decoded_content = download.content.decode('utf-8')
            reader = csv.DictReader(decoded_content.splitlines(), delimiter=',')
            for row in reader:
                cols = [x for x in row.keys() if x not in ['City/Town', 'Ward', 'Pct']]
                for col in cols:
                    party = final_cands[col]
                    results.append([row['City/Town'], row['Ward'], row['Pct'], 'Auditor', None, party, col, int(row[col].replace(',',''))])

def parse_attorney_general():
    url = "http://electionstats.state.ma.us/elections/search/year_from:2010/year_to:2010/office_id:12/stage:General"
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    state_house_candidates = []
    election_links = []
    districts = {}
    table = soup.find('table', id="search_results_table")
    for row in table.findAll('tr')[1:]:
        election_link = next((x for x in row.findAll('a') if "/elections/view/" in x['href']), None)
        if election_link:
            download_url = "http://electionstats.state.ma.us/elections/download/%s/precincts_include:1/" % election_link['href'].split('/')[3]
            election_links.append(download_url)
        if row.text != '':
            state_house_candidates.append([{x.find('a').text : x.find('div', {'class': 'party'}).text} for x in row.findAll('td', {'class' : "candidate"}) if x.find('a') and x.find('a').text != ''])

    final_cands = {}
    final_cands['All Others'] = None
    final_cands['Blank Votes'] = None
    final_cands['Total Votes Cast'] = None
    for cand in state_house_candidates:
        if cand != []:
            final_cands[cand[0].keys()[0]] = cand[0][cand[0].keys()[0]]

    with requests.Session() as s:
        for link in election_links:
            download = s.get(link)
            decoded_content = download.content.decode('utf-8')
            reader = csv.DictReader(decoded_content.splitlines(), delimiter=',')
            for row in reader:
                cols = [x for x in row.keys() if x not in ['City/Town', 'Ward', 'Pct']]
                for col in cols:
                    party = final_cands[col]
                    results.append([row['City/Town'], row['Ward'], row['Pct'], 'Attorney General', None, party, col, int(row[col].replace(',',''))])

def parse_council():
    url = "http://electionstats.state.ma.us/elections/search/year_from:2010/year_to:2010/office_id:529/stage:General"
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    state_house_candidates = []
    election_links = []
    districts = {}
    table = soup.find('table', id="search_results_table")
    for row in table.findAll('tr')[1:]:
        election_link = next((x for x in row.findAll('a') if "/elections/view/" in x['href']), None)
        if election_link:
            download_url = "http://electionstats.state.ma.us/elections/download/%s/precincts_include:1/" % election_link['href'].split('/')[3]
            election_links.append(download_url)
            try:
                district = row.findAll('td')[2].text.replace(' Congressional','')
            except:
                districts[download_url] = district
        if row.text != '':
            state_house_candidates.append([{x.find('a').text : x.find('div', {'class': 'party'}).text} for x in row.findAll('td', {'class' : "candidate"}) if x.find('a') and x.find('a').text != ''])

    final_cands = {}
    final_cands['All Others'] = None
    final_cands['Blank Votes'] = None
    final_cands['Total Votes Cast'] = None
    for cand in state_house_candidates:
        if cand != []:
            final_cands[cand[0].keys()[0]] = cand[0][cand[0].keys()[0]]

    with requests.Session() as s:
        for link in election_links:
            download = s.get(link)
            district = districts[link]
            decoded_content = download.content.decode('utf-8')
            reader = csv.DictReader(decoded_content.splitlines(), delimiter=',')
            for row in reader:
                cols = [x for x in row.keys() if x not in ['City/Town', 'Ward', 'Pct']]
                for col in cols:
                    party = final_cands[col]
                    results.append([row['City/Town'], row['Ward'], row['Pct'], "Governor's Council", district, party, col, int(row[col].replace(',',''))])


def parse_us_house():
    url = "http://electionstats.state.ma.us/elections/search/year_from:2010/year_to:2010/office_id:5/stage:General"
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    state_house_candidates = []
    election_links = []
    districts = {}
    table = soup.find('table', id="search_results_table")
    for row in table.findAll('tr')[1:]:
        election_link = next((x for x in row.findAll('a') if "/elections/view/" in x['href']), None)
        if election_link:
            download_url = "http://electionstats.state.ma.us/elections/download/%s/precincts_include:1/" % election_link['href'].split('/')[3]
            election_links.append(download_url)
            try:
                district = row.findAll('td')[2].text.replace(' Congressional','')
            except:
                districts[download_url] = district
        if row.text != '':
            state_house_candidates.append([{x.find('a').text : x.find('div', {'class': 'party'}).text} for x in row.findAll('td', {'class' : "candidate"}) if x.find('a') and x.find('a').text != ''])

    final_cands = {}
    final_cands['All Others'] = None
    final_cands['Blank Votes'] = None
    final_cands['Total Votes Cast'] = None
    for cand in state_house_candidates:
        if cand != []:
            final_cands[cand[0].keys()[0]] = cand[0][cand[0].keys()[0]]

    with requests.Session() as s:
        for link in election_links:
            download = s.get(link)
            district = districts[link]
            decoded_content = download.content.decode('utf-8')
            reader = csv.DictReader(decoded_content.splitlines(), delimiter=',')
            for row in reader:
                cols = [x for x in row.keys() if x not in ['City/Town', 'Ward', 'Pct']]
                for col in cols:
                    party = final_cands[col]
                    results.append([row['City/Town'], row['Ward'], row['Pct'], 'U.S. House', district, party, col, int(row[col].replace(',',''))])

def parse_state_senate():
    url = "http://electionstats.state.ma.us/elections/search/year_from:2010/year_to:2010/office_id:9/stage:General"
    r = requests.get(url)
    soup = BeautifulSoup(r.text.encode('utf-8'))
    state_senate_candidates = []
    election_links = []
    districts = {}
    table = soup.find('table', id="search_results_table")
    for row in table.findAll('tr')[1:]:
        election_link = next((x for x in row.findAll('a') if "/elections/view/" in x['href']), None)
        if election_link:
            download_url = "http://electionstats.state.ma.us/elections/download/%s/precincts_include:1/" % election_link['href'].split('/')[3]
            election_links.append(download_url)
            try:
                district = row.findAll('td')[2].text
            except:
                districts[download_url] = district
        if row.text != '':
            state_senate_candidates.append([{x.find('a').text : x.find('div', {'class': 'party'}).text} for x in row.findAll('td', {'class' : "candidate"}) if x.find('a') and x.find('a').text != ''])

    final_cands = {}
    final_cands['All Others'] = None
    final_cands['Blank Votes'] = None
    final_cands['Total Votes Cast'] = None
    for cand in state_senate_candidates:
        if cand != []:
            final_cands[cand[0].keys()[0]] = cand[0][cand[0].keys()[0]]

    with requests.Session() as s:
        for link in election_links:
            download = s.get(link)
            district = districts[link]
            decoded_content = download.content
            reader = csv.DictReader(decoded_content.splitlines(), delimiter=',', encoding='utf-8')
            for row in reader:
                cols = [x for x in row.keys() if x not in ['City/Town', 'Ward', 'Pct']]
                for col in cols:
                    if col == u'Sonia Rosa Chang-D\xcdaz' or col == u'Sonia Rosa Chang-D?az':
                        party = 'Democratic'
                    else:
                        party = final_cands[col]
                    results.append([row['City/Town'], row['Ward'], row['Pct'], 'State Senate', district, party, col, int(row[col].replace(',',''))])


def parse_state_house():
    url = "http://electionstats.state.ma.us/elections/search/year_from:2010/year_to:2010/office_id:8/stage:General"
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    state_house_candidates = []
    election_links = []
    districts = {}
    table = soup.find('table', id="search_results_table")
    for row in table.findAll('tr')[1:]:
        election_link = next((x for x in row.findAll('a') if "/elections/view/" in x['href']), None)
        if election_link:
            download_url = "http://electionstats.state.ma.us/elections/download/%s/precincts_include:1/" % election_link['href'].split('/')[3]
            election_links.append(download_url)
            try:
                district = row.findAll('td')[2].text
            except:
                districts[download_url] = district
        if row.text != '':
            state_house_candidates.append([{x.find('a').text : x.find('div', {'class': 'party'}).text} for x in row.findAll('td', {'class' : "candidate"}) if x.find('a') and x.find('a').text != ''])

    final_cands = {}
    final_cands['All Others'] = None
    final_cands['Blank Votes'] = None
    final_cands['Total Votes Cast'] = None
    for cand in state_house_candidates:
        if cand != []:
            final_cands[cand[0].keys()[0]] = cand[0][cand[0].keys()[0]]

    final_cands['Antonio d. F. Cabral'] = 'Democratic'

    with requests.Session() as s:
        for link in election_links:
            download = s.get(link)
            district = districts[link]
            decoded_content = download.content.decode('utf-8')
            reader = csv.DictReader(decoded_content.splitlines(), delimiter=',')
            for row in reader:
                cols = [x for x in row.keys() if x not in ['City/Town', 'Ward', 'Pct']]
                for col in cols:
                    party = final_cands[col]
                    results.append([row['City/Town'], row['Ward'], row['Pct'], 'State House', district, party, col, int(row[col].replace(',',''))])

if __name__ == "__main__":
    results = []
#    parse_president()
    parse_us_senate()
    parse_governor()
    parse_secretary()
    parse_treasurer()
    parse_auditor()
    parse_attorney_general()
    parse_council()
    parse_us_house()
    parse_state_senate()
    parse_state_house()
    results = [list(x) for x in set(tuple(x) for x in results)]
    with open('2010/20101102__ma__general__precinct.csv','wb') as csvfile:
        csvwriter = csv.writer(csvfile, encoding='utf-8')
        csvwriter.writerow(['town', 'ward', 'precinct', 'office', 'district', 'party', 'candidate', 'votes'])
        csvwriter.writerows(results)
