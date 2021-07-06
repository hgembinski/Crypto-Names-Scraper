#Haiden Gembinski
#Script to scrape the names of all
#available cryptocurrencies from CoinMarketCap.com.

from bs4 import BeautifulSoup
import re
import requests
import pandas
import json
import time

def scrape_crypto_names():
    cryptos = {} #dictionary of coins
    coinmarketcap = requests.get('https://coinmarketcap.com/')
    soup = BeautifulSoup(coinmarketcap.content, 'html.parser')
    text = soup.findAll('p', {'class': 'sc-1eb5slv-0 kDEzev'}, string = re.compile("Showing"))
    pages = calculate_pages(soup)

    #scrape first page
    print("Scraping page 1 of " + str(pages) + "...")
    data = soup.find('script', id = "__NEXT_DATA__", type = "application/json")
    crypto_data = json.loads(data.contents[0])
    listings = crypto_data['props']['initialState']['cryptocurrency']['listingLatest']['data']

    for i in listings:
        cryptos[str(i['name'])] = str(i['symbol']), str(i['slug']) #add to dictionary
     
    #scrape the rest of the pages
    for i in range (2, pages + 1):
        time.sleep(0.5)

        print("Scraping page " + str(i) + " of " + str(pages) + "...")
        url = 'https://coinmarketcap.com/?page=' + str(i) #generate the url
        site = requests.get(url)
        soup = BeautifulSoup(site.content, 'html.parser')
        
        data = soup.find('script', id = "__NEXT_DATA__", type = "application/json")
        crypto_data = json.loads(data.contents[0])
        listings = crypto_data['props']['initialState']['cryptocurrency']['listingLatest']['data']

        for i in listings:
            cryptos[str(i['name'])] = str(i['symbol']), str(i['slug']) #add to dictionary
    
    for i in sorted(cryptos.keys()):
        print(i + " " + str(cryptos[i]))
    print("Total entries: " + str(len(cryptos)))


#calculates the number of pages in the table of cryptos from the "Showing 1 - X out of Y" text
def calculate_pages(soup):
    text = soup.findAll('p', {'class': 'sc-1eb5slv-0 kDEzev'}, string = re.compile("Showing"))
    text_numbers = re.findall(r'\d+',str(text)) #get all the numbers in the "showing" line

    items_total = int(text_numbers[len(text_numbers) - 1]) #get the max number of items from the last number found in the "showing" line
    items_per_page = int(text_numbers[len(text_numbers) - 2]) #get the items per page from the SECOND to last number found in "showing" line

    pages = round(items_total / items_per_page) #calculate number of pages

    return pages

scrape_crypto_names()
