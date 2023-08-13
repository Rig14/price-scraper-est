"""Cache the products to a file and get the cached products from the file.
Can be validated by timestamp and providers.
Cache file format:
    timestamp
    providers
    products
"""

import os
import time
from src.util.product import Product


class Cache:
    """Cache class"""

    def __init__(self, cache_dir):
        self._cache_dir = cache_dir
        self._cache_file_name = ".EstPriceScraper.cache"
        self._cache_timeout = 60 * 60 * 24 * 2  # 2 days

    def cache_products(self, products: list[Product], providers: list[str]):
        """Cache the products

        Parameters:
            products (list[Product]): the products to cache
            providers (list[str]): the providers of the products
        """
        with open(os.path.join(self._cache_dir, self._cache_file_name), "w", encoding="UTF-8") as file:
            # timestamp
            file.write(f"{int(time.time())}\n")
            # providers
            file.write(f"{'|'.join(providers)}\n")
            # products
            for product in products:
                file.write(f"{product.get_cacheable()}\n")

    def get_cache(self, providers: list[str]):
        """Get the cache
        Parameters:
            providers (list[str]): the providers of the products, used to check if the cache is still valid (when the providers change the cache is invalid)
        Returns:
            list[Product] | None: the cached products or None if there is no cache
        """
        if not os.path.exists(os.path.join(self._cache_dir, self._cache_file_name)):
            return None

        with open(os.path.join(self._cache_dir, self._cache_file_name), "r", encoding="UTF-8") as file:
            # timestamp
            timestamp = int(file.readline().strip())
            # check if the cache is still valid
            if int(time.time()) > timestamp + self._cache_timeout:
                return None

            # providers
            cache_providers = file.readline().strip().split("|")
            # check if the providers are the same
            for provider in providers:
                if provider not in cache_providers:
                    return None

            # products
            products = []
            for line in file.readlines():
                products.append(Product.convert_cache_to_product(line.strip()))

            return products

    def set_cache_timeout(self, timeout: int):
        """Set the cache timeout (default: 2 days)

        Parameters:
            timeout (int): the timeout in seconds
        """
        self._cache_timeout = timeout

    def delete_cache(self):
        """Delete the cache file"""
        if os.path.exists(os.path.join(self._cache_dir, self._cache_file_name)):
            os.remove(os.path.join(self._cache_dir, self._cache_file_name))
