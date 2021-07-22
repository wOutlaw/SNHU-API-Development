"""
Warren Outlaw
Final Project
CS-340-Q5079

Main module for the stock API application.
"""

import stocks_api as api
import etc

menu_items = ["Create", "Read", "Update", "Delete", "Industry List",
              "50-Day SMA Range", "Outstanding Shares", "Exit"]

def input_number(prompt):
    while True:
        try:
            num = int(raw_input(prompt))
            break
        except:
            pass
    
    return num


def display_menu(options):
    for i in range(len(options)):
        print "{:d}. {:s}".format(i+1, options[i])
    
    choice = 0
    while not 0 < choice < len(options)+1:
        choice = input_number("Please choose a menu item: ")
        
    return choice


def main():
    print "-" * 50
    print "Stock Market Summary Data API"
    print "Version: 1.0"
    print "-" * 50
    
    while True:
        choice = display_menu(menu_items)

        if choice == 1:
            ticker = str(raw_input("Ticker symbol: "))
            result = api.create_stock(ticker)
            print result

        if choice == 2:
            ticker = str(raw_input("Ticker symbol: "))
            result = api.get_stock(ticker)
            print result
            
        if choice == 3:
            ticker = str(raw_input("Ticker symbol: "))
            key = str(raw_input("Key to update: "))
            value = int(raw_input("Value: "))
            result = api.update_stock(ticker, key, value)
            print result

        if choice == 4:
            ticker = str(raw_input("Ticker symbol: "))
            result = api.delete_stock(ticker)
            print result

        if choice == 5:
            industry = str(raw_input("Industry: "))
            result = etc.industry_list(industry)
            print result
            
        if choice == 6:
            low = int(raw_input("Low value: "))
            high = int(raw_input("High value: "))
            result = etc.sma(low, high)
            print result
            
        if choice == 7:
            sector = str(raw_input("Sector: "))
            result = api.portfolio(sector)
            print result
        
        if choice == 8:
            break


if __name__ == '__main__':
    main()