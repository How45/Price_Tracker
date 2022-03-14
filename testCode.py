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
            if soup.find("span",id="priceblock_ourprice").get_text() != None:
                price = soup.find("span",id="priceblock_ourprice").get_text()
        except:
            pass

        try:
            if soup.find("span",id="priceblock_saleprice").get_text() != None:
                price = soup.find("span",id="priceblock_saleprice").get_text()
        except:
            pass
        try:
            if soup.find("span",id="priceblock_dealprice").get_text() != None:
                price = soup.find("span",id="priceblock_dealprice").get_text()
        except:
            pass

        price = soup.find("span",class_="a-price-whole").get_text()

        priceLst.append(float(price[0:]))
        
        getDate = datetime.datetime.now()
        dates = getDate.strftime("%x")
    print(priceLst)
    return priceLst,dates

def main():
    linkLst = ["https://www.amazon.co.uk/TeckNet-Wireless-Keyboard-keyboard-Whisper-Quiet/dp/B00M75WPKO/ref=sr_1_14?crid=E39FAEH8J98G&keywords=keyboards&qid=1647269775&s=computers&sprefix=keyboards%2Ccomputers%2C152&sr=1-14"]
    # priceLst, date = 
    getPriceURL(linkLst)
main()