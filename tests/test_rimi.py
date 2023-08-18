"""Test Rimi provider"""

import requests
import re

from src.rimi.rimi import RimiProvider


URL_TESTS = 2


def test_category_urls():
    """Test getting category urls"""
    rimi = RimiProvider()
    category_urls = rimi._category_urls
    for i in range(URL_TESTS):
        assert category_urls[i] is not None
        res = requests.get(category_urls[i])
        assert res.status_code == 200
        url_regex = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
        assert re.match(url_regex, category_urls[i]) is not None


def test_make_next_request():
    """Test making next request"""
    rimi = RimiProvider()

    rimi.make_next_request()
    products = rimi.get_products()
    for product in products:
        assert len(product["name"]) > 2
        assert product["price"] > 0
        assert product["price_per_unit"] > 0
        assert product["weight_unit"] in [
            "kg", "l", "tk", "g", "ml", "cl", "l"]
        assert product["weight"] > 0
        assert product["category"] is not None

    # products from cache
    cache_products = rimi.get_products()
    assert products == cache_products

    rimi.delete_cache()


def test_make_next_request_10():
    """Test making next request 10 times"""
    rimi = RimiProvider()

    for _ in range(10):
        rimi.make_next_request()
        products = rimi.get_products()
        for product in products:
            assert len(product["name"]) > 2
            assert product["price"] > 0
            assert product["price_per_unit"] > 0
            assert product["weight_unit"] in [
                "kg", "l", "tk", "g", "ml", "cl", "l"]
            assert product["weight"] > 0
            assert product["category"] is not None

    # products from cache
    rimi2 = RimiProvider()
    cache_products = rimi2.get_products()
    assert products == cache_products
