import csv
import matplotlib.pyplot as plt
import numpy as np
import page_retrival as page
import os

def listChange(price_list):
    return [[i[index] for i in price_list] for index in range(len(price_list[0]))] #

def drawGraph(price_list,lst,date):
    cl = ["--b.","--r.","--g.","--c.","--m.","--y.","--k."]

    try:
        price_list = listChange(price_list)
    except TypeError:
        print("Single lst")

    x = np.array(date)
    y = np.array(price_list)

    for i in range(len(price_list)):
        plt.plot(date,y[i],cl[i], label=lst[i])
    plt.legend()

    while True:
        if plt.waitforbuttonpress():
            break
    plt.close()

def user_links():
	link_list = []
	title_list = []

	file_name = input("Enter name of graph: ")
	linke_accounts = int(input("Enter amount of items you wanna be tracked (max. 7): "))

	for i in linke_accounts:
		url = input("Enter Amazon item URL (page of item you wanna track): ")
		links = url.rsplit("/", 1)[0] # Removes unnecessary extra link lenght (NEED TO DO A CHECK IF ITS ALREADY SHORT)
		link_list.append(links)

		item_name = input("Enter name of Item: ")
		title_list.append(item_name)

	return link_list,title_list,file_name

def storeGraph(user_links, price, file_name, name, date):
    price_date = price + [date]

    try:
        with open(f'following/{file_name}.csv', 'x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(user_links)
            writer.writerow(name)
            writer.writerow(price_date)
    except FileExistsError:
        print(f"Error: {file_name}.csv already exists. Returning to the menu.")

def load(name):
    file = open(f'following/{name}.csv','r')
    reader = csv.reader(file)

    all_prices,graph_name,link,date = [],[],[],[]
    index = 0

    # Get all info
    for line in reader:
        price = []
        index += 1

        if index == 1: # Links to find new prices
            link = line.copy()
            new_price, new_date = page.getPriceURL(link)

        elif index == 2: # get name always stored on line 2
            graph_name = line.copy()

        else: # line 3 onwards are all the price from old on top to new at the very bottom
            price = line.copy()
            print(price)
            date.append(price[-1])
            price.remove(price[-1])
            all_prices.append(price)

    file.close()

    # Converst prices from str to float
    for i in range(len(all_prices)):
        for k in range(len(all_prices[i])):
            all_prices[i][k] = float(all_prices[i][k])

    # If statment sees if the new_price found online is still the same as the most recent price on the file
    if new_price == all_prices[-1]:
        print("Drawing")
        drawGraph(all_prices,graph_name,date)

    else:
        file = open(f'following/{name}.csv','a')
        writer = csv.writer(file)

        print("add new_price to all price, also update the file")
        store_price = new_price.copy() # Changes name as it becomes new price
        print(store_price)
        store_price.append(new_date)
        print(store_price)

        writer.writerow(store_price)
        file.close()
        load(name)


def delete(name):
    if os.path.exists(f'following/{name}.csv'):
        os.remove(f'following/{name}.csv')
        print(f'Deleted {name}')