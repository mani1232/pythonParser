import re

import requests
from bs4 import BeautifulSoup as BS

print('---------')
print('Enter model for search:')
product = input()
print('Enter sort type:')
print('(True - sorts the list in the descending order')
print('(False - sorts the list in the ascending order')


# Check true or false
def sort_type_check():
    while True:
        user_answer = input().lower().strip()
        if user_answer == "true":
            return True
        elif user_answer == "false":
            return False
        else:
            print("Error: Answer must be True or False")


sort_type = sort_type_check()


# Get price from text
def get_price(price_text):
    price_text_list = price_text.split()
    price_text_no_spaces = ''.join(price_text_list)
    return int(re.search(r"\d+", price_text_no_spaces).group(0))


# Print list of prices with ', ' and sorted
def print_list_prices(html_prices):
    price_list = []
    for el in html_prices.select(".tr-odd"):
        price = el.select(".where-buy-price")
        price_list.append(get_price(price[0].text))
    for i in price_list:
        print(i, end=', ')
    price_list.sort(reverse=sort_type)


# Search link product on ek
def search_link_product(link_product):
    for elem in link_product.select(".model-short-info"):
        href = elem.select('a')
        return href[0].get("href")


# Search link for prices on ek
def search_link_for_prices(link_for_prices):
    for elem in link_for_prices.select(".main-part-content > .desc-menu"):
        href = elem.select('a')
        return href[0].get("link")


# Search link
r = requests.get("https://ek.ua/ek-list.php?search_={0}".format(product))
html = BS(r.content, "html.parser")
print('Search link')
print(r.url)

# Product link
r = requests.get("https://ek.ua{0}".format(search_link_product(html)))
html = BS(r.content, "html.parser")
print('Product link')
print(r.url)

# Prices link
r = requests.get("https://ek.ua{0}".format(search_link_for_prices(html)))
html = BS(r.content, "html.parser")
print('Prices link')
print(r.url)

# Print all sorted prices
print_list_prices(html)
