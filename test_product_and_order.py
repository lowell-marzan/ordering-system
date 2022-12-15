# Lowell Marzan | CIS 345 | 10:30 - 11:45

from product import *
from order import *


class TestProduct:

    def test_details(self):
        p = Product("P.S.M", "Pizza", "14 in.")
        p2 = Product("Ink", "Dessert", "")
        print("Testing details: Product")
        assert("P.S.M", "Pizza", "14 in.", 25.99) == (p.name, p.category, p.size, p.price)
        assert("Ink", "Dessert", "Regular", 0) == (p2.name, p2.category, p2.size, p2.price)


class TestOrder:

    def test_details(self):
        o = Order(25.99, time.ctime(), time.ctime(), [])
        assert(25.99, time.ctime(), time.ctime(), []) == (o.total, o.creation_time, o.pickup_time, o.items)
