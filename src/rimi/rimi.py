"""Rimi webpage scraper"""

from bs4 import BeautifulSoup
import requests


BASE_URL = "https://www.rimi.ee"
E_STORE_URL = BASE_URL + "/epood"
# id of the ul element containing the category item
CATEGORY_ID = "desktop_category_menu_"
# 1 indexed (1..19)
CATEGORY_N = 19
# page querry for the category page
PAGE_QUERRY = "?page=1&pageSize=80"


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
