import re

import requests
from bs4 import BeautifulSoup as BS

product = 'AMD Ryzen 5 Cezanne'

r = requests.get("https://ek.ua/ek-list.php?search_={0}".format(product))
html = BS(r.content, "html.parser")

price_list = []


# Get price from text
def get_price(price_text):
    price_text_list = price_text.split()
    price_text_no_spaces = ''.join(price_text_list)
    return int(re.search(r"\d+", price_text_no_spaces).group(0))


# Print list with ', '
def print_list(list_print):
    for i in list_print:
        print(i, end=', ')


def search_link(html_search_link):
    for elem in html_search_link.select(".model-short-info"):
        href = elem.select('a')
        return href[0].get("href")


def search_link_button(html_search_link_button):
    for elem in html_search_link_button.select(".main-part-content > .desc-menu"):
        href = elem.select('a')
        return href[0].get("link")


print(search_link(html))
r2 = requests.get("https://ek.ua{0}".format(search_link(html)))
html2 = BS(r2.content, "html.parser")
print(search_link_button(html2))
r3 = requests.get("https://ek.ua{0}".format(search_link_button(html2)))
html3 = BS(r3.content, "html.parser")

for el in html3.select(".tr-odd"):
    price = el.select(".where-buy-price")
    price_list.append(get_price(price[0].text))

price_list.sort()
print_list(price_list)
