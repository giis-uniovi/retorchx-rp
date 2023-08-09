class Capacity:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def add_quantity(self, number):
        self.quantity = self.quantity + number
