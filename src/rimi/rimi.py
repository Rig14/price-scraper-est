"""Rimi webpage scraper"""

from bs4 import BeautifulSoup
import requests
from src.util.cacher import Cacher

from src.util.product import ProductInfo
from src.util.provider import Provider


class RimiProvider(Provider):
    """Rimi webpage scraper (initialization makes 1 request)"""

    def __init__(self):
        self._products: list[ProductInfo] = []
        self._use_cache = True
        self._cache_file_name = "rimi_cache.cache"
        self._base_url = "https://www.rimi.ee/"
        self._estore_url = self._base_url + "epood"
        self._category_urls = self._get_category_urls()
        self._category_urls_index = 0
        self._page_index = 1

    def make_next_request(self) -> None:
        """Make the next request"""
        products = self._get_products_from_category(
            self._category_urls[self._category_urls_index], self._page_index)

        if products is None:
            self._category_urls_index += 1
            self._page_index = 1
            return

        self._products.extend(products)

    def get_products(self) -> list[ProductInfo] | None:
        """Return the products"""
        if self._products:
            if self._use_cache:
                cache = Cacher(self._cache_file_name)
                cache.cache_products(self._products)
            return self._products
        else:
            cache = Cacher(self._cache_file_name)
            try:
                return cache.get_cached_products()
            except Exception:
                return None

    def get_progress(self) -> int:
        """Return the progress"""
        return self._category_urls_index * 100 // len(self._category_urls)

    def set_use_cache(self, use_cache: bool) -> None:
        """Set False if you dont want to use cache (default: True)"""
        self._use_cache = use_cache

    def _get_category_urls(self) -> list[str]:
        """Get category urls"""
        CATEGORY_CLASS_NAME = "category-menu -second-level js-categories-level-container"

        # CATEGORY_CLASS_NAME > ul > li > a
        html = requests.get(self._estore_url, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")

        urls = []
        for category in soup.find_all("div", class_=CATEGORY_CLASS_NAME):
            urls.append(self._base_url +
                        category.find("ul").find("li").find("a").get("href"))

        return urls

    def _get_products_from_category(self, category_url: str, page: int) -> list[ProductInfo]:
        """Get products from a category"""
        # page querry for the category page
        PAGE_SIZE = 100
        PRODUCT_CONTAINER_CLASS = "card__details"
        PRICE_CONTAINER_CLASS = "price-tag"
        UNIT_PRICE_CLASS = "card__price-per"

        products = []

        html = requests.get(
            category_url + f"?page={page}&pageSize={PAGE_SIZE}", timeout=10).text
        soup = BeautifulSoup(html, "html.parser")
        category = soup.find("h1").text
        product_containers = soup.find_all(
            "div", {"class": PRODUCT_CONTAINER_CLASS})

        if product_containers is None or not product_containers:
            return None

        for product in product_containers:
            name = product.find("p").text

            price_conatiner = product.find(
                "div", {"class": PRICE_CONTAINER_CLASS})

            if price_conatiner is None:
                continue

            # price is in the form of price_main.price_decimal
            price_main = int(price_conatiner.find("span").text)
            price_decimal = int(price_conatiner.find("sup").text)
            price = (price_main * 100 + price_decimal) / 100

            # [price, unit]
            unit_price = product.find(
                "p", {"class": UNIT_PRICE_CLASS}).text.replace(" ", "").replace("\n", "").split("€/")

            price_per_unit = float(unit_price[0].replace(",", "."))
            weight_unit = unit_price[1]

            product: ProductInfo = {
                "name": name,
                "price": price,
                "price_per_unit": price_per_unit,
                "weight_unit": weight_unit,
                "category": category,
                "store_name": "rimi",
                "weight": price / price_per_unit
            }

            products.append(product)

        return products
