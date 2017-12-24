 # -*- coding: utf-8 -*-

import csv
import requests
from BeautifulSoup import BeautifulSoup

results = []

state_senate_districts = [
    "Berkshire, Hampshire and Franklin",
    "Bristol and Norfolk",
    "1st Bristol and Plymouth",
    "2nd Bristol and Plymouth",
    "Cape and Islands",
    "1st Essex",
    "2nd Essex",
    "3rd Essex",
    "1st Essex and Middlesex",
    "2nd Essex and Middlesex",
    "Hampden",
    "1st Hampden and Hampshire",
    "2nd Hampden and Hampshire",
    "Hampshire, Franklin and Worcester",
    "1st Middlesex",
    "2nd Middlesex",
    "3rd Middlesex",
    "4th Middlesex",
    "5th Middlesex",
    "1st Middlesex and Norfolk",
    "2nd Middlesex and Norfolk",
    "Middlesex and Worcester",
    "Middlesex and Suffolk",
    "Norfolk, Bristol and Middlesex",
    "Norfolk, Bristol and Plymouth",
    "Norfolk and Plymouth",
    "Norfolk and Suffolk",
    "Plymouth and Barnstable",
    "Plymouth and Norfolk",
    "Plymouth and Norfolk",
    "1st Plymouth and Bristol",
    "2nd Plymouth and Bristol",
    "1st Suffolk",
    "2nd Suffolk",
    "1st Suffolk and Middlesex",
    "1st Suffolk and Middlesex",
    "2nd Suffolk and Middlesex",
    "Worcester and Middlesex",
    "Worcester and Norfolk",
    "Worcester, Hampden, Hampshire and Middlesex",
    "1st Worcester",
    "2nd Worcester"
]

state_house_districts = [
    "1st Barnstable",
    "2nd Barnstable",
    "3rd Barnstable",
    "4th Barnstable",
    "5th Barnstable",
    "Barnstable, Dukes and Nantucket",
    "1st Berkshire",
    "2nd Berkshire",
    "3rd Berkshire",
    "4th Berkshire",
    "1st Bristol",
    "2nd Bristol",
    "3rd Bristol",
    "4th Bristol",
    "5th Bristol",
    "6th Bristol",
    "7th Bristol",
    "8th Bristol",
    "9th Bristol",
    "10th Bristol",
    "11th Bristol",
    "12th Bristol",
    "13th Bristol",
    "14th Bristol",
    "1st Essex",
    "2nd Essex",
    "3rd Essex",
    "4th Essex",
    "5th Essex",
    "6th Essex",
    "7th Essex",
    "8th Essex",
    "9th Essex",
    "10th Essex",
    "10th Essex",
    "11th Essex",
    "12th Essex",
    "12th Essex",
    "13th Essex",
    "14th Essex",
    "15th Essex",
    "16th Essex",
    "17th Essex",
    "18th Essex",
    "1st Franklin",
    "2nd Franklin",
    "1st Hampden",
    "2nd Hampden",
    "3rd Hampden",
    "4th Hampden",
    "5th Hampden",
    "6th Hampden",
    "7th Hampden",
    "8th Hampden",
    "9th Hampden",
    "10th Hampden",
    "11th Hampden",
    "12th Hampden",
    "1st Hampshire",
    "2nd Hampshire",
    "3rd Hampshire",
    "1st Middlesex",
    "2nd Middlesex",
    "3rd Middlesex",
    "4th Middlesex",
    "5th Middlesex",
    "6th Middlesex",
    "7th Middlesex",
    "8th Middlesex",
    "9th Middlesex",
    "10th Middlesex",
    "11th Middlesex",
    "12th Middlesex",
    "13th Middlesex",
    "14th Middlesex",
    "15th Middlesex",
    "16th Middlesex",
    "17th Middlesex",
    "18th Middlesex",
    "19th Middlesex",
    "20th Middlesex",
    "21st Middlesex",
    "22nd Middlesex",
    "23rd Middlesex",
    "24th Middlesex",
    "25th Middlesex",
    "26th Middlesex",
    "27th Middlesex",
    "28th Middlesex",
    "29th Middlesex",
    "30th Middlesex",
    "31st Middlesex",
    "32nd Middlesex",
    "33rd Middlesex",
    "34th Middlesex",
    "35th Middlesex",
    "36th Middlesex",
    "37th Middlesex",
    "1st Norfolk",
    "2nd Norfolk",
    "3rd Norfolk",
    "4th Norfolk",
    "5th Norfolk",
    "6th Norfolk",
    "7th Norfolk",
    "8th Norfolk",
    "9th Norfolk",
    "10th Norfolk",
    "11th Norfolk",
    "12th Norfolk",
    "13th Norfolk",
    "14th Norfolk",
    "15th Norfolk",
    "1st Plymouth",
    "2nd Plymouth",
    "3rd Plymouth",
    "4th Plymouth",
    "5th Plymouth",
    "6th Plymouth",
    "7th Plymouth",
    "8th Plymouth",
    "9th Plymouth",
    "9th Plymouth",
    "10th Plymouth",
    "11th Plymouth",
    "12th Plymouth",
    "1st Suffolk",
    "2nd Suffolk",
    "3rd Suffolk",
    "4th Suffolk",
    "5th Suffolk",
    "6th Suffolk",
    "7th Suffolk",
    "8th Suffolk",
    "9th Suffolk",
    "10th Suffolk",
    "11th Suffolk",
    "12th Suffolk",
    "13th Suffolk",
    "14th Suffolk",
    "15th Suffolk",
    "16th Suffolk",
    "17th Suffolk",
    "18th Suffolk",
    "19th Suffolk",
    "1st Worcester",
    "2nd Worcester",
    "3rd Worcester",
    "3rd Worcester",
    "4th Worcester",
    "5th Worcester",
    "6th Worcester",
    "7th Worcester",
    "8th Worcester",
    "9th Worcester",
    "10th Worcester",
    "11th Worcester",
    "12th Worcester",
    "13th Worcester",
    "14th Worcester",
    "15th Worcester",
    "16th Worcester",
    "17th Worcester",
    "18th Worcester"
]

