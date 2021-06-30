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

		# Change this to user entering name	
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

		# Remove this

		title = soup.find_all("span",id="productTitle")[0].get_text()
		title = title.replace("\n","")
 
		if len(title) > 18:
			titlelst.append(title[:19])
		else:
			titlelst.append(title)

	return priceLst


def drawGraph(pricelst,lst):
	x = np.array(lst)
	y = np.array(pricelst)

	plt.plot(x,y, 'ro')
	plt.draw()
	plt.waitforbuttonpress(0)
	plt.close()

def storeGraph(links,price,fileName,name):
	file = open(fileName+".txt","w") # For error Handling (To stop repeating names, change this to x (w = write / x = create))
	
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
				newPrice = getPriceURL(link)
		elif index == 2:
			for word in line.split():
				graphName.append(word)
		else:
			for word in line.split():
				tempPrice.append(word)
			allPrices.append(tempPrice)

	for i in range(len(newPrice)):
		if float(newPrice[i]) == float(allPrices[-1][i]):
			print("Same")
		else:
			print("Add")
		
	file.close()


def delete(name):
	if os.path.exists(name+".txt"):
		os.remove(name+".txt")
		print("Deleted "+name)

def main():
	index = 2 #GUI()

	if 	index == 1:

		fileName = "Phones"
		itemNames = ["Samsung","Phone 2"]
		linkLst = ["https://www.amazon.co.uk/Samsung-Galaxy-Android-Smartphone-Version/dp/B08SMS5WMZ/","https://www.amazon.co.uk/Sim-Free-Unlocked-OUKITEL-6-4Inches-Smartphone-Black/dp/B08RDB89QR/"]
		# linkLst, itemNames, fileName = userLinks()
		priceLst = getPriceURL(linkLst)
		
		storeGraph(linkLst,priceLst,fileName,itemNames)
		drawGraph(priceLst,itemNames)

	elif index == 2:
		for i in os.listdir():
			if i.endswith(".txt"):
				print(i)
		name = "Phones"#name = input("Entre name of graph (without .txt): ")

		load(name)



	elif index == 3:
		for i in os.listdir():
			if i.endswith(".txt"):
				print(i)

		name = input("Entre name of graph (without .txt): ")
		delete(name)

main()

# Load = If New compare if there is a change in pricing if no change dont create new line if some change create new one if all change create new line
