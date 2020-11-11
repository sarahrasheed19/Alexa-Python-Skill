import requests, re, json
from bs4 import BeautifulSoup
from calendar import month_abbr
from word2number import w2n
from datetime import datetime

# gets information from academic calendar and creates soup parser
url = "https://www.adelphi.edu/academics/academic-calendar/"
html_text = requests.get(url).text
soup = BeautifulSoup(html_text, 'html.parser')

# finds all <td> tags
td_tags = soup.find_all('td')

# creates lists for date and events
date = []
event = []

# pattern to search the text within tags to check if it is a date or not
pattern = '|'.join(month_abbr[1:])

# searches through tags and appends dates and events together
for tag in td_tags:
    tag = str(tag.text)
    ifDate = re.search(pattern, tag, re.IGNORECASE) # if text in tag is a date
    if (ifDate and len(tag) <= 15):
        date.append(tag.strip())
    else:
        event.append(tag.strip()) # if it is not a date, it is an event, so append

# zips the two lists together into a dictionary
date_events = dict(zip(date, event))

with open('AdelphiCalendar.json') as json_data:
    json.dump(date_events, json_data)
