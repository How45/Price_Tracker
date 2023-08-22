import csv
import matplotlib.pyplot as plt
import numpy as np
import page_retrival as page
import os

def list_change(priceLsts):
    return [[i[index] for i in priceLsts] for index in range(len(priceLsts[0]))] # 

def draw_graph(lstPrice,lst,date):
    cl = ["--b.","--r.","--g.","--c.","--m.","--y.","--k."]

    try:
        lstPrice = list_change(lstPrice)
    except TypeError:
        print("Single lst")

    x = np.array(date)
    y = np.array(lstPrice)

    for i in range(len(lstPrice)):
        plt.plot(date,y[i],cl[i], label=lst[i])
    plt.legend()

    while True:
        if plt.waitforbuttonpress():
            break
    plt.close()

def user_links():
	lstLink = []
	titlelst = []

	fileName = input("Enter name of graph: ")
	linkAmount = int(input("Enter amount of items you wanna be tracked (max. 7): "))

	for i in linkAmount:
		url = input("Enter Amazon item URL (page of item you wanna track): ")
		links = url.rsplit("/", 1)[0] # Removes unnecessary extra link lenght (NEED TO DO A CHECK IF ITS ALREADY SHORT)
		lstLink.append(links)

		userName = input("Enter name of Item: ")
		titlelst.append(userName)

	return lstLink,titlelst,fileName

def store_graph(user_links, price, file_name, name, date):
    price_date = price + [date]

    try:
        with open(f'{file_name}.csv', 'x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(user_links)
            writer.writerow(name)
            writer.writerow(price_date)
    except FileExistsError:
        print(f"Error: {file_name}.csv already exists. Returning to the menu.")

def load(name):
    def get_new_price_data(link):
        new_price, new_date = page.getPriceURL(link)
        return new_price + [new_date]

    with open(f'following/{name}.csv', 'r') as file:
        reader = csv.reader(file)
        all_prices, graph_name, link, date = [], [], [], []

        for index, line in enumerate(reader, start=1): # Gets prices off CSV
            if index == 1:
                link = line.copy()
                new_price_data = get_new_price_data(link)
            elif index == 2:
                graph_name = line.copy()
            else:
                temp_price = list(map(float, line[:-1]))
                all_prices.append(temp_price)
                date.append(line[-1])

    if new_price_data == all_prices[-1]: # Draws
        print("Drawing")
        draw_graph(all_prices, graph_name, date)
    else:
        with open(f'{name}.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(new_price_data)
        print("Adding newPrice to all prices and updating the file")
        load(name)


def delete(name):
    if os.path.exists(name+".csv"):
        os.remove(name+".csv")
        print("Deleted "+name)