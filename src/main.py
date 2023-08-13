from src.rimi.rimi import get_rimi_products
import time

from src.util.product import Product


class PriceScraper():
    def __init__(self):
        self._cache = True
        self._cache_timeout = 60 * 60 * 24 * 2  # 2 days
        self._available_providers = ["rimi"]

    def set_cache(self, cache: bool, **kwargs):
        """Tweak settings related to caching

        Parameters:
            cache (bool): whether to use cache or not (default: True)
        Kwargs:
            cache_timeout (int): how long to cache the data in seconds (default: 2 days)
        """
        self._cache = cache
        self._cache_timeout = kwargs.get("cache_timeout", self._cache_timeout)

    def get_products(self, provider) -> list[Product]:
        """Return a list of products from a provider

        Parameters:
            provider (str): the provider to use
        """
        # check if the provider is valid
        if provider not in self._available_providers:
            raise ValueError(f"Provider {provider} is not available")

        if provider == "rimi":
            return get_rimi_products()
