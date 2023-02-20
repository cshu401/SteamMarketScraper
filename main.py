import requests
from bs4 import BeautifulSoup
import numpy as np


'''
    @param inList - input single list
    @return value in string of highest price
'''
def highestPriceExtractor(inList):
    highestpriceSoup = inList.find(class_="normal_price")
    highestpriceSoup = str(highestpriceSoup)
    highestpriceloc1 = highestpriceSoup.find("data-price")
    highestpriceloc2 = highestpriceSoup.find("span>")
    highestprice = highestpriceSoup[highestpriceloc1:highestpriceloc2]
    highestpriceloc21 = highestprice.find(">") + 1
    highestpriceloc22 = highestprice.find("</")
    highestprice2 = highestprice[highestpriceloc21:highestpriceloc22]

    highestprice2 = highestprice2.replace("$",'')
    highestprice2 = highestprice2.replace("USD", '')
    return float(highestprice2)

def lowestPriceExtractor(inList):
    lowestpricearr = []
    lowestpriceSoup = inList.find(class_="sale_price")
    for lowestpriceSoup in lowestpriceSoup:
        lowestpricearr.append(lowestpriceSoup)
    lowestpriceval = "".join(str(x) for x in lowestpricearr)
    lowestpriceret = lowestpriceval.replace("$",'')
    lowestpriceret = lowestpriceret.replace("USD", '')
    return float(lowestpriceret)


def isNextPage(soup):
    page = soup.find("span", class_ = "pagebtn")
    if not page:
        return False
    else:
        return True

'''
list - page to extract from
return- names of each object
'''
def pageNameRetrieve(list):
    # Gets listing in single page and puts in array
    # pricearr: name, lowest price, highest price
    listLen = len(list)
    nameArr = [0] * listLen
    i = 0
    for i in range(listLen):
        name = list[i].get("data-hash-name")
        # extracts lowest price
        nameArr[i] = name
    return nameArr


''''
list - page to extract from
return - price of each object
'''
def pageValueRetrieve(list):
    # Gets listing in single page and puts in array
    # pricearr: name, lowest price, highest price
    listLen = len(list)
    priceArr = np.zeros((listLen, 2), dtype=float)
    i = 0
    for i in range(listLen):
        lowestprice = lowestPriceExtractor(list[i])
        # extracts highest price
        highestprice = highestPriceExtractor(list[i])
        priceArr[i][0] = lowestprice
        priceArr[i][1] = highestprice
    return priceArr







url = "https://steamcommunity.com/market/search?appid=730&q=case+key#p1_default_desc"

response = requests.get(url)

soup = BeautifulSoup(response.text, features="html.parser")


#list - all listings of page extracted
list = soup.find_all("div", "market_listing_row market_recent_listing_row market_listing_searchresult")
#Gets amount of listings
listLen = len(list)




#Gets listing in single page and puts in array
#pricearr: name, lowets price, highest price

nameArr = pageNameRetrieve(list)
priceArr = pageValueRetrieve(list)


print(nameArr)
print(priceArr)





