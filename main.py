import requests
from bs4 import BeautifulSoup

url = "https://steamcommunity.com/market/search?appid=730&q=case+key#p1_default_desc"

response = requests.get(url)

soup = BeautifulSoup(response.text)
# print(soup, type(soup), sep= '\n')

# variable = soup.find("span", {"class": "market_listing_item_name"})

retrievedOb = soup.find_all("div", "market_listing_row market_recent_listing_row market_listing_searchresult")

\

print(retrievedOb[1])

