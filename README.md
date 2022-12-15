# README

#### Context

Organ Stop Pizza is a local pizza restaurant in Mesa, Arizona. They offer 
pizzas, pastas, appetizers, sandwiches, beer, wine, and more. 
They also have live music all day which is played by local musicians. 
While there is a certain charm to this type of restaurant, 
they fall behind in that they do not have the ability to create 
online orders for pickup on their website. This app addresses that problem.

## Install Required Libraries

Install PILLOW and Pytest using the Python Packages tab in PyCharm

## Running the Program

Click the green run button in the top right corner of PyCharm 

or run the following command in the terminal:

```shell
$ python main.py
```

Refer to the `accounts.json` file for accounts to use or create your own using the GUI

## Functionality

### Log In Screen

Log into the application using a username and a password. This information may be found
in the `accounts.json` file. The following example shows information that
is included in an account:

Username: "lmarzan", Password: "90mart", Name: "Lowe Marzan", Email: "lmarzan@asu.edu"

### Account Creation Screen

A new user may create a new account via the Account Creation Screen. The user
must simply fill out a form with the following information: Username, Full Name,
Email, Password, and Confirmed Password.

A user may not create an account if:
* The username already exists in `accounts.json`
* The Password does not match Confirmed Password

After successful account creation, the form will be cleared and the new account
will appear in `accounts.json` and the user may log in with those new credentials.

After unsuccessful account creation, the form will still be cleared and feedback
will be displayed explaining why the account could not be created.

### Order Creation

After successful log in, the user will be greeted with the category select screen.
The user may select from Pizza, Pasta, Sandwich, and Drinks. From there the user may
choose which category to go to and can add different food items to their shopping cart.
After a user adds an item to their cart, the total cost will be updated, 
and it will be added to their order.

At any point, the user may go to the shopping cart and view all the items they added
to their cart and checkout whenever they'd like. The user may also select a time for pickup
(from ASAP (10-15 mins) to 2 hours after checkout time).

### Remove Item From Cart

A user can delete any item from their cart by selecting it from their shopping
cart and hitting the "Delete Item" button. The shopping cart and total cost will
be updated appropriately.

### Exit Button

From any screen, a user may exit the application.

## Data Files

### accounts.json

This contains info related to accounts in the following format:

```json
{"lmarzan": {"Password": "90mart", "Name":  "Lowe Marzan", "Email": "lmarzan@asu.edu"}}
```

### orders.csv

This contains order information in the following format:

| Username | Name        | Create Time | Pickup Time | Items           | Total  |
|----------|-------------|-------------|-------------|-----------------|--------|
| lmarzan  | Lowe Marzan |Sat Nov 26 17:28:10 2022 |Sat Nov 26 17:43:10 2022             | (List of items) | 40.13 |

### product_list.csv

This contains product information in the following format:

| Product Name    | Category |
|-----------------|----------|
| The Combination | Pizza    |
| ...             | ...      |

## Classes

### Product Class

#### Variables

The product class has the following instance variables:
1. name: private, String
2. category: private, String
3. size: private, String
4. price: private, float
5. name getter
6. name setter
7. category getter
8. category setter
9. size getter 
10. size setter
11. price getter
12. price setter

#### Methods

* dunder \__init\__
* dunder \__str\__

### Order Class

#### Variables
 
The order class has the following instance variables:
1. total: private, double
2. creation_time: private, String
3. pickup_time: private, String
4. items: private, List
5. total getter
6. creation_time getter
7. pickup_time getter
8. items getter

#### Methods

* dunder \__init\__
* dunder \__str\__
* add_item
* delete_item
* set_create_and_pickup_time
* clear_order

## Auto Testing

Run the following commands to test the `test_product_and_order.py` file:

```shell
$ pip install pytest
$ pytest -v
```

