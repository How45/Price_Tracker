import csv
import os
import datetime
import matplotlib.pyplot as plt
import numpy as np
import page_retrival as page

def list_change(price_list):
    """Transposing the list so prices are in the same category."""
    return [[i[index] for i in price_list] for index in range(len(price_list[0]))]

def draw_graph(price_list,lst,date):
    """Draws graph"""
    colours = ["--b.","--r.","--g.","--c.","--m.","--y.","--k."]

    try:
        price_list = list_change(price_list)
    except TypeError:
        print("Single list")

    # x_axis = np.array(date)
    y_axis = np.array(price_list)

    for i in range(len(price_list)):
        plt.plot(date,y_axis[i],colours[i], label=lst[i])
    plt.legend()

    print('Press any key to close')
    while True:
        if plt.waitforbuttonpress():
            break
    plt.close()

def get_links():
    """gets links from user"""
    link_list, title_list = [], []

    file_name = input("Enter name of graph: ")
    linked_accounts = int(input("Enter amount of items you wanna be tracked (max. 7): "))

    for _ in range(linked_accounts):
        url = input("Enter Amazon item URL (page of item you wanna track): ")
        links = url.rsplit("/", 1)[0] # Removes unnecessary link lenght
        # ^ (NEED TO DO A CHECK IF ITS ALREADY SHORT)
        link_list.append(links)

        item_name = input("Enter name of Item: ")
        title_list.append(item_name)

    return link_list, title_list, file_name

def store_graph_data(user_links, price, file_name, name, date):
    """Store Data for graph in CSV"""
    price_date = price + [date]

    try:
        with open(f'following/{file_name}.csv','x', newline='',encoding='UTF-8') as file:
            writer = csv.writer(file)
            writer.writerow(user_links)
            writer.writerow(name)
            writer.writerow(price_date)
    except FileExistsError:
        print(f"Error: {file_name}.csv already exists. Returning to the menu.")

def load(name):
    """gets data from folder and update if needed"""
    file = open(f'following/{name}.csv','r',encoding='UTF-8')
    reader = csv.reader(file)

    all_prices, graph_name, url, item_date, new_price = [],[],[],[],None
    index = 0

    # Get all info
    for line in reader:
        price = []
        index += 1
        if index == 1: # Links to find new prices
            url = line.copy()

        elif index == 2: # get name always stored on line 2
            graph_name = line.copy()

        else: # line 3 onwards are all the price from old on top to new at the very bottom
            price = line.copy()
            item_date.append(price[-1])
            price.remove(price[-1])
            all_prices.append(price)

    file.close()

    # Doesn't need to retrieve data if date is in file
    current_date = datetime.datetime.now().strftime('%d/%m/%Y')
    if current_date not in item_date:
        print('Retrieving new data')
        new_price, new_date = page.get_prices(url)

    # Converst prices from str to float
    for line_index, line in enumerate(all_prices):
        for price_index, price in enumerate(line):
            all_prices[line_index][price_index] = float(price)

    # Checks new prices and if its in the prices are the same to file
    if not new_price or new_price == all_prices[-1]:
        print("Drawing")
        draw_graph(all_prices, graph_name, item_date)

    else:
        with open(f'following/{name}.csv', 'a', newline='', encoding='UTF-8') as file:
            writer = csv.writer(file)
            print("Adding new_price to all_prices and updating the file")
            store_price = new_price.copy()  # Make a copy to avoid modifying new_price
            store_price.append(new_date)
            print(store_price)
            writer.writerow(store_price)

        load(name)

def delete(name):
    """Deletes anything that it wants to follow"""
    if os.path.exists(f'following/{name}.csv'):
        os.remove(f'following/{name}.csv')
        print(f'Deleted {name}')