candidates = {
    "Clinton/ Kaine": 'Hillary Clinton - DEM',
    'Trump/ Pence': 'Donald J. Trump - REP',
    'Johnson/ Weld': 'Gary Johnson - LIB',
    'Stein/ Baraka': 'Jill Stein - GRE',
    'Mcmullin/ Johnson': 'Evan McMullin - ',
    'Kotlikoff/ Leamer': 'Laurence Kotlikoff - ',
    'Feegbeh/ O\'Brien': 'William Feegbeh - ',
    'Moorehead/ Lilly': 'Monica Moorehead - ',
    'Schoenke/ Mitchel': 'Marshall Schoenke - ',
    'All Others': 'Write-ins - ',
    'No Preference': 'No Preference - ',
    'Blank Votes': 'Blank Votes - ',
    'Total Votes Cast': 'Total - ',
    "Richard E. Neal": "Richard E. Neal - DEM",
    "Frederick O. Mayock": "Frederick O. Mayock - ",
    "Thomas T. Simmons": "Thomas T. Simmons - LIB",
    "James P. McGovern": "James P. McGovern - DEM",
    "Nicola S. Tsongas": "Nicola S. Tsongas - DEM",
    "Ann Wofford": "Ann Wofford - REP",
    "Joseph P. Kennedy, III": "Joseph P. Kennedy, III - DEM",
    "David A. Rosa": "David A. Rosa - REP",
    "Katherine M. Clark": "Katherine M. Clark - DEM",
    "Seth W. Moulton": "Seth W. Moulton - DEM",
    "Michael E. Capuano": "Michael E. Capuano - DEM",
    "Stephen F. Lynch": "Stephen F. Lynch - DEM",
    "William Burke": "William Burke - REP",
    "William Richard Keating": "William Richard Keating - DEM",
    "Mark C. Alliegro": "Mark C. Alliegro - REP",
    "Paul J. Harrington": "Paul J. Harrington - ",
    "Christopher D. Cataldo": "Christopher D. Cataldo - ",
    "Anna Grace Raduc": "Anna Grace Raduc - ",
    "Joseph C. Ferreira": "Joseph C. Ferreira - DEM",
    "Robert L. Jubinville": "Robert L. Jubinville - DEM",
    "Brad Williams": "Brad Williams - REP",
    "Marilyn Petitto Devaney": "Marilyn Petitto Devaney - DEM",
    "Christopher A. Iannella, Jr.": "Christopher A. Iannella, Jr. - DEM",
    "Eileen R. Duff": "Eileen R. Duff - DEM",
    "Richard A. Baker, Jr.": "Richard A. Baker, Jr. - REP",
    "Terrence W. Kennedy": "Terrence W. Kennedy - DEM",
    "Jennie L. Caissie": "Jennie L. Caissie - REP",
    "Matthew Cj Vance": "Matthew CJ Vance - DEM",
    "Mary E. Hurley": "Mary E. Hurley - DEM",
    "Adam G. Hinds": "Adam G. Hinds - DEM",
    "Christine M. Canning": "Christine M. Canning - REP",
    "James E. Timilty":"James E. Timilty - DEM",
    "Michael J. Rodrigues": "Michael J. Rodrigues - DEM",
    "Mark C. Montigny": "Mark C. Montigny - DEM",
    "Julian Andre Cyr": "Julian Andre Cyr - DEM",
    "Anthony E. Schiavi": "Anthony E. Schiavi - REP",
    "Kathleen  A. O'Connor Ives": "Kathleen A. O'Connor Ives - DEM",
    "Joan B. Lovely": "Joan B. Lovely - DEM",
    "Thomas M. McGee": "Thomas M. McGee - DEM",
    "Bruce E. Tarr": "Bruce E. Tarr - REP",
    "Barbara A. L'Italien": "Barbara A. L'Italien - DEM",
    "Susan M. Laplante": "Susan M. Laplante - REP",
    "James T. Welch": "James T. Welch - DEM",
    "Eric P. Lesser": "Eric P. Lesser - DEM",
    "James Chip Harrington": "James Chip Harrington - REP",
    "Donald F. Humason, Jr": "Donald F. Humason, Jr - REP",
    "Jerome Parker-O'grady": "Jerome Parker-O'Grady - DEM",
    "Stanley C. Rosenberg": "Stanley C. Rosenberg - DEM",
    "Donald Peltier": "Donald Peltier - REP",
    "Eileen M. Donoghue": "Eileen M. Donoghue - DEM",
    "Patricia D. Jehlen": "Patricia D. Jehlen - DEM",
    "Michael J. Barrett": "Michael J. Barrett - DEM",
    "Kenneth J. Donnelly": "Kenneth J. Donnelly - DEM",
    "Jason M. Lewis": "Jason M. Lewis - DEM",
    "Vincent Lawrence Dixon": "Vincent Lawrence Dixon - REP",
    "Cynthia Stone Creem": "Cynthia Stone Creem - DEM",
    "Karen E. Spilka": "Karen E. Spilka - DEM",
    "James B. Eldridge": "James B. Eldridge - DEM",
    "Ted Busiek": "Ted Busiek - REP",
    "Terra Friedrichs": "Terra Friedrichs - ",
    "Sal N. DiDomenico": "Sal N. DiDomenico - DEM",
    "Richard J. Ross": "Richard J. Ross - REP",
    "Kristopher K. Aleksov": "Kristopher K. Aleksov - DEM",
    "Walter F. Timilty, Jr.": "Walter F. Timilty, Jr. - DEM",
    "Jonathan D. Lott": "Jonathan D. Lott - ",
    "John F. Keenan": "John F. Keenan - DEM",
    "Alexander N. Mendez": "Alexander N. Mendez - ",
    "Michael F. Rush": "Michael F. Rush - DEM",
    "Vinny M. deMacedo": "Vinny M. deMacedo - REP",
    "Patrick M. O'Connor": "Patrick M. O'Connor - REP",
    "Paul J. Gannon": "Paul J. Gannon - DEM",
    "Marc R. Pacheco": "Marc R. Pacheco - DEM",
    "Sandra M. Wright": "Sandra M. Wright - REP",
    "Michael D. Brady": "Michael D. Brady - DEM",
    "Linda Dorcena Forry": "Linda Dorcena Forry - DEM",
    "Sonia Rosa Chang-DÍaz": "Sonia Rosa Chang-DÍaz - DEM",
    "Joseph A. Boncore": "Joseph A. Boncore - DEM",
    "William N. Brownsberger": "William N. Brownsberger - DEM",
    "Jennifer L. Flanagan": "Jennifer L. Flanagan - DEM",
    "Ryan C. Fattman": "Ryan C. Fattman - REP",
    "Anne M. Gobi": "Anne M. Gobi - DEM",
    "James P. Ehrhard": "James P. Ehrhard - REP",
    "Harriette L. Chandler": "Harriette L. Chandler - DEM",
    "Michael O. Moore": "Michael O. Moore - DEM",
    "Mesfin H. Beshir": "Mesfin H. Beshir - REP"
}

