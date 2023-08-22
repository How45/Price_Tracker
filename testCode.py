from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import numpy as np
import os
import datetime
import csv
import websitePrice as web

def getPriceURL(lst):
    priceLst = []

    for i in lst:
        HEADER = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})
        page = requests.get(i, headers=HEADER)
        if str(page.status_code) != "200": # If page not found
            print("This wont work, its the {0} URL you have entered".format(i))
            main()

        soup = BeautifulSoup(page.content, "lxml")
        print(soup)
        price = web.webPrice(soup) # Finding price 
        
        # check if there is a £ or not
        if price[0] == "£":
            priceLst.append(float(price[1:]))
        else:
            priceLst.append(float(price[0:]))
        
        dates = datetime.datetime.now().strftime('%d/%m/%Y')
    return priceLst,dates

def main():
    linkLst = ["https://www.amazon.co.uk/TCL-43P617K-Android-Freeview-Bluetooth/dp/B098WSJXXW"]
    # priceLst, date = 
    getPriceURL(linkLst)
main()  