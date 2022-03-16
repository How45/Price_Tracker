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
        page = requests.get(i, headers={'User-Agent':'Mozilla/2.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'})

        if str(page.status_code) != "200": # If page not found
            print("This wont work, its the {0} URL you have entered".format(i))
            main()

        soup = BeautifulSoup(page.content, 'html.parser')

        div_elm = soup.find("div",class_="a-section a-spacing-none aok-align-center")
        print(div_elm)
        price = "£-1"
       # price = web.webPrice(soup)
        
        # check if there is a £ or not
        if price[0] == "£":
            priceLst.append(float(price[1:]))
        else:
            priceLst.append(float(price[0:]))
        
        dates = datetime.datetime.now().strftime('%d/%m/%Y')
    return priceLst,dates

def main():
    linkLst = ["https://www.amazon.co.uk/OUKEYI-Stuffed-Animal-Plushies-Pillows/dp/B08PT88YNP"]
    # priceLst, date = 
    getPriceURL(linkLst)
main()