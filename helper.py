import os
import datetime
import matplotlib.pyplot as plt
import numpy as np
import page_retrival as page
import sql_commands as sql
import app

def draw_graph(price_list, items, dates):
    """
    Draws graph
    """
    colours = ("--b.", "--r.", "--g.", "--c.", "--m.", "--y.", "--k.")

    # x_axis = np.array(date)
    y_axis = np.array(price_list)
    for i, _ in enumerate(items):
        plt.plot(dates, y_axis[i], colours[i], label=items[i])
    plt.legend()

    print('Press any key to close')
    while True:
        if plt.waitforbuttonpress():
            break
    plt.close()


def get_links():
    """
    gets links from user
    """
    link_list, title_list = [], []

    file_name = input("Enter name of graph: ")
    linked_accounts = int(input("Enter amount of items you wanna be tracked: "))

    for _ in range(linked_accounts):
        url = input("Enter Amazon item URL (page of item you wanna track): ")
        links = url.rsplit("/", 1)[0]  # Removes unnecessary link lenght
        # ^ (NEED TO DO A CHECK IF ITS ALREADY SHORT)
        link_list.append(links)

        item_name = input("Enter name of Item: ")
        title_list.append(item_name)

    return link_list, title_list, file_name


def initialise_data_graph(links, prices, file_name, items, date):
    """
    Store Data for graph in CSV
    """
    for item in items:
        if sql.get_name(file_name):
            print("Can't have the same file_name")
            app.main()

    for link in (links):
        sql.add_links(link)

    links_id = sql.get_link_id(items, file_name)
    print(links_id)

    for price, item, date, link_id in zip(prices, items, date, links_id):
        sql.add_items(file_name, item, price, date, link_id)
    print("ADDED")


def load(name):
    """
    gets data from folder and update if needed
    """
    attribute_data = sql.get_attributes(name)
    item_name, all_prices, item_dates, url, link_id, new_prices = [], [], [], [], [], None
    for item in attribute_data:
        if item[0] not in item_name:
            item_name.append(item[0])
        if item[1] not in item_dates:
            item_dates.append(item[1])
        url.append(item[2])
        if item[3] not in link_id:
            link_id.append(item[3])

    for name in item_name:
        prices = sql.get_prices(name)
        all_prices.append([price[0] for price in prices])

    item_dates = [date.strftime('%Y-%m-%d') for date in item_dates]
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    if current_date not in item_dates:
        print('Retrieving new data')
        new_prices, new_dates = page.get_prices(url)

    print(all_prices, item_name, item_dates)
    if not new_prices or new_prices == all_prices[-1]:
        print("Drawing")
        draw_graph(all_prices, item_name, item_dates)
    else:
        print("Adding new_price to all_prices and updating the file")
        sql.add_items(name, item_name, new_prices, new_dates, link_id)

    load(name)


def delete(name): # CHANGE to SQL
    """
    Deletes anything that it wants to follow
    """
    if os.path.exists(f'following/{name}.csv'):
        os.remove(f'following/{name}.csv')
        print(f'Deleted {name}')
