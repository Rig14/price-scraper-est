"""Scraper for getting the prices of products from different stores"""

import time
from os.path import exists

from src.util.product import Product
from src.rimi.rimi import get_rimi_products


class PriceScraper():
    """Price scraper class"""
    _CACHE_FILE_NAME = "EstPriceScraper.cache"

    def __init__(self):
        self._cache = True
        self._cache_timeout = 60 * 60 * 24 * 2  # 2 days
        self._available_providers = ["rimi"]
        self._used_providers = self._available_providers

    def set_cache(self, cache: bool, **kwargs):
        """Tweak settings related to caching

        Parameters:
            cache (bool): whether to use cache or not (default: True)
        Kwargs:
            cache_timeout (int): how long to cache the data in seconds (default: 2 days)
        """
        self._cache = cache
        self._cache_timeout = kwargs.get("cache_timeout", self._cache_timeout)

    def set_used_providers(self, providers: list[str]):
        """Set the providers to use (default: all available providers)

        Parameters:
            providers (list[str]): the providers to use
        """
        # check if the providers are available
        for provider in providers:
            if provider not in self._available_providers:
                raise ValueError(f"Provider {provider} is not available")

        self._used_providers = providers

    def get_products(self) -> list[Product]:
        """Return a list of products from a provider

        Parameters:
            provider (str): the provider to use
        """
        products = []
        if self._cache:
            try:
                products = self._get_cached_products()
            except ValueError:
                pass

        if not products:
            for provider in self._used_providers:
                if provider == "rimi":
                    products.extend(get_rimi_products())

            if self._cache:
                self._cache_products(products)

        return products

    def _cache_products(self, products: list[Product]):
        """Cache the products

        Parameters:
            products (list[Product]): the products to cache
        """
        with open(self._CACHE_FILE_NAME, "w", encoding="UTF-8") as file:
            # timestamp on top of the file - unix time in seconds
            file.write(str(int(time.time())) + "\n")
            # used providers
            file.write(" ".join(self._used_providers) + "\n")
            # products
            for product in products:
                file.write(product.get_cache() + "\n")

    def _get_cached_products(self):
        """Return the cached products"""
        products = []

        if not exists(self._CACHE_FILE_NAME):
            raise ValueError("Cache file does not exist")

        with open(self._CACHE_FILE_NAME, "r", encoding="UTF-8") as file:
            timestamp = int(file.readline())
            # check if the cache is too old
            if timestamp + self._cache_timeout < int(time.time()):
                raise ValueError("Cache is too old")
            # used providers
            providers = file.readline()
            # check if the used providers are the same
            if providers != " ".join(self._used_providers):
                raise ValueError("Used providers are not the same")

            # products
            for line in file.readlines():
                product_info = line.split(" ")
                product = Product({
                    "name": product_info[0],
                    "price": float(product_info[1]),
                    "weight": float(product_info[2]),
                    "category": product_info[3],
                    "store": product_info[6]
                }, {
                    "price": float(product_info[4]),
                    "weigth_unit": product_info[5]
                })
                products.append(product)

        return products
