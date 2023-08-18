from src.selver.selver import SelverProvider


def test_selver_categorys_and_ids():
    """Test selver category ids"""
    selver = SelverProvider()
    ids = selver._category_ids

    assert len(ids) > 0

    for id in ids:
        assert isinstance(id, int)
        assert id > -1
        assert id < 1000


def test_selver_category_getter():
    selver = SelverProvider()
    selver.make_next_request()
    products = selver.get_products()

    assert len(products) > 0

    for product in products:
        assert product['name'] is not None
        assert product['price'] is not None
        assert product['weight'] > 0
        assert product['weight_unit'] in ['kg', 'tk', 'l', 'ml', 'g', 'cl']
        assert product['category'] is not None
        assert product['store_name'] == 'Selver'
        assert product['price_per_unit'] is not None
