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
    sorted_cryptos = {} #dictionary of sorted coins
    coinmarketcap = requests.get('https://coinmarketcap.com/')
    soup = BeautifulSoup(coinmarketcap.content, 'html.parser')
    pages = calculate_pages(soup) #get # of pages
     
    #scrape data from pages
    for i in range (1, pages + 1):
        time.sleep(0.5)

        print("Scraping page " + str(i) + " of " + str(pages) + "...")
        url = 'https://coinmarketcap.com/?page=' + str(i) #generate the page url
        site = requests.get(url)
        soup = BeautifulSoup(site.content, 'html.parser')
        
        data = soup.find('script', id = "__NEXT_DATA__", type = "application/json")
        crypto_data = json.loads(data.contents[0])
        listings = crypto_data['props']['initialState']['cryptocurrency']['listingLatest']['data']

        #add symbol and generated url to dictionary, name as key
        for i in listings:
            cryptos[str(i['name'])] = str(i['symbol']), "https://coinmarketcap.com/currencies/" + str(i['slug'])
    
    print("Done scraping...")

    for key in sorted(cryptos):
        sorted_cryptos[key] = cryptos[key] #create new dictionary ordered by name

    print_to_csv(sorted_cryptos)


#calculates the number of pages in the table of cryptos from the "Showing 1 - X out of Y" text
def calculate_pages(soup):
    text = soup.findAll('p', {'class': 'sc-1eb5slv-0 kDEzev'}, string = re.compile("Showing"))
    text_numbers = re.findall(r'\d+',str(text)) #get all the numbers in the "showing" line

    items_total = int(text_numbers[len(text_numbers) - 1]) #get the max number of items from the last number found in the "showing" line
    items_per_page = int(text_numbers[len(text_numbers) - 2]) #get the items per page from the SECOND to last number found in "showing" line

    pages = round(items_total / items_per_page) #calculate number of pages

    return pages

#output the dictionary of crypto names to csv file
def print_to_csv(cryptos):
    print("Printing to csv...")
    crypto_names = []
    crypto_symbols = []
    crypto_urls = []

    for key in cryptos:
        crypto_names.append(str(key))
        crypto_symbols.append(str(cryptos[key][0]))
        crypto_urls.append(str(cryptos[key][1]))

    dataframe = pandas.DataFrame(columns = ['name', 'symbol', 'url'])

    dataframe['name'] = crypto_names
    dataframe['symbol'] = crypto_symbols
    dataframe['url'] = crypto_urls
    
    file = 'cryptos.csv'
    dataframe.to_csv(file, index = False)
    
    print("----------------------------------------------")
    print("- Data written to " + file + " successfully! -")
    print("----------------------------------------------")

scrape_crypto_names()
