import json
import urllib
from urllib.request import urlopen

import re
import requests
import bs4
import csv
from datetime import datetime


# Cleaners
def change_all_whitespace(x):
    """
    Returns a string with any blank spaces removed.
    """
    try:
        x = x.replace(" ", "+")
    except:
        pass
    return x

##--------------------INPUT/INPUT FORMATTING-----------------------------##

def Searching():
    product_input = input("Enter your product:")
    product_input = change_all_whitespace(product_input)

    ##-------------------Searching for links----------------------------------##

    URL = ("http://www.pricetree.com/search.aspx?q=" + product_input)
    result = bs4.BeautifulSoup(urlopen(URL), 'html.parser')
    li_links = []
    li_id = []

    for link in result.find_all('div', {"class": "items-wrap"}):
        li = link.a['href']
        li_links.append(li)

    # -------------------Searching for key--------------------------------

    if not li_links:
        print('No Data Found')
    else:
        for i in range(len(li_links)):
            k = re.findall(r'(\d+)', li_links[i])
            for i in range(len(k)):
                li_id.append(k[i])

    ##-----------------------Getting Prices--------------------------------##
    if li_id:
        for i in range(1, len(li_id)):
            results = json.load(urlopen("http://www.pricetree.com/dev/api.ashx?pricetreeId=" + li_id[
                i] + "&apikey=7770AD31-382F-4D32-8C36-3743C0271699"))
            li = results['data']
            if len(li) > 0 :
                for i in range(1, len(li)):
                    print("Product Name ::", li[i]['Product_Name'])
                    print("Seller Name  ::", li[i]['Seller_Name'])
                    print("Best Price   ::", li[i]['Best_Price'])
                    print("Link         ::", li[i]['Uri'])

    else:
        print("No Data found")



while True:
    a = input("Enter y/n to continue ::")
    if a=="y":
        Searching()
        continue
    elif a=="n":
        break