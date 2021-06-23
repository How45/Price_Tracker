from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import numpy as np

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

	linkAmount = 2 #int(input("Entre amount of items you wanna be tracked: "))
	groupName = input("Entre name for this graph: ")

	for i in range(linkAmount):
		url = input("Entre Amazon item URL (page of item you wanna track): ")
		links = url.rsplit("/", 1)[0]
		lstLink.append(links)

	return lstLink,groupName

def getPriceURL(lst):
	priceLst = []
	titlelst = []

	for i in lst:
		page = requests.get(i, headers={'User-Agent':'Mozilla/2.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'})

		if str(page.status_code) != "200":
			print("This wont work, its the {0} URL you have entreed".format(i))
			main()

		soup = BeautifulSoup(page.content, 'html.parser')

		price = soup.find_all("span",id="priceblock_ourprice")[0].get_text()

		priceLst.append(float(price[1:]))

		title = soup.find_all("span",id="productTitle")[0].get_text()
		title = title.replace("\n","")

		if len(title) > 18:
			titlelst.append(title[:19])
		else:
			titlelst.append(title)

	return priceLst,titlelst

def drawGraph(pricelst,lst):
	x = np.array(lst)
	y = np.array(pricelst)

	plt.plot(x,y, 'ro')
	plt.draw()
	plt.waitforbuttonpress(0)
	plt.close()

def storeGraph(name,objects,price):
	print(":")


def main():
	index = 1 #GUI()

	if 	index == 1:
		groupName = "Test"
		linkLst = ["https://www.amazon.co.uk/Samsung-Galaxy-Android-Smartphone-Version/dp/B08SMS5WMZ/","https://www.amazon.co.uk/Sim-Free-Unlocked-OUKITEL-6-4Inches-Smartphone-Black/dp/B08RDB89QR/"]
		#linkLst, groupName = userLinks()
		priceLst,title = getPriceURL(linkLst)
		drawGraph(priceLst,title)
		#storeGraph(groupName,linkLst,priceLst)
		print("test For git")

main()
