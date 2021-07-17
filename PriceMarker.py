from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import numpy as np
import os


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

	fileName = input("Entre name of graph: ")
	linkAmount = int(input("Entre amount of items you wanna be tracked: "))

	for i in range(linkAmount):
		url = input("Entre Amazon item URL (page of item you wanna track): ")
		links = url.rsplit("/", 1)[0] # Removes unnecessary extra link lenght 
		lstLink.append(links)

		userName = input("Entre name of Item: ")
		titlelst.append(userName)

	return lstLink,titlelst,fileName

def getPriceURL(lst):
	priceLst = []
	titlelst = []

	for i in lst:
		page = requests.get(i, headers={'User-Agent':'Mozilla/2.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'})

		if str(page.status_code) != "200": # If page not found
			print("This wont work, its the {0} URL you have entreed".format(i))
			main()

		soup = BeautifulSoup(page.content, 'html.parser')

		try:
			price = soup.find_all("span",id="priceblock_ourprice")[0].get_text()
		except IndexError:
			price = soup.find_all("span",id="priceblock_saleprice")[0].get_text()


		priceLst.append(float(price[1:]))

	return priceLst

def listChange(pricelst):
	tempPrice = []
	index = 0
	for j in range(len(pricelst[0])):
		temp = [] 
		for i in pricelst:
			for k in i:
				if k == i[index]:
					temp.append(k)
					break
		tempPrice.append(temp)
		index += 1

	pricelst = tempPrice
	return pricelst

def drawGraph(pricelst,lst):
	tst = [0,1,2,3,4,5]
	cl = ["--b.","--r.","--g."]

	try:
		pricelst = listChange(pricelst)
	except TypeError:
		print("Single lst")
		
	x = np.array(lst) 
	y = np.array(pricelst)

	for i in range(len(pricelst)):
		plt.plot(tst,y[i],cl[i], label = 'i')
	plt.draw()

	while True:
		if plt.waitforbuttonpress():
			break
	plt.close()

def storeGraph(links,price,fileName,name):
	file = open(fileName+".txt","x") # For error Handling (if error go back to menu)
	# If error do return

	for i in links:
		file.write(i+" ")
	file.write("\n")

	for i in name:
		file.write(i+" ")
	file.write("\n")

	for i in price:
		file.write(str(i)+" ")
	file.close()

def load(name):
	file = open(name+".txt","r")

	allPrices = []
	graphName = []
	link = []
	index = 0

	# Get all info   
	for line in file:
		tempPrice = []
		index += 1

		if index == 1:# Links to find new prices
			for word in line.split():
				link.append(word)
				newPrice = getPriceURL(link)
		elif index == 2:# get name always stored on line 2
			for word in line.split():
				graphName.append(word)
		else:# line 3 onwards are all the price from old on top to new at the very bottom
			for word in line.split():
				tempPrice.append(word)
			allPrices.append(tempPrice)
	file.close()

	# Check if there is any new prices (V this for loop changes prices on file into float)
	for i in range(0,len(allPrices)):
		for k in range(0,len(allPrices[i])):
			allPrices[i][k] = float(allPrices[i][k])

	# If statment sees if the newPrice found online is still the same as the most recent price on the file
	if newPrice == allPrices[-1]:
		print("Drawing")
		drawGraph(allPrices,graphName)

	else:
		file = open(name+".txt","a")
		print("add newPrice to all price, also update the file")

		storePrice = newPrice
		for i in range(0,len(storePrice)):
			storePrice[i] = str(storePrice[i])

		file.write("\n")
		for i in storePrice:
			file.write(i+" ")
		file.close()
		load(name)


def delete(name):
	if os.path.exists(name+".txt"):
		os.remove(name+".txt")
		print("Deleted "+name)

def main():
	index = GUI()

	if 	index == 1:

		linkLst, itemNames, fileName = userLinks()
		priceLst = getPriceURL(linkLst)

		storeGraph(linkLst,priceLst,fileName,itemNames)
		drawGraph(priceLst,itemNames)

	elif index == 2:
		for i in os.listdir():
			if i.endswith(".txt"):
				print(i)
		name = input("Entre name of graph (without .txt): ")

		load(name)


	elif index == 3:
		for i in os.listdir():
			if i.endswith(".txt"):
				print(i)

		name = input("Entre name of graph (without .txt): ")
		delete(name)

main()
# Note - Fix name space