import datetime
import requests
from bs4 import BeautifulSoup
import website_ids as web


def get_prices(url_list):
    """
    Gets prices from page
    """

    prices_list = []
    for url in url_list:
        page = requests.get(url, headers={'User-Agent':'Mozilla/2.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'},timeout=10)

        if str(page.status_code) != '200':  # If page not found
            print(f'This wont work, its the {url} URL you have entered')

        soup = BeautifulSoup(page.content, 'html.parser')
        price = web.web_price(soup)  # Finding price

        # check if there is a £ or not
        if price[0] == '£':
            prices_list.append(float(price[1:]))
        else:
            prices_list.append(float(price[0:]))

        dates = datetime.datetime.now().strftime('%Y-%m-%d')
    return prices_list, dates