with open('csvs/PD43+__2016_President_General_Election_including_precincts.csv', 'r') as president_csv:
    reader = csv.DictReader(president_csv, delimiter=',')
    for row in reader:
        cols = [x for x in row.keys() if x not in ['City/Town', 'Ward', 'Pct']]
        for col in cols:
            candidate, party = candidates[col].split(' - ')
            results.append([row['City/Town'], row['Ward'], row['Pct'], 'President', None, party, candidate, int(row[col].replace(',',''))])

for district in ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th']:
    file_name = 'csvs/PD43+__2016_U_S_House_General_Election_%s_Congressional_District_including_precincts.csv' % district
    with open(file_name, 'r') as congress_csv:
        reader = csv.DictReader(congress_csv, delimiter=',')
        for row in reader:
            cols = [x for x in row.keys() if x not in ['City/Town', 'Ward', 'Pct']]
            for col in cols:
                candidate, party = candidates[col].split(' - ')
                results.append([row['City/Town'], row['Ward'], row['Pct'], 'U.S. House', district[0], party, candidate, int(row[col].replace(',',''))])

for district in ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th']:
    file_name = 'csvs/PD43+__2016_Governor_s_Council_General_Election_%s_District_including_precincts.csv' % district
    with open(file_name, 'r') as council_csv:
        reader = csv.DictReader(council_csv, delimiter=',')
        for row in reader:
            cols = [x for x in row.keys() if x not in ['City/Town', 'Ward', 'Pct']]
            for col in cols:
                candidate, party = candidates[col].split(' - ')
                results.append([row['City/Town'], row['Ward'], row['Pct'], 'Governor\'s Council', district[0], party, candidate, int(row[col].replace(',',''))])

