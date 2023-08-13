"""Test the rimi module."""

import random
import requests

from src.rimi.rimi import get_all_products_from_category, get_category_urls, get_products_from_category_url


CATEGORY_URL_TESTS = 2


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

    products = get_products_from_category_url(test_url, 1)

    for product in products:
        assert product.name != "" or None
        assert product.price != 0 or None
        assert product.weight != 0 or None
        assert product.category != "" or None
        assert product.price_per_unit != 0 or None
        assert product.weight_unit in ["kg", "g", "l", "ml", "tk"]


def test_full_category_query():
    """test if a full category can be queried"""
    category_urls = get_category_urls()

    random.shuffle(category_urls)

    test_url = category_urls[0]

    products = get_all_products_from_category(test_url)

    assert products != [] or None

    for product in products:
        assert product.name != "" or None
        assert product.price != 0 or None
        assert product.weight != 0 or None
        assert product.category != "" or None
        assert product.price_per_unit != 0 or None
        assert product.weight_unit in ["kg", "g", "l", "ml", "tk"]
