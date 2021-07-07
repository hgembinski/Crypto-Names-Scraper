#Haiden Gembinski
#Script to scrape the names of all
#available cryptocurrencies from CoinMarketCap.com.

from bs4 import BeautifulSoup
import tkinter
from tkinter import *
import re
import requests
import pandas
import json
import time

#main function / GUI
def scrape_crypto_names():
    root = tkinter.Tk()
    root.title("Crypto Name Scraper")
    root.geometry("500x500")
    root.config(bg = "light blue", highlightbackground = "steel blue", highlightcolor = "steel blue", highlightthickness = 10)

    #GUI
    titleframe = LabelFrame(root, bg = 'light blue', highlightbackground = "steel blue", highlightthickness = 10,
                relief = "flat", height = 75, width = 310).place(x = 250, y = 27.5, anchor = "center")
    title = Label(titleframe, text = "Crypto Name Scraper", bg = 'light blue',
                font = (None, 20, "bold")).place(x = 250, y = 30, anchor = "center")
    subtitle = Message(root, text = "This program compiles a list of all available cryptocurrencies on coinmarketcap.com", bg = 'light blue', 
                font = (None, 15, "italic"), justify = "center", width = 500).place(x = 250, y = 100, anchor = "center")
    activitytext = Label(root, text = "Currently Idle", bg = 'light blue', font = (None, 40))
    activitytext.place(x = 250, y = 200, anchor = "center")
    activitystatus = Message(root, text = "Click 'Go' to begin!", bg = 'light blue', width = 450, justify = "center", font = (None, 25))
    activitystatus.place(x = 250, y = 275, anchor = "center")

    #button calls scrape function
    go_button = Button(root, bg = "green", activebackground = 'light green', text = "Go!", relief = "raised", 
                font = (None, 30, "bold"))
    go_button.place(x = 250, y = 400, anchor = "center")
    go_button.config(command = lambda : scraper(root, activitytext, activitystatus, go_button))


    root.mainloop()

#main scrape function
def scraper(root, activitytext, activitystatus, go_button):
    activitytext.config(text = "Working on it...")
    go_button.config(bg = "light grey", state = "disabled")

    cryptos = {} #dictionary of coins
    sorted_cryptos = {} #dictionary of sorted coins
    coinmarketcap = requests.get('https://coinmarketcap.com/')
    soup = BeautifulSoup(coinmarketcap.content, 'html.parser')
    pages = calculate_pages(soup) #get # of pages to scrape

     
    #scrape data from pages
    for i in range (1, pages + 1):
        time.sleep(0.5) #wait half a second between pages to avoid server timeout
        activitystatus.config(text = "Scraping page " + str(i) + " of " + str(pages) + "...")
        print("beep " + str(i))
        root.update()

        url = 'https://coinmarketcap.com/?page=' + str(i) #generate the page url
        site = requests.get(url)
        soup = BeautifulSoup(site.content, 'html.parser')
        
        data = soup.find('script', id = "__NEXT_DATA__", type = "application/json")
        crypto_data = json.loads(data.contents[0])
        listings = crypto_data['props']['initialState']['cryptocurrency']['listingLatest']['data']

        #add symbol and generated url to dictionary, name as key
        for i in listings:
            cryptos[str(i['name'])] = str(i['symbol']), "https://coinmarketcap.com/currencies/" + str(i['slug'])

    #create new dictionary ordered by name
    for key in sorted(cryptos):
        sorted_cryptos[key] = cryptos[key]

    #print to file
    file = 'cryptos.csv'
    print_to_csv(sorted_cryptos, file)

    activitytext.config(text = "Done!")
    activitystatus.config(text = "Data has been written to " + file + " successfully!")
    go_button.config(bg = "green", state = "normal")


#calculates the number of pages in the table of cryptos from the "Showing 1 - X out of Y" text
def calculate_pages(soup):
    text = soup.findAll('p', {'class': 'sc-1eb5slv-0 kDEzev'}, string = re.compile("Showing")) #find the correct html line
    text_numbers = re.findall(r'\d+',str(text)) #find the numbers in the line

    items_total = int(text_numbers[len(text_numbers) - 1]) #get the max number of items from the last number found in the "showing" line
    items_per_page = int(text_numbers[len(text_numbers) - 2]) #get the items per page from the SECOND to last number found in "showing" line

    pages = round(items_total / items_per_page) #calculate number of pages

    return pages

#output the dictionary of crypto names to csv file
def print_to_csv(cryptos, file):
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
    
    dataframe.to_csv(file, index = False)

scrape_crypto_names()
