"""Rimi webpage scraper"""

from bs4 import BeautifulSoup
import requests

from ..util.product import Product


BASE_URL = "https://www.rimi.ee"
E_STORE_URL = BASE_URL + "/epood"
# id of the ul element containing the category item
CATEGORY_ID = "desktop_category_menu_"
# 1 indexed (1..19)
CATEGORY_N = 19


def get_category_urls():
    """Return a list of category urls"""
    category_urls = []
    html = requests.get(E_STORE_URL, timeout=10).text
    soup = BeautifulSoup(html, "html.parser")

    # ul[category_id] -> (first)li -> a[href]
    for index in range(1, CATEGORY_N+1):
        ul_element = soup.find("ul", {"id": CATEGORY_ID + str(index)})
        li_element = ul_element.find("li")
        link = li_element.find("a")
        category_urls.append(BASE_URL + link["href"])
    return category_urls


# page querry for the category page
PAGE_QUERRY = "?page=1&pageSize=80"
PRODUCT_CONTAINER_CLASS = "card__details"
PRICE_CONTAINER_CLASS = "price-tag"
UNIT_PRICE_CLASS = "card__price-per"


def get_products_from_category_url(category_url):
    """Return a list of products from a category url"""
    products = []

    html = requests.get(category_url, timeout=10).text
    soup = BeautifulSoup(html, "html.parser")
    category = soup.find("h1").text
    product_conatiners = soup.find_all(
        "div", {"class": PRODUCT_CONTAINER_CLASS})

    for product in product_conatiners:
        name = product.find("p").text

        price_conatiner = product.find(
            "div", {"class": PRICE_CONTAINER_CLASS})

        price_main = int(price_conatiner.find("span").text)
        price_decimal = int(price_conatiner.find("sup").text)
        price = (price_main * 100 + price_decimal) / 100

        unit_price = product.find(
            "p", {"class": UNIT_PRICE_CLASS}).text.replace(" ", "").replace("\n", "").split("€/")

        products.append(
            Product(name, price, {"price": float(unit_price[0].replace(",", ".")), "unit": unit_price[1]}, category))

    return products
