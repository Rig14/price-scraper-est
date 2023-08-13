import random
from src.main import PriceScraper
from src.rimi.rimi import get_category_urls, get_products_from_category_url


def test_scraper_cache_rimi():
    """Test PriceScraper cache functionality using rimi api"""
    scraper = PriceScraper()

    # modify provider-function map to make a small request to the server
    # will query 1 full category
    urls = get_category_urls()
    random.shuffle(urls)
    def test(): return get_products_from_category_url(urls[0], 1)
    scraper.modify_provider_function_map(
        {"rimi": test})

    products = scraper.get_products()

    products_from_cache = scraper.get_products()

    counter = 0
    for product in products:
        for cached_product in products_from_cache:
            if product.name == cached_product.name:
                counter += 1
                break

    assert counter == len(products)
    assert counter == len(products_from_cache)
