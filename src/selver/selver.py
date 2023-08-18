import os
import requests
import json

from src.util.product import ProductInfo
from src.util.provider import Provider

CATEGORY_API_URL = "https://www.selver.ee/api/catalog/vue_storefront_catalog_et/category/_search"


class SelverProvider(Provider):
    """Selver webpage scraper (initialization makes 1 request)"""

    def __init__(self):
        self._category_ids = self._get_category_ids()

    def make_next_request(self) -> None:
        """Make the next request"""
        pass

    def get_products(self) -> list[ProductInfo] | None:
        """Return the products"""
        pass

    def get_progress(self) -> int:
        """Return the progress"""
        pass

    def set_use_cache(self, use_cache: bool) -> None:
        """Set False if you dont want to use cache (default: True)"""
        pass

    def _get_category_ids(self) -> list[int]:

        with open(os.path.join(os.getcwd(), "src/selver/category_request.json"), "r", encoding="UTF-8") as file:
            request = file.read()
            request = request.replace(" ", "").replace("\n", "")

            response = requests.get(
                CATEGORY_API_URL + "?request=" + request + "&size=4000")
            response = json.loads(response.text)

            ids = [int(category["_source"]["path"].split("/")[-1])
                   for category in response["hits"]["hits"]]

            return ids
