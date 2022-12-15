# Lowell Marzan | CIS 345 | 10:30 - 11:45
import csv
import time
import product


class Order:

    def __init__(self, total, creation_time, pickup_time, items=None):
        self._total = total
        self._creation_time = creation_time
        self._pickup_time = pickup_time
        if items is None:
            self._items = []
        else:
            self._items = items

    def add_item(self, new_item):
        with open("product_list.csv", "r") as fp:
            data = csv.reader(fp)
            for prod in data:
                if prod[0] in new_item.name:
                    self._items.append(new_item)
        self._total += new_item.price

    def delete_item(self, item_to_be_deleted):
        for item in self._items:
            if item.name in item_to_be_deleted:
                self._total -= item.price
                self._items.remove(item)

    def set_create_and_pickup_time(self, sec):
        t0 = time.time()
        self._creation_time = time.ctime(t0)
        t1 = t0 + sec
        self._pickup_time = time.ctime(t1)

    def clear_order(self):
        self._creation_time = 0
        self._pickup_time = 0
        self._total = 0
        self._items.clear()

    def __str__(self):
        prods = f"Total: ${self._total:.2f}\n"
        for prod in self._items:
            prods += str(prod) + "\n"
        return prods

    @property
    def creation_time(self):
        return self._creation_time

    @property
    def pickup_time(self):
        return self._pickup_time

    @property
    def items(self):
        return self._items

    @property
    def total(self):
        return self._total

