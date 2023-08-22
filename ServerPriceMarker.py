from bs4 import BeautifulSoup
import requests
import os
import datetime
import csv
import time

def getPriceURL(lst):
	priceLst = []

	for i in lst:
		page = requests.get(i, headers={'User-Agent':'Mozilla/2.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'})

		if str(page.status_code) != "200": # If page not found
			print("This wont work, its the {0} URL you have entered".format(i))
			main()

		soup = BeautifulSoup(page.content, 'html.parser')

		if soup.find_all("span",id="priceblock_ourprice")[0].get_text() != None:
			price = soup.find_all("span",id="priceblock_ourprice")[0].get_text()

		elif soup.find_all("span",id="priceblock_saleprice")[0].get_text() != None:
			price = soup.find_all("span",id="priceblock_saleprice")[0].get_text()

		elif soup.find_all("span",id="priceblock_dealprice")[0].get_text() != None:
			price = soup.find_all("span",id="priceblock_dealprice").get_text()

		elif soup.find_all("span",class_="a-size-base a-color-price")[0].get_text() != None:
			price = soup.find_all("span",class_="a-size-base a-color-price")[0].get_text()

		else:
			print("There is an ID you need to add")
			
		priceLst.append(float(price[1:]))

		getDate = datetime.datetime.now()
		dates = getDate.strftime("%x")

	return priceLst,dates

def load(name):
	file = open(name,"r")
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
			tempPrice = line.copy()

			date.append(tempPrice[-1])
			tempPrice.remove(tempPrice[-1])
			allPrices.append(tempPrice)
				
	file.close()

	# Converst prices from str to float
	for i in range(len(allPrices)):
		for k in range(len(allPrices[i])):
			allPrices[i][k] = float(allPrices[i][k])

	# If statment sees if the newPrice found online is still the same as the most recent price on the file
	if newPrice == allPrices[-1]:
		return

	else:
		file = open(name,"a")
		writer = csv.writer(file)

		print("add newPrice to all price, also update the file")
		storePrice = newPrice.copy() # Changes name as it becomes new price
		storePrice.append(newDate)

		writer.writerow(storePrice)
		file.close()
		load(name)

def main():
	print("New Check")
	for i in os.listdir():
		if i.endswith(".csv"):
			print(i)
			load(i)
	print("Sleeping")

	time.sleep(1)
	main()

main()