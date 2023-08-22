import os
import helper as hp
import page_retrival as page

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

def main():
    index = GUI()

    if 	index == 1:

        linkLst, itemNames, fileName = hp.user_links()
        priceLst, date = page.get_price_url(linkLst)

        hp.store_graph(linkLst,priceLst,fileName,itemNames,date)
        hp.draw_graph(priceLst,itemNames,date)

    elif index == 2:
        for i in os.listdir():
            if i.endswith(".csv"):
                print(i)
        name = input("Enter name of graph (without .csv): ")

        hp.load(name)


    elif index == 3:
        for i in os.listdir():
            if i.endswith(".csv"):
                print(i)
        name = input("Enter name of graph (without .csv): ")
        hp.delete(name)

if __name__ == '__main__':
    main()