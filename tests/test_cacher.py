import time
from src.util.cacher import Cacher
from src.util.product import ProductInfo

TEST_PRODUCTS: list[ProductInfo] = [
    {
        "store_name": "Rimi",
        "name": "Test product 1",
        "price": 1.0,
        "price_per_unit": 1.0,
        "weight": 1.0,
        "weight_unit": "kg",
        "category": "Test category 1"
    },
    {
        "store_name": "Rimi",
        "name": "Test product 2",
        "price": 2.0,
        "price_per_unit": 2.0,
        "weight": 2.0,
        "weight_unit": "kg",
        "category": "Test category 2"
    }
]


def test_cacher_caching():
    cacher = Cacher("rimi_cache.cache")

    cacher.cache_products(TEST_PRODUCTS)
    cached_products = cacher.get_cached_products()

    assert cached_products == TEST_PRODUCTS

    cacher.delete_cache()


def test_cacher_timeout():
    cacher = Cacher("rimi_cache.cache")

    cacher.cache_products(TEST_PRODUCTS)
    cacher.set_cache_timeout(0)

    time.sleep(1)

    try:
        cacher.get_cached_products()
        assert False
    except Exception:
        assert True

    cacher.delete_cache()


def test_2_caches():
    cacher1 = Cacher("rimi_cache.cache")
    cacher2 = Cacher("rimi_cache2.cache")

    cacher1.cache_products(TEST_PRODUCTS)

    try:
        cacher2.get_cached_products()
        assert False
    except Exception:
        assert True

    cacher1.delete_cache()
    cacher2.delete_cache()
