"""Rimi webpage scraper"""

from bs4 import BeautifulSoup
import requests

from src.util.product import ProductInfo
from src.util.provider import Provider


class RimiProvider(Provider):
    def __init__(self):
        self._products = []
        self._progress = 0
        self._use_cache = True
        self._base_url = "https://www.rimi.ee/"
        self._estore_url = self._base_url + "epood"

    def make_next_request() -> None:
        """Make the next request"""
        pass

    def get_products(self) -> list[ProductInfo]:
        """Return the products"""
        pass

    def get_progress(self) -> int:
        """Return the progress"""
        pass

    def set_use_cache(self, use_cache: bool) -> None:
        """Set False if you dont want to use cache (default: True)"""
        self._use_cache = use_cache

    def _get_category_urls(self) -> list[str]:
        CATEGORY_CLASS_NAME = "category-menu -second-level js-categories-level-container"

        # CATEGORY_CLASS_NAME > ul > li > a
        html = requests.get(self._estore_url, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")

        urls = []
        for category in soup.find_all("div", class_=CATEGORY_CLASS_NAME):
            urls.append(self._base_url +
                        category.find("ul").find("li").find("a").get("href"))

        return urls
