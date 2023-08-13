"""Product helpers"""

from typing import TypedDict


class ProductUnitInfo(TypedDict):
    """Price per unit helper class"""
    price: int
    weigth_unit: str


class ProductInfo(TypedDict):
    """Product info helper class"""
    name: str
    price: int
    weight: float
    category: str


class Product:
    """Product helper class"""

    def __init__(self, product_info: ProductInfo, price_per_unit: ProductUnitInfo):
        self.name = product_info["name"]
        self.price = product_info["price"]
        self.weight = product_info["weight"]
        self.category = product_info["category"]

        self.price_per_unit = price_per_unit["price"]
        self.weight_unit = price_per_unit["weigth_unit"]

    def __str__(self):
        return f"{self.name}"

    def get_price(self):
        """Return the price of the product"""
        return f"{self.price}€ ({self.price_per_unit}€/{self.weight_unit})"
