import requests
from bs4 import BeautifulSoup





url = "https://steamcommunity.com/market/search?appid=730&q=case+key#p1_default_desc"

response = requests.get(url)

soup = BeautifulSoup(response.text, features="html.parser")
# print(soup, type(soup), sep= '\n')


#Gets all listings
list = soup.find_all("div", "market_listing_row market_recent_listing_row market_listing_searchresult")
#Gets amount of listings
listLen = len(list)

lowestprice = list[0].find(class_ = "sale_price")
highestprice = list[0].find(class_ = "normal_price")




print(list[0])
print("===============================")
print("Lowest Price:" + str(lowestprice))
print("Highest Price:" + str(highestprice))

