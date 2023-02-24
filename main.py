from requests_html import HTMLSession
from bs4 import BeautifulSoup
import numpy as np
import requests
import time
import pandas as pd


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
    return highestprice2

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
    return lowestpriceret


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

'''
arr1: base array
arr2: array to be combined to
arrPos: position arrMain is at
'''
def arrayCombine(arrMain, arr1, pos):
    i = 0;
    arrNew = arr1[:,pos]
    for i in range(len(arrNew)):
        arrMain.append(arrNew[i])
    return arrMain








session = HTMLSession()
url = "https://steamcommunity.com/market/search/render/?query=&start=0&count=10&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=730"
soup = getData(url)
curpage = 0
pagetoscrape = 5

marketData = np.zeros((3,50), dtype = str)
nameList = []
lowestPriceList = []
highestPriceList = []


while curpage < pagetoscrape:

    soup = getData(url)
    # list - all listings of page extracted
    list = soup.find_all("div", "market_listing_row market_recent_listing_row market_listing_searchresult")
    # Gets amount of listings
    listLen = len(list)
    # Gets listing in single page and puts in array
    # pricearr: name, lowets price, highest price
    nameArrCur = pageNameRetrieve(list)
    priceArr = pageValueRetrieve(list)
    i = 0
    lowestpricearr=[0] * 10
    highestpricearr=[0] * 10
    while i < len(priceArr):
        lowestpricearr[i] = priceArr[i][0]
        highestpricearr[i] = priceArr[i][1]
        i = i + 1
    marketData = np.concatenate((nameArrCur,lowestpricearr,highestpricearr)).reshape(3,10)

    nameList = np.append(nameList, nameArrCur)
    lowestPriceList = np.append(lowestPriceList,lowestpricearr)
    highestPriceList = np.append(highestPriceList, highestpricearr)








    print("=========")
    print(url)

    curpage = curpage + 1
    url = getNextPage(url)

print("=========")
print("=========")

df = pd.DataFrame({"Name": nameList, "LowestPrice": lowestPriceList, "HighestPrice": highestPriceList}, )
print(df)







