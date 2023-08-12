"""Test the rimi module."""

import random
import requests

from src.rimi.rimi import get_category_urls


CATEGORY_URL_TESTS = 5


def test_category_urls():
    """test if the category urls are correct"""
    category_urls = get_category_urls()

    random.shuffle(category_urls)

    for url in category_urls[:CATEGORY_URL_TESTS]:
        request = requests.get(url, timeout=10)
        assert request.status_code == 200
        assert request.url == url
