"""Test the rimi module."""

import random
import requests

from src.rimi.rimi import get_category_urls, get_products_from_category_url


CATEGORY_URL_TESTS = 5


def test_category_urls():
    """test if the category urls are correct"""
    category_urls = get_category_urls()

    random.shuffle(category_urls)

    for url in category_urls[:CATEGORY_URL_TESTS]:
        request = requests.get(url, timeout=10)
        assert request.status_code == 200
        assert request.url == url


def test_product_query():
    """test if the query for products is correct"""
    category_urls = get_category_urls()

    random.shuffle(category_urls)

    test_url = category_urls[0]

    products = get_products_from_category_url(test_url)

    for product in products:
        assert product.price > 0
        assert product.price_per_unit > 0
        assert product.unit in ["kg", "l", "tk", "g", "ml", "cl"]
        assert product.weight > 0
        assert product.name != ""
