from bs4 import BeautifulSoup
import requests
import datetime
import website_ids as web

def getPriceURL(lst):
    price_list = []
    for i in lst:
        page = requests.get(i, headers={'User-Agent':'Mozilla/2.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'})

        if str(page.status_code) != "200": # If page not found
            print("This wont work, its the {0} URL you have entered".format(i))

        soup = BeautifulSoup(page.content, 'html.parser')
        price = web.web_price(soup) # Finding price

        # check if there is a £ or not
        if price[0] == "£":
            price_list.append(float(price[1:]))
        else:
            price_list.append(float(price[0:]))

        dates = datetime.datetime.now().strftime('%d/%m/%Y')
    return price_list,dates
