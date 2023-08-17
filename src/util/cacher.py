"""Cacher class for caching products to a file"""

import json
import os
import time

from src.util.product import ProductInfo


class Cacher:
    """Cache file structure:
    (1) timestamp
    (2..) products
    """

    def __init__(self, cache_file_name: str):
        self._cache_dir = os.getcwd() + "./EstPriceScraperCache"
        self._cache_file = os.path.join(self._cache_dir, cache_file_name)
        self._cache_timeout = 60 * 60 * 24 * 2  # 2 days

        self._create_cache_dir_if_not_exists()

    def _create_cache_dir_if_not_exists(self) -> None:
        """Create cache dir if it does not exist"""
        if not os.path.exists(self._cache_dir):
            os.makedirs(self._cache_dir)

    def set_cache_timeout(self, timeout: int) -> None:
        """Set cache timeout in seconds (default: 2 days)"""
        self._cache_timeout = timeout

    def get_cached_products(self) -> list[ProductInfo]:
        """Return cached products"""
        with open(self._cache_file, "r", encoding="UTF-8") as cache_file:
            timestamp = int(cache_file.readline().strip())
            if timestamp + self._cache_timeout > int(time.time()):
                raise Exception("Cache timeout")

            products: list[ProductInfo] = []
            for line in cache_file.readlines():
                products.append(json.loads(line.strip()))
            return products

    def cache_products(self, products: list[ProductInfo]) -> None:
        """Cache products to a file"""
        with open(self._cache_file, "w", encoding="UTF-8") as cache_file:
            # timestamp
            cache_file.writeline(str(int(time.time())) + "\n")
            # products
            for product in products:
                cache_file.writeline(json.dumps(product) + "\n")
