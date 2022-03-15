from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import numpy as np
import os
import datetime
import csv 

def getPriceURL(lst):
    priceLst = []

    for i in lst:
        page = requests.get(i, headers={'User-Agent':'Mozilla/2.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'})

        if str(page.status_code) != "200": # If page not found
            print("This wont work, its the {0} URL you have entered".format(i))
            main()

        soup = BeautifulSoup(page.content, 'html.parser')
        
        try: 
            price = soup.find("span",id="priceblock_ourprice").get_text()
        except:
            pass
        try:
            price = soup.find("span",id="priceblock_saleprice").get_text()
        except:
            pass
        try:
            price = soup.find("span",id="priceblock_dealprice").get_text()
        except:
            pass
        try:
            price = soup.find("span",class_="a-price-whole").get_text()
        except:
            pass
        try:
            price = soup.find("span",class_="a-offscreen").get_text()
        except:
            print("This link doesnt match any of thses")
        
        # check if there is a £ or not
        if price[0] == "£":
            priceLst.append(float(price[1:]))
        else:
            priceLst.append(float(price[0:]))

        dates = datetime.datetime.now().replace(microsecond=0).strftime("%x")
    return priceLst,dates

def main():
    linkLst = ["https://www.amazon.co.uk/TCL-43P617K-Android-Freeview-Bluetooth/dp/B098WSJXXW"]
    # priceLst, date = 
    getPriceURL(linkLst)
main()