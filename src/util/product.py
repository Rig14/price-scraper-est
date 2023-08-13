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
    store: str


class Product:
    """Product helper class"""

    def __init__(self, product_info: ProductInfo, price_per_unit: ProductUnitInfo):
        self.name = product_info["name"]
        self.price = product_info["price"]
        self.weight = product_info["weight"]
        self.category = product_info["category"]

        self.price_per_unit = price_per_unit["price"]
        self.weight_unit = price_per_unit["weigth_unit"]
        self.store = product_info["store"]

    def get_cacheable(self):
        """Get the cacheable version of the product"""
        return f"{self.name}|{self.price}|{self.weight}|{self.category}|{self.price_per_unit}|{self.weight_unit}|{self.store}"

    @staticmethod
    def convert_cache_to_product(cache: str):
        """Convert a cache string to a product"""
        cache = cache.split("|")
        return Product(
            {
                "name": cache[0],
                "price": float(cache[1]),
                "weight": float(cache[2]),
                "category": cache[3],
                "store": cache[6]
            },
            {
                "price": float(cache[4]),
                "weigth_unit": cache[5]
            }
        )
