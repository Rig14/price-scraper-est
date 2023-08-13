import os
import random
import time
from src.util.cacher import Cache
from src.util.product import Product

TEST_PRODUCTS = [
    Product({"name": "test", "price": 1, "weight": 1, "category": "test", "store": "test"}, {
        "price": 1, "weigth_unit": "test"}),
    Product({"name": "test22233", "price": 2, "weight": 1223, "category": "test", "store": "test"}, {
        "price": 22, "weigth_unit": "kg"})]


def test_cache():
    """Test the cache integrity"""

    current_dir = os.getcwd()
    cache = Cache(current_dir)

    # cache products
    cache.cache_products(TEST_PRODUCTS, ["test"])

    # get the products back from the cache
    cached_products = cache.get_cache(["test"])
    # test if they are the same
    for i in range(len(TEST_PRODUCTS)):
        prod = TEST_PRODUCTS[i]
        cached_prod = cached_products[i]

        assert prod.name == cached_prod.name
        assert prod.price == cached_prod.price
        assert prod.weight == cached_prod.weight
        assert prod.category == cached_prod.category
        assert prod.price_per_unit == cached_prod.price_per_unit
        assert prod.weight_unit == cached_prod.weight_unit
        assert prod.store == cached_prod.store

    # remove the cache file
    cache.delete_cache()


def test_cache_timeout():
    """Test the cache timeout"""
    timeout = random.randint(2, 10)

    current_dir = os.getcwd()
    cache = Cache(current_dir)
    # change the timeout
    cache.set_cache_timeout(timeout)

    # cache products
    cache.cache_products(TEST_PRODUCTS, ["test"])

    # wait for the cache to timeout
    time.sleep(timeout+1)

    # get the products back from the cache
    cached_products = cache.get_cache(["test"])
    # test if the cache is invalid
    assert cached_products == None

    # remove the cache file
    cache.delete_cache()


def test_cache_providers():
    """Test the cache if providers are changed"""
    current_dir = os.getcwd()
    cache = Cache(current_dir)

    # cache products
    cache.cache_products(TEST_PRODUCTS, ["test"])

    # get the products back from the cache with different providers
    cached_products = cache.get_cache(["test", "test2"])
    # test if the cache is invalid
    assert cached_products == None

    # remove the cache file
    cache.delete_cache()
