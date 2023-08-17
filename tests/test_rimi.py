"""Test Rimi provider"""

import requests
from src.rimi.rimi import RimiProvider


URL_TESTS = 2


def test_category_urls():
    """Test getting category urls"""
    rimi = RimiProvider()
    category_urls = rimi._get_category_urls()
    for i in range(URL_TESTS):
        assert category_urls[i] is not None
        res = requests.get(category_urls[i])
        assert res.status_code == 200
