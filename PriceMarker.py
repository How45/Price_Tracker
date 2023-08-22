from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import numpy as np
import os
import datetime
import csv
import websitePrice as web

def GUI():
	print("""
		  ___  ____   __   ____  _  _     ___  __   _  _  ____   __   ____  ____
		 / __)(  _ \ / _\ (  _ \/ )( \   / __)/  \ ( \/ )(  _ \ / _\ (  _ \(  __)
		( (_ \ )   //    \ ) __/) __ (  ( (__(  O )/ \/ \ ) __//    \ )   / ) _)
		 \___/(__\_)\_/\_/(__)  \_)(_/   \___)\__/ \_)(_/(__)  \_/\_/(__\_)(____)

		1. Create New Graph
		2. Load Graph
		3. Delete Graph
		""")
	user = int(input(": "))
	return user

def userLinks():
	lstLink = []
	titlelst = []

	fileName = input("Enter name of graph: ")
	linkAmount = int(input("Enter amount of items you wanna be tracked (max. 7): "))

	for i in range(linkAmount):
		url = input("Enter Amazon item URL (page of item you wanna track): ")
		
		if url[12] == "a":
			links = url.rsplit("/", 1)[0] # Removes unnecessary extra link lenght (NEED TO DO A CHECK IF ITS ALREADY SHORT)
			lstLink.append(links)
		else:
			lstLink.append(url)
		

		userName = input("Enter name of Item: ")
		titlelst.append(userName)

	return lstLink,titlelst,fileName

def getPriceURL(lst):
	priceLst = []

	for i in lst:
		page = requests.get(i, headers={'User-Agent':'Mozilla/2.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'})

		if str(page.status_code) != "200": # If page not found
			print("This wont work, its the {0} URL you have entered".format(i))
			main()

		soup = BeautifulSoup(page.content, 'html.parser')
		
		price = web.webPrice(soup)

		elif soup.find_all("span",id="priceblock_saleprice")[0].get_text() != None:
			price = soup.find_all("span",id="priceblock_saleprice")[0].get_text()

		else:
			price = soup.find_all("span",id="priceblock_dealprice")[0].get_text()
			
		priceLst.append(float(price[1:]))

		getDate = datetime.datetime.now()
		dates = getDate.strftime("%x")

	return priceLst,dates

def listChange(priceLsts):
	tempPrice = []
	index = 0
	for j in range(len(priceLsts[0])):
		temp = [] 
		for i in priceLsts:
			for k in i:
				if k == i[index]:
					temp.append(k)
					break
		tempPrice.append(temp)
		index += 1

	priceLsts = tempPrice
	return priceLsts

def drawGraph(lstPrice,lst,date):
	cl = ["--b.","--r.","--g.","--c.","--m.","--y.","--k."]

	try:
		lstPrice = listChange(lstPrice)
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

def storeGraph(userLinks,price,filesName,name,date):
	priceDate = price.copy()
	priceDate.append(date)

	file = open(filesName+".csv","x",newline='') # For error Handling (if error go back to menu)
	# If error do return
	writer = csv.writer(file)

	writer.writerow(userLinks)
	writer.writerow(name)
	writer.writerow(priceDate)
	file.close()

def load(name):
	file = open(name+".csv","r")
	reader = csv.reader(file)

	allPrices = []
	graphName = []
	link = []
	date = []
	index = 0

	# Get all info   
	for line in reader:
		tempPrice = []
		index += 1

		if index == 1: # Links to find new prices
			link = line.copy()
			newPrice, newDate = getPriceURL(link)

		elif index == 2:# get name always stored on line 2
			graphName = line.copy()

		else:# line 3 onwards are all the price from old on top to new at the very bottom
			tempPrice = line.copy() # price,price,...,date

			date.append(tempPrice[-1]) # Gets the date 
			tempPrice.remove(tempPrice[-1]) # removes the date
			allPrices.append(tempPrice) # prices 
				
	file.close()

	# Converst prices from str to float
	for i in range(len(allPrices)):
		for k in range(len(allPrices[i])):
			allPrices[i][k] = float(allPrices[i][k])

	# If statment sees if the newPrice found online is still the same as the most recent price on the file
	if newPrice == allPrices[-1]:
		print("Drawing")
		drawGraph(allPrices,graphName,date)

	else:
		file = open(name+".csv","a",newline='')
		writer = csv.writer(file)

		print("add newPrice to all price, also update the file")
		newPrice.append(newDate)
		writer.writerow(newPrice)
		file.close()

		load(name)

def delete(name):
	if os.path.exists(name+".csv"):
		os.remove(name+".csv")
		print("Deleted "+name)

def main():
	index = GUI()

	if 	index == 1:

		linkLst, itemNames, fileName = userLinks()
		priceLst, date = getPriceURL(linkLst)

		storeGraph(linkLst,priceLst,fileName,itemNames,date)
		drawGraph(priceLst,itemNames,date)

	elif index == 2:
		for i in os.listdir():
			if i.endswith(".csv"):
				print(i)
		name = input("Enter name of graph (without .csv): ")

		load(name)


	elif index == 3:
		for i in os.listdir():
			if i.endswith(".csv"):
				print(i)
		name = input("Enter name of graph (without .csv): ")
		delete(name)

main()
# Note - Fix name space, when someone adds a space between names replace that with a dash 
