Steam Marketplace Scraper

This Python code scrapes the Steam Marketplace and extracts the name, lowest price, and highest price of items for a given number of pages. The BeautifulSoup library is used to parse the HTML of the Steam Marketplace pages.
Prerequisites

    Python 3.11.1 installed
    Beautiful Soup 4 library
    Requests
    Pandas
    Numpy

Usage

    Set the url variable to the desired Steam Marketplace page URL.
    Set the pagetoscrape variable to the desired number of pages to scrape.
    Run the code.

The code will output the name, lowest price, highest price, and price difference of each item scraped to the console.
Functions
highestPriceExtractor(inList)

Extracts the highest price of an item from the given HTML list of items.
lowestPriceExtractor(inList)

Extracts the lowest price of an item from the given HTML list of items.
getNextPage(url)

Returns the URL of the next page to scrape.
pageNameRetrieve(list)

Returns the names of each item in the given HTML list of items.
pageValueRetrieve(list)

Returns the lowest and highest prices of each item in the given HTML list of items.
getData(url)

Retrieves the HTML of the given Steam Marketplace page.
