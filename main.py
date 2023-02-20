import requests
from bs4 import BeautifulSoup


'''
    @param inList - input single list
    @return value in string of highest price
'''
def highestPriceExtractor(inList):
    highestpriceSoup = inList.find(class_="normal_price")
    highestpriceSoup = str(highestpriceSoup)
    print(highestpriceSoup)
    highestpriceloc1 = highestpriceSoup.find("data-price")
    highestpriceloc2 = highestpriceSoup.find("span>")
    highestprice = highestpriceSoup[highestpriceloc1:highestpriceloc2]
    highestpriceloc21 = highestprice.find(">") + 1
    highestpriceloc22 = highestprice.find("</")
    highestprice2 = highestprice[highestpriceloc21:highestpriceloc22]
    return highestprice2

def lowestPriceExtractor(inList):
    lowestpriceSoup = inList.find(class_="sale_price")
    for lowestpriceSoup in lowestpriceSoup:
        print(lowestpriceSoup)




url = "https://steamcommunity.com/market/search?appid=730&q=case+key#p1_default_desc"

response = requests.get(url)

soup = BeautifulSoup(response.text, features="html.parser")
# print(soup, type(soup), sep= '\n')


#list - all listings of page extracted
list = soup.find_all("div", "market_listing_row market_recent_listing_row market_listing_searchresult")
#Gets amount of listings
listLen = len(list)
#gets name of listings


name = list[0].get("data-hash-name")

#extracts lowest price
lowestprice = lowestPriceExtractor(list[0])
# lowestpriceSoup = list[0].find(class_ = "sale_price")
# for lowestpriceSoup in lowestpriceSoup:
#     print(lowestpriceSoup)

#extracts highest price
highestprice = highestPriceExtractor(list[0])








print(list[0])
print("===============================")
print("Name:" + str(name))
print("Lowest Price:" + str(lowestprice))
print("Highest Price:" + str(highestprice))


