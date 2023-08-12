"""Rimi webpage scraper"""

from bs4 import BeautifulSoup

base_url = "https://www.rimi.ee/epood"

# id of ul element containing category links


def category_id(n): return f"desktop_category_menu_{n}"


# 1 indexed (1..19)
number_of_categories = 19

# ul[category_id] -> (first)li -> a[href]
