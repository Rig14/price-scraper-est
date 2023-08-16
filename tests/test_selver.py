from src.selver.selver import get_categorys_and_ids


def test_selver_categorys_and_ids():
    """Test selver category ids"""
    cat_and_ids = get_categorys_and_ids()

    for [id, cat] in cat_and_ids:
        assert isinstance(id, int)
        assert id > -1
        assert id < 1000
        assert isinstance(cat, str)
        assert len(cat) > 0