for district in state_senate_districts:
    file_name = 'csvs/PD43+__2016_State_Senate_General_Election_%s_District_including_precincts.csv' % district.replace(' ','_').replace(',','')
    with open(file_name, 'r') as council_csv:
        reader = csv.DictReader(council_csv, delimiter=',')
        for row in reader:
            cols = [x for x in row.keys() if x not in ['City/Town', 'Ward', 'Pct']]
            for col in cols:
                candidate, party = candidates[col].split(' - ')
                results.append([row['City/Town'], row['Ward'], row['Pct'], 'State Senate', district, party, candidate, int(row[col].replace(',',''))])

url = "http://electionstats.state.ma.us/elections/search/year_from:2016/year_to:2016/office_id:8/stage:General"
r = requests.get(url
soup = BeautifulSoup(r.text)
table = soup.find('table', id="search_results_table")
for row in table.findAll('tr')[1:]:
    state_house_candidates = [{x.find('a').text : x.find('div', {'class': 'party'}).text} for x in row.findAll('td', {'class' : "candidate"}) if x.find('a')]
    state_house_candidates.append({"All Others": None})
    state_house_candidates.append({"Blank Votes": None})
    state_house_candidates.append({"Total Votes Cast": None})
    final_cands = {k: v for d in state_house_candidates for k, v in d.items()}
    

for district in state_house_districts:
    file_name = 'PD43+__2016_State_Senate_General_Election_%s_District_including_precincts.csv' % district.replace(' ','_').replace(',','')
    with open(file_name, 'r') as council_csv:
        reader = csv.DictReader(council_csv, delimiter=',')
        for row in reader:
            cols = [x for x in row.keys() if x not in ['City/Town', 'Ward', 'Pct']]
            for col in cols:
                candidate, party = candidates[col].split(' - ')
                results.append([row['City/Town'], row['Ward'], row['Pct'], 'State Senate', district, party, candidate, int(row[col].replace(',',''))])



with open('2016/20161108__ma__general__precinct.csv','wb') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['town', 'ward', 'precinct', 'office', 'district', 'party', 'candidate', 'votes'])
    csvwriter.writerows(results)
