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
		links = url.rsplit("/", 1)[0]
		lstLink.append(links)

		userName = input("Entre name of Item: ")
		titlelst.append(userName)

	return lstLink,titlelst,fileName

def getPriceURL(lst):
	priceLst = []
	titlelst = []

	for i in lst:
		page = requests.get(i, headers={'User-Agent':'Mozilla/2.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'})

		if str(page.status_code) != "200":
			print("This wont work, its the {0} URL you have entreed".format(i))
			main()

		soup = BeautifulSoup(page.content, 'html.parser')

		price = soup.find_all("span",id="priceblock_ourprice")[0].get_text() # Will have to change this for all type of ID types FUCK AMAZON!

		priceLst.append(float(price[1:]))

		# Remove this V no need for title, use can create its own title

		# title = soup.find_all("span",id="productTitle")[0].get_text()
		# title = title.replace("\n","")

		# if len(title) > 18:
		# 	titlelst.append(title[:19])
		# else:
		# 	titlelst.append(title)

	return priceLst


def drawGraph(pricelst,lst):
	x = np.array(lst)
	y = np.array(pricelst)

	for i in y:
		print(x,i)
		if (i == y[-1]).all():
			plt.plot(x,i, "b")
		else:
			plt.plot(x,i, "r.")
	plt.draw()
	while True:
		if plt.waitforbuttonpress():
			break
	plt.close()

def storeGraph(links,price,fileName,name):
	file = open(fileName+".txt","x") # For error Handling (if error go back to menu)

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
	# Get all info 1) Links to find new prices 2) get name always stored on line 2 3) line 3 onwards are all the price from old on top to new at the very bottom
	for line in file:
		tempPrice = []
		index += 1

		if index == 1:
			for word in line.split():
				link.append(word)
				# newPrice = getPriceURL(link)
				newPrice = [243.0, 439.99]
		elif index == 2:
			for word in line.split():
				graphName.append(word)
		else:
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
		drawGraph(priceLst,itemNames)# See if this still works??!

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
