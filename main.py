from requests_html import HTMLSession
from bs4 import BeautifulSoup
import numpy as np
import requests
from celery import Celery
import time


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

'''
Retrieves the lowest price from a list
'''
def lowestPriceExtractor(inList):
    lowestpricearr = []
    lowestpriceSoup = inList.find(class_="sale_price")
    for lowestpriceSoup in lowestpriceSoup:
        lowestpricearr.append(lowestpriceSoup)
    lowestpriceval = "".join(str(x) for x in lowestpricearr)
    lowestpriceret = lowestpriceval.replace("$",'')
    lowestpriceret = lowestpriceret.replace("USD", '')
    return float(lowestpriceret)


def getNextPage(url):

    firstPos = url.index("start=") + 6
    lastPos = url.find("&count=10")
    lastPart = url[lastPos: len(url)]

    curpage = url[firstPos:lastPos]

    nextpage = int(curpage) + 10
    url = "https://steamcommunity.com/market/search/render/?query=&start=" + str(nextpage) + lastPart
    return url

def isNextPage(soup):
    page = soup.find("span", class_="pagebtn")
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

def getData (url):
    # time.sleep(3)
    r = requests.get(url, headers={'User-agent': 'your bot 0.1'} )
    while r.status_code == 429:
        print("Retrying in 60 seconds")
        time.sleep(60)
        r = requests.get(url, headers={'User-agent': 'your bot 0.1'})
    rJ = r.json()
    rH = rJ['results_html']
    soup = BeautifulSoup(rH, 'html.parser')
    return soup









session = HTMLSession()
url = "https://steamcommunity.com/market/search/render/?query=&start=0&count=10&search_descriptions=0&sort_column=popular&sort_dir=desc"

app = Celery('task', broker='amqp://guest@localhost//')


soup = getData(url)


#list - all listings of page extracted
list = soup.find_all(class_ = "market_listing_row market_recent_listing_row market_listing_searchresult")
#Gets amount of listings
listLen = len(list)

#Gets listing in single page and puts in array
#pricearr: name, lowets price, highest price

nameArr = pageNameRetrieve(list)
priceArr = pageValueRetrieve(list)

print(nameArr)
print(priceArr)

url = getNextPage(url)



while True == True:
    url = getNextPage(url)
    soup = getData(url)
    # list - all listings of page extracted
    list = soup.find_all("div", "market_listing_row market_recent_listing_row market_listing_searchresult")
    # Gets amount of listings
    listLen = len(list)
    # Gets listing in single page and puts in array
    # pricearr: name, lowets price, highest price
    nameArr2 = pageNameRetrieve(list)
    priceArr2 = pageValueRetrieve(list)
    print("=========")
    print(url)
    print(nameArr2)
    print(priceArr2)






