"""Apstract provider class for different stores to use"""

from abc import abstractmethod

from src.util.product import ProductInfo


class Provider:
    """Provider abstract class"""

    @abstractmethod
    def make_next_request() -> None:
        """Make the next request"""
        pass

    @abstractmethod
    def get_products(self) -> list[ProductInfo]:
        """Return the products"""
        pass

    @abstractmethod
    def get_progress(self) -> range(100):
        """Return the progress"""
        pass
