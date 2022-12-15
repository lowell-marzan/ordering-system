# Lowell Marzan | CIS 345 | 10:30 - 11:45

class Product:

    def __init__(self, name, category, size=""):
        self._name = name
        self._category = category
        if size != "":
            self._size = size
        else:
            self._size = "Regular"
        if self._category == "Drinks" and self._size == "Small - $2.25":
            self._price = 2.25
        elif self._category == "Drinks" and self._size == "Large - $2.50":
            self._price = 2.50
        elif self._category == "Sandwiches":
            self._price = 8.39
        elif self._name == "Spaghetti with Tomato Sauce - $8.79":
            self._price = 8.79
        elif self._name == "Spaghetti with Meatballs – $11.89":
            self._price = 11.89
        elif self._name == "Lasagna (Sausage and Beef) - $12.89":
            self._price = 12.89
        elif self._category == "Pizza":
            if self._size == "8 in.":
                self._price = 12.59
            elif self._size == "12 in.":
                self._price = 22.29
            elif self._size == "12 in. (Gluten Free)":
                self._price = 25.79
            elif self._size == "14 in.":
                self._price = 25.99
        else:
            self._price = 0.0

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_cat):
        self._category = new_cat

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, new_size):
        self._size = new_size

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        self._price = new_price

    def __str__(self):
        return f"{self._name:<20} | {self._size:<10} | ${self._price:<6.2f}"

