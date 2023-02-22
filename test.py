import requests
from bs4 import BeautifulSoup

counter = 432800

data = []

while True:
    url = f'https://steamcommunity.com/market/search/render/?query=&start={counter}&count=10&search_descriptions=0&sort_column=popular&sort_dir=desc'
    json_data = requests.get(url).json()
    soup = BeautifulSoup(json_data['results_html'])

    print(url)
    for e in soup.select('[id^="resultlink_"]'):
        data.append(list(e.stripped_strings))

    if counter < json_data['total_count']:
        counter = counter + 1
    else:
        break
data