"""Scraper for getting the prices of products from different stores"""

import os
from typing import Callable

from src.util.cacher import Cache
from src.rimi.rimi import get_rimi_products


class PriceScraper():
    """Price scraper class"""
    _CACHE_FILE_NAME = "EstPriceScraper.cache"

    def __init__(self):
        self._cache = True
        self._available_providers = ["rimi"]
        self._used_providers = self._available_providers
        # maps provider names to product getter functions
        self._provider_functions_map = {
            "rimi": get_rimi_products
        }

    def set_use_cache(self, cache: bool):
        """Set whether to use cache or not (default: True)

        Parameters:
            cache (bool): whether to use cache or not
        """
        self._cache = cache

    def set_used_providers(self, providers: list[str] | str):
        """Set the providers to use (default: all available providers)

        Parameters:
            providers (list[str]): the providers to use
        """
        # if string converts into list
        if isinstance(providers, str):
            providers = [providers]
        # check if the providers are available
        for provider in providers:
            if provider not in self._available_providers:
                raise ValueError(f"Provider {provider} is not available")

        self._used_providers = providers

    def get_products(self):
        """Get all products from all providers

        Returns:
            list[Product]: the products
        """
        cache = Cache(os.getcwd())
        # check if cache is enabled
        if self._cache:
            # get the cache
            cached_products = cache.get_cache(self._used_providers)
            if cached_products is not None:
                return cached_products

        # get the products by scraping if there is no cache or the cache is invalid
        products = []
        for provider in self._used_providers:
            products.extend(self._provider_functions_map[provider]())
        # cache the products
        if self._cache:
            cache.cache_products(products, self._used_providers)
        return products

    def modify_provider_function_map(self, modifyed_map: dict[str, Callable]):
        """ATTENTION: FOR TESTING PURPOSES ONLY

        Modify the provider-function map

        Parameters:
            modifyed_map (dict[str, function]): the new map
        """
        self._provider_functions_map = modifyed_map
