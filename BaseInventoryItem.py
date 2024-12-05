# Absraction: Define abstract base class for a generic inventory item
class InventoryItem:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def add_stock(self, amount):
        raise NotImplementedError

    def remove_stock(self, amount):
        raise NotImplementedError

    def __str__(self):
        return f'(self.name): (self quantity)'
