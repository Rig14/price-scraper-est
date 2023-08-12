"""Product helpers"""

from typing import TypedDict


class PricePerUnit(TypedDict):
    """Price per unit helper class"""
    price: int
    unit: str


class Product:
    """Product helper class"""

    def __init__(self, name: str, price: int, price_per_unit: PricePerUnit, category: str):
        self.name = name
        # price that is paid for 1 product
        self.price = price
        # price that is paid for 1 unit of product (e.g. 1kg)
        self.price_per_unit = price_per_unit['price']
        self.unit = price_per_unit['unit']
        self.category = category
        self.weight = price * 100 // self.price_per_unit

    def __str__(self):
        return f"{self.name}"

    def price_string(self):
        """Return price as a string"""
        return f"{self.price}"
