import os
import helper as hp
import page_retrival as page


def graphic():  # UI graphic of page
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


def main():  # Control of all UI
    index = graphic()

    if index == 1:

        link_list, item_name, file_name = hp.get_links()
        # price_list, date = page.get_prices(link_list)
        price_list = [-1, -1]
        date = ['09/08/23', '09/08/23']
        hp.initialise_data_graph(link_list, price_list, file_name, item_name, date)
        hp.draw_graph(price_list, item_name, date)

    elif index == 2:
        print(os.listdir('following'))
        name = input("Enter name of graph (without .csv): ")

        hp.load(name)
    elif index == 3:
        print(os.listdir('following'))
        name = input("Enter name of graph (without .csv): ")
        hp.delete(name)
    else:
        print('ERROR: No key')


if __name__ == '__main__':
    main()
