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
