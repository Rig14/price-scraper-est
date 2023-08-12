class RimiProduct:
    def __init__(self, name, price_per_product, price_per_unit, unit):
        self.name = name
        # price if you buy 1 product
        self.price_per_produt = price_per_product
        # price if you buy 1 unit (e.g. 1kg)
        self.price_per_unit = price_per_unit
        self.unit = unit
