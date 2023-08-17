"""Product dictionary layout"""

from typing import TypedDict


class ProductInfo(TypedDict):
    # store that has the product
    store_name: str
    # name of the product
    name: str
    # price of the product
    price: float
    # price per unit of the product e.g. 1.5€/kg
    price_per_unit: float
    # weight of the product
    weight: float
    # weight unit of the product e.g. kg, tk
    weight_unit: str
    # category of the product
    category: str
