"""Apstract provider class for different stores to use"""

from abc import abstractmethod

from src.util.product import ProductInfo


class Provider:
    """Provider abstract class"""

    @abstractmethod
    def make_next_request(self) -> None:
        """Make the next request"""
        pass

    @abstractmethod
    def get_products(self) -> list[ProductInfo] | None:
        """Return the products"""
        pass

    @abstractmethod
    def get_progress(self) -> int:
        """Return the progress"""
        pass

    def set_use_cache(self, use_cache: bool) -> None:
        """Set False if you dont want to use cache (default: True)"""
        pass
