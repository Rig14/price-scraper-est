"""Rimi webpage scraper"""

from bs4 import BeautifulSoup
import requests

from ..util.product import Product, ProductInfo, ProductUnitInfo


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
PAGE_SIZE = 80
PRODUCT_CONTAINER_CLASS = "card__details"
PRICE_CONTAINER_CLASS = "price-tag"
UNIT_PRICE_CLASS = "card__price-per"


def get_products_from_category_url(category_url, page):
    """Return a list of products from a category url"""
    products = []

    html = requests.get(
        category_url + f"?page={page}&pageSize={PAGE_SIZE}", timeout=10).text
    soup = BeautifulSoup(html, "html.parser")
    category = soup.find("h1").text
    product_containers = soup.find_all(
        "div", {"class": PRODUCT_CONTAINER_CLASS})

    if product_containers is None or not product_containers:
        return products

    for product in product_containers:
        name = product.find("p").text

        price_conatiner = product.find(
            "div", {"class": PRICE_CONTAINER_CLASS})

        if price_conatiner is None:
            continue

        # price is in the form of price_main.price_decimal
        price_main = int(price_conatiner.find("span").text)
        price_decimal = int(price_conatiner.find("sup").text)
        price = (price_main * 100 + price_decimal) / 100

        # [price, unit]
        unit_price = product.find(
            "p", {"class": UNIT_PRICE_CLASS}).text.replace(" ", "").replace("\n", "").split("€/")

        price_per_unit = float(unit_price[0].replace(",", "."))
        weight_unit = unit_price[1]

        product_unit_info: ProductUnitInfo = {
            "price": price_per_unit, "weigth_unit": weight_unit}

        product_info: ProductInfo = {"name": name, "price": price,
                                     "weight": round(price / price_per_unit, 3 if weight_unit != "tk" else 0), "category": category, "store": "rimi"}

        products.append(Product(product_info, product_unit_info))

    return products


def get_all_products_from_category(category_url):
    """Return a list of all products from a category url"""
    products = []
    page = 1
    while True:
        page_products = get_products_from_category_url(category_url, page)
        if len(page_products) == 0:
            break
        products.extend(page_products)
        page += 1
    return products


def get_rimi_products():
    """Return a list of all products from all categories"""
    products = []
    category_urls = get_category_urls()
    for category_url in category_urls:
        products.extend(get_all_products_from_category(category_url))
    return products
