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
