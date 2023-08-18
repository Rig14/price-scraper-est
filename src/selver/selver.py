import os
import requests
import json

from src.util.product import ProductInfo
from src.util.provider import Provider
from src.util.cacher import Cacher

CATEGORY_API_URL = "https://www.selver.ee/api/catalog/vue_storefront_catalog_et/category/_search"
PRODUCT_API_URL = "https://www.selver.ee/api/catalog/vue_storefront_catalog_et/product/_search"


class SelverProvider(Provider):
    """Selver webpage scraper (initialization makes 1 request)"""

    def __init__(self):
        self._category_ids = self._get_category_ids()
        self._category_ids_index = 0
        self._products = []
        self._use_cache = True
        self._cache_file_name = "selver_cache.cache"

    def make_next_request(self) -> None:
        """Make the next request"""
        ID_INCREMENTS = 10
        ids = self._category_ids[self._category_ids_index:self._category_ids_index + ID_INCREMENTS if self._category_ids_index + ID_INCREMENTS < len(
            self._category_ids) else len(self._category_ids)]

        self._products.extend(self._get_products_from_categorys(ids))

        self._category_ids_index += ID_INCREMENTS if self._category_ids_index + ID_INCREMENTS < len(
            self._category_ids) else len(self._category_ids)

    def get_products(self) -> list[ProductInfo] | None:
        """Return the products"""
        if self._products:
            if self._use_cache:
                cache = Cacher(self._cache_file_name)
                cache.cache_products(self._products)
            return self._products
        else:
            cache = Cacher(self._cache_file_name)
            try:
                return cache.get_cached_products()
            except Exception:
                return None

    def get_progress(self) -> int:
        """Return the progress"""
        return self._category_ids_index * 100 // len(self._category_ids)

    def set_use_cache(self, use_cache: bool) -> None:
        """Set False if you dont want to use cache (default: True)"""
        self._use_cache = use_cache

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

    def _get_products_from_categorys(self, category_ids: list[int]) -> list[ProductInfo]:
        with open(os.path.join(os.getcwd(), "src/selver/product_request.json"), "r", encoding="UTF-8") as file:
            request = file.read()
            request = json.loads(request)

            request["query"]["bool"]["filter"]["bool"]["must"][2]["terms"]["category_ids"] = category_ids

            request = str(request).replace("\'", '"')

            response = requests.get(
                PRODUCT_API_URL + "?request=" + request + "&size=4000")
            response = json.loads(response.text)
            products = []

            for product in response["hits"]["hits"]:

                prdt = ProductInfo()
                prdt["name"] = product["_source"]["name"]
                prdt["price"] = product["_source"]["final_price_incl_tax"]
                prdt["store_name"] = "Selver"
                prdt["category"] = product["_source"]["category"][0]["name"]
                volume = product["_source"]["product_volume"]
                prdt["weight"] = float(volume.split(" ")[0].replace(",", ".")) if volume.split(
                    " ")[0].replace(",", "", 1).isdigit() else 1
                prdt["weight_unit"] = volume.split(" ")[-1].lower()
                prdt["price_per_unit"] = product["_source"]["unit_price"]

                products.append(prdt)

            return products
