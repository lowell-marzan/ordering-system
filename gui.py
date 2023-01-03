# Lowell Marzan | CIS 345 | 10:30 - 11:45

import json
import mysql.connector
import os
import pprint
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from order import *
from product import *


def insert_test_doc():
    collection = order_db.test
    test_document = {
        "user": "lmarzan",
        "type": "test"
    }
    inserted_id =  collection.insert_one(test_document).inserted_id
    print(inserted_id)

def insert_into_db(user, name, create, pickup, items, cost):
    collection = order_db.orders
    doc = {
        "Username": user,
        "Customer Name": name,
        "Create Time": create,
        "Pickup Time": pickup,
        "Items": items,
        "Total Price": cost
    }
    inserted_id = collection.insert_one(doc).inserted_id
    print(f"The new document's ID is: {inserted_id}")

def close():
    window.destroy()


def open_gui():
    window.mainloop()


def signin():
    global first_name, user
    user = username.get()
    password = passwd.get()
    if user not in accounts.keys():
        signin_feedback.set("Invalid Username or Password. Please Try Again.")
    else:
        if user in accounts.keys() and accounts[user]["Password"] == password:
            first_name = accounts[user]["Name"].split(" ")[0]
            total.set(f"Hello {first_name}, your total is ${orders.total:.2f}")
            sign_in.grid_forget()
            cat_select.grid(columnspan=3)
        else:
            signin_feedback.set("Invalid Username or Password. Please Try Again.")
    username.set("")
    passwd.set("")


def goto_create_acc():
    username.set("")
    passwd.set("")
    sign_in.grid_forget()
    acc_create.grid(columnspan=3)


def create_acc():
    global user
    user = username.get()
    entered_email = email_entry.get()
    entered_fullname = fullname.get()
    password = passwd.get()
    confirmed_password = confirm_passwd.get()
    blank_flag = False

    if user in accounts.keys():
        acc_create_feedback.set("Username already in use. Please create another one")
    if user == "" or password == "" or entered_email == "" or entered_fullname == "" or entered_email == "":
        acc_create_feedback.set("One or more fields missing information.")
        blank_flag = True
    if password != confirmed_password:
        acc_create_feedback.set("Passwords do not match.")
    if user not in accounts.keys() and password == confirmed_password and not blank_flag:
        accounts.update({user: {"Password": password, "Name": entered_fullname, "Email": entered_email}})
        with open("accounts.json", "w") as file_pointer:
            json.dump(accounts, file_pointer)
        acc_create_feedback.set("Account successfully created. Log in with your new credentials")

    username.set("")
    passwd.set("")
    email.set("")
    confirm_passwd.set("")
    fullname.set("")


def to_signin():
    username.set("")
    passwd.set("")
    email.set("")
    confirm_passwd.set("")
    fullname.set("")
    acc_create.grid_forget()
    sign_in.grid(columnspan=3)


def view_cart():
    cat_select.grid_forget()
    shopping_cart.grid(columnspan=3)
    cart.delete(0, END)
    for food in orders.items:
        cart.insert(END, str(food))


def checkout():
    """
    Gets the current time and sets the order's create time and
    pickup time. Also adds the order to orders.csv.
    Will give feedback to the customer and clear the order class
    :return: void
    """
    if orders.items:
        p_u_time = checkout_time_dropdown.get()
        sec = 60
        if p_u_time == "in 15 mins":
            sec *= 15
        elif p_u_time == "in 30 mins":
            sec *= 30
        elif p_u_time == "in 45 mins":
            sec *= 45
        elif p_u_time == "in 1 hour":
            sec *= 60
        elif p_u_time == "in 1 hr 15 mins":
            sec *= 75
        elif p_u_time == "in 1 hr 30 mins":
            sec *= 90
        elif p_u_time == "in 1 hr 45 mins":
            sec *= 105
        elif p_u_time == "in 2 hours":
            sec *= 120
        orders.set_create_and_pickup_time(sec)
        total.set(f"Thank you {first_name}! Your total is ${orders.total:.2f}. \nWe will have your order ready by "
                  f"{orders.pickup_time.split(' ')[3]}")
        order_to_csv = []
        for key in accounts:
            if key == user:
                items_list = []
                for food in orders.items:
                    items_list.append(str(food) + " ")
                order_to_csv = [user, accounts[user]["Name"], orders.creation_time, orders.pickup_time,
                                items_list, orders.total]
        with open("orders.csv", "a") as file_pointer:
            data = csv.writer(file_pointer)
            data.writerow(order_to_csv)

        # Insert into MongoDB collection
        insert_into_db(user, accounts[user]["Name"], orders.creation_time, orders.pickup_time, items_list, orders.total)

        for food in orders.items:
            cart2.insert(END, str(food))
        orders.clear_order()
        shopping_cart.grid_forget()
        finish_screen.grid(columnspan=3)


def to_pizza_menu():
    cat_select.grid_forget()
    pizza_menu.grid(columnspan=3)


def logout():
    cat_select.grid_forget()
    sign_in.grid(columnspan=3)


def pizza_submit():
    global orders
    new_pizza = Product(pizza_dropdown.get(), "Pizza", sizes_dropdown.get())
    orders.add_item(new_pizza)
    total.set(f"Hello {first_name}, your total is ${orders.total:.2f}")


def from_pizza_to_cat():
    pizza_menu.grid_forget()
    cat_select.grid(columnspan=3)


def to_pasta_menu():
    cat_select.grid_forget()
    pasta_menu.grid(columnspan=3)


def pasta_submit():
    global orders
    new_pasta = Product(pasta_dropdown.get(), "Pasta")
    orders.add_item(new_pasta)
    total.set(f"Hello {first_name}, your total is ${orders.total:.2f}")


def from_pasta_to_cat():
    pasta_menu.grid_forget()
    cat_select.grid(columnspan=3)


def to_sandwich_menu():
    cat_select.grid_forget()
    sandwich_menu.grid(columnspan=3)


def sandwich_submit():
    global orders
    new_sandwich = Product(sandwiches_dropdown.get(), "Sandwiches")
    orders.add_item(new_sandwich)
    total.set(f"Hello {first_name}, your total is ${orders.total:.2f}")


def from_sandwich_to_cat():
    sandwich_menu.grid_forget()
    cat_select.grid(columnspan=3)


def to_drink_menu():
    cat_select.grid_forget()
    drink_menu.grid(columnspan=3)


def drink_submit():
    global orders
    new_drink = Product(drinks_dropdown.get(), "Drinks", drink_sizes_dropdown.get())
    orders.add_item(new_drink)
    total.set(f"Hello {first_name}, your total is ${orders.total:.2f}")


def from_drink_to_cat():
    drink_menu.grid_forget()
    cat_select.grid(columnspan=3)


def from_cart_to_cat():
    shopping_cart.grid_forget()
    cat_select.grid(columnspan=3)


def from_cart_to_signin():
    cart2.delete(0, END)
    finish_screen.grid_forget()
    sign_in.grid(columnspan=3)


def delete_item():
    global orders
    selected_boxes = cart.curselection()

    for selected in selected_boxes[::-1]:
        orders.delete_item(cart.get(selected))
        cart.delete(selected)

    total.set(f"Hello {first_name}, your total is ${orders.total:.2f}")


# Variables

orders = Order(0, 0, 0)
with open("accounts.json", "r") as file_pointer:
    accounts = json.load(file_pointer)

first_name = ""
user = ""

helv18 = ("Helvetica", 18)
helv16 = ("Helvetica", 16)
helv12 = ("Helvetica", 12)

# MongoDB connection

load_dotenv(find_dotenv())

db_password = os.environ.get("MONGODB_PWD")

connection_string = f"mongodb+srv://admin:{db_password}@orders.wxqmah1.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(connection_string)
order_db = client.orders
collections = order_db.list_collection_names()
print(collections)

# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     passwd="root"
# )

# cursor = db.cursor()

# cursor.execute("CREATE TABLE orders ()")

# insert_test_doc()



window = Tk()

window.title("Organ Stop Pizza Online Ordering System")
window.geometry("750x750")
window.columnconfigure(0, weight=1)  # content displayed in the center
window.config(bg="#33BFFF")

signin_feedback = StringVar()
signin_feedback.set("Welcome, Please Sign In")
acc_create_feedback = StringVar()
acc_create_feedback.set("Enter Info to Make a New Account:")
username = StringVar()
email = StringVar()
passwd = StringVar()
confirm_passwd = StringVar()
fullname = StringVar()
fullname.set("")
total = StringVar()
total.set(f"Hello {first_name}, your total so far is $0")

##### Sign-in Screen

sign_in = Frame(window, bg="#94ACB7", width=350, height=200, borderwidth=5, relief=RIDGE)

greeting = Label(window, text="Welcome to Organ Stop Pizza", width=30, bg="#33BFFF", fg="#F3F3f3", font=helv18)
greeting.grid(row=0, columnspan=3)

# Picture and resizing
logo = Image.open("osp.jpg")
new_width = 300
new_height = 150
img = logo.resize((new_width, new_height), Image.LANCZOS)
img.save('osp.png')
logo = ImageTk.PhotoImage(img)
logo_label = Label(window, image=logo)
logo_label.image = logo
logo_label.grid(columnspan=3, column=0, row=1, pady=10)

username_lbl = Label(sign_in, text="Username: ", width=20, font=helv16, fg="#F3F3F3", bg="#94ACB7")
username_lbl.grid(row=1, column=0)
name_entry = Entry(sign_in, textvariable=username, width=20)
name_entry.grid(row=1, column=1)

passwd_lbl = Label(sign_in, text="Password: ", width=20, font=helv16, fg="#F3F3F3", bg="#94ACB7")
passwd_lbl.grid(row=2, column=0)
passwd_entry = Entry(sign_in, textvariable=passwd, width=20, show="*")
passwd_entry.grid(row=2, column=1)

signin_feedback_lbl = Label(sign_in, textvariable=signin_feedback, width=50, font=helv16, fg="#F3F3F3", bg="#94ACB7")
signin_feedback_lbl.grid(row=0, column=0, columnspan=3)

signin_btn = Button(sign_in, command=signin, font=helv12, text='Sign In', width=15)
signin_btn.grid(row=4, column=0, pady=20)

create_acc_btn = Button(sign_in, command=goto_create_acc, font=helv12, text='Create Account', width=15)
create_acc_btn.grid(row=4, column=1, pady=20)

exit_button = Button(window, command=close, font=helv12, text='Exit App', width=15)
exit_button.grid(column=0, row=2, pady=10)

sign_in.grid(columnspan=3)

##### Account Creation

acc_create = Frame(window, bg="#94ACB7", width=350, height=200, borderwidth=5, relief=RIDGE)

acc_create_feedback_lbl = Label(acc_create, textvariable=acc_create_feedback, width=50, font=helv16, fg="#F3F3F3",
                                bg="#94ACB7")
acc_create_feedback_lbl.grid(row=0, column=0, columnspan=3)

username_lbl2 = Label(acc_create, text="Username: ", width=20, font=helv16, fg="#F3F3F3", bg="#94ACB7")
username_lbl2.grid(row=1, column=0)
name_entry2 = Entry(acc_create, textvariable=username, width=20)
name_entry2.grid(row=1, column=1, padx=(0, 10))

email_lbl = Label(acc_create, text="Email: ", width=20, font=helv16, fg="#F3F3F3", bg="#94ACB7")
email_lbl.grid(row=2, column=0)
email_entry = Entry(acc_create, textvariable=email, width=20)
email_entry.grid(row=2, column=1, padx=(0, 10))

name_lbl = Label(acc_create, text="Full Name: ", width=20, font=helv16, fg="#F3F3F3", bg="#94ACB7")
name_lbl.grid(row=3, column=0)
full_name_entry = Entry(acc_create, textvariable=fullname, width=20)
full_name_entry.grid(row=3, column=1, padx=(0, 10))

passwd_lbl = Label(acc_create, text="Password: ", width=20, font=helv16, fg="#F3F3F3", bg="#94ACB7")
passwd_lbl.grid(row=4, column=0)
passwd_entry = Entry(acc_create, textvariable=passwd, width=20, show="*")
passwd_entry.grid(row=4, column=1, padx=(0, 10))
confirm_passwd_lbl = Label(acc_create, text="Confirm Password: ", width=20, font=helv16, fg="#F3F3F3", bg="#94ACB7")
confirm_passwd_lbl.grid(row=5, column=0)
confirm_passwd_entry = Entry(acc_create, textvariable=confirm_passwd, width=20, show="*")
confirm_passwd_entry.grid(row=5, column=1, padx=(0, 10))

acc_create_btn = Button(acc_create, command=create_acc, font=helv12, text='Create Account', width=20)
acc_create_btn.grid(row=6, column=0, pady=10, columnspan=3)

back_to_signin = Button(acc_create, command=to_signin, font=helv12, text='Back to Login Screen', width=20)
back_to_signin.grid(column=0, row=10, pady=10, columnspan=3)

##### Category Select

cat_select = Frame(window, bg="#94ACB7", width=350, height=200, borderwidth=5, relief=RIDGE)

total_label = Label(cat_select, textvariable=total, width=30, font=helv18, fg="#F3F3F3", bg="#94ACB7")
total_label.grid(row=1, column=0, columnspan=3, pady=10)

info = Label(cat_select, text="Select the Category", width=35, bg="#94ACB7", fg="#F3F3f3",
             font=helv16)
info.grid(row=2, columnspan=3)

cat_menu = Frame(cat_select, bg="#94ACB7", width=200, height=140, borderwidth=5, relief=RIDGE)
cat_menu.grid(row=4, column=0, columnspan=3)
cat_menu.grid_propagate(False)
cat_menu.columnconfigure(0, weight=1)
cat_menu.columnconfigure(1, weight=1)

to_pizza = Button(cat_menu, command=to_pizza_menu, font=helv12, text='Pizzas', width=30)
to_pizza.grid(row=0, column=0)
to_pastas = Button(cat_menu, command=to_pasta_menu, font=helv12, text='Pastas', width=30)
to_pastas.grid(row=1, column=0)
to_sandwiches = Button(cat_menu, command=to_sandwich_menu, font=helv12, text='Sandwiches', width=30)
to_sandwiches.grid(row=2, column=0)
to_drinks = Button(cat_menu, command=to_drink_menu, font=helv12, text='Drinks', width=30)
to_drinks.grid(row=3, column=0)

view_shopping_cart = Button(cat_select, command=view_cart, font=helv12, text="View Cart", width=15)
view_shopping_cart.grid(column=0, row=9, pady=10, columnspan=3)

logout_button = Button(cat_select, command=logout, font=helv12, text='Log Out', width=15)
logout_button.grid(column=0, row=10, pady=10, columnspan=3)

##### Pizza Menu

pizza_menu = Frame(window, bg="#94ACB7", width=350, height=200, borderwidth=5, relief=RIDGE)

total_label = Label(pizza_menu, textvariable=total, width=30, font=helv18, fg="#F3F3F3", bg="#94ACB7")
total_label.grid(row=0, column=0, columnspan=3, pady=10)

pizza_label = Label(pizza_menu, text="Pizzas", width=35, bg="#94ACB7", fg="#F3F3f3",
                    font=helv16)
pizza_label.grid(row=1, column=0)

pizzas = ["The Combination", "Hawaiian", "P.S.M.", "Spicy Italian", "Vegetarian"]
pizza_dropdown = ttk.Combobox(pizza_menu, values=pizzas, width=40, state="readonly")
pizza_dropdown.grid(row=2, column=0)
pizza_dropdown.current(0)

sizes_lbl = Label(pizza_menu, text="Sizes", width=35, bg="#94ACB7", fg="#F3F3f3", font=helv16)
sizes_lbl.grid(row=3, column=0)
sizes = ["8 in.", "12 in.", "12 in. (Gluten Free)", "14 in."]
sizes_dropdown = ttk.Combobox(pizza_menu, values=sizes, width=40, state="readonly")
sizes_dropdown.grid(row=4, column=0)
sizes_dropdown.current(0)

pizza_submit = Button(pizza_menu, command=pizza_submit, font=helv12, text='Add Order', width=15)
pizza_submit.grid(row=5, pady=20)

from_pizza_to_cat_btn = Button(pizza_menu, command=from_pizza_to_cat, font=helv12, text='Back to Categories', width=15)
from_pizza_to_cat_btn.grid(row=6, pady=(0, 20))

##### Pastas

pasta_menu = Frame(window, bg="#94ACB7", width=350, height=200, borderwidth=5, relief=RIDGE)

total_label = Label(pasta_menu, textvariable=total, width=30, font=helv18, fg="#F3F3F3", bg="#94ACB7")
total_label.grid(row=0, column=0, columnspan=3, pady=10)

pasta_label = Label(pasta_menu, text="Pastas", width=35, bg="#94ACB7", fg="#F3F3f3",
                    font=helv16)
pasta_label.grid(row=1, column=0)
pastas = ["Spaghetti with Tomato Sauce - $8.79", "Spaghetti with Meatballs – $11.89",
          "Lasagna (Sausage and Beef) - $12.89"]
pasta_dropdown = ttk.Combobox(pasta_menu, values=pastas, width=40, state="readonly")
pasta_dropdown.grid(row=2, column=0)
pasta_dropdown.current(0)

pasta_submit = Button(pasta_menu, command=pasta_submit, font=helv12, text='Add Order', width=15)
pasta_submit.grid(row=3, pady=20)

from_pasta_to_cat_btn = Button(pasta_menu, command=from_pasta_to_cat, font=helv12, text='Back to Categories', width=15)
from_pasta_to_cat_btn.grid(row=4, pady=(0, 20))


##### Sandwiches

sandwich_menu = Frame(window, bg="#94ACB7", width=350, height=200, borderwidth=5, relief=RIDGE)

total_label = Label(sandwich_menu, textvariable=total, width=30, font=helv18, fg="#F3F3F3", bg="#94ACB7")
total_label.grid(row=0, column=0, columnspan=3, pady=10)

sandwich_label = Label(sandwich_menu, text="Sandwiches", width=35, bg="#94ACB7", fg="#F3F3f3", font=helv16)
sandwich_label.grid(row=1, column=0)
sandwiches = ["Ham - $8.39", "Turkey - $8.39", "Roast Beef - $8.39"]
sandwiches_dropdown = ttk.Combobox(sandwich_menu, values=sandwiches, width=40, state="readonly")
sandwiches_dropdown.grid(row=2, column=0)
sandwiches_dropdown.current(0)

sandwich_submit = Button(sandwich_menu, command=sandwich_submit, font=helv12, text='Add Order', width=15)
sandwich_submit.grid(row=3, pady=20)

from_sandwich_to_cat_btn = Button(sandwich_menu, command=from_sandwich_to_cat, font=helv12, text='Back to Categories',
                                  width=15)
from_sandwich_to_cat_btn.grid(row=4, pady=(0, 20))


##### Drinks

drink_menu = Frame(window, bg="#94ACB7", width=350, height=200, borderwidth=5, relief=RIDGE)

total_label = Label(drink_menu, textvariable=total, width=30, font=helv18, fg="#F3F3F3", bg="#94ACB7")
total_label.grid(row=0, column=0, columnspan=3, pady=10)

drink_label = Label(drink_menu, text="Drinks", width=35, bg="#94ACB7", fg="#F3F3f3",
                    font=helv16)
drink_label.grid(row=1, column=0)

drinks = ["Pepsi", "Diet Pepsi", "Root Beer", "Sierra Mist", "Dr. Pepper", "Mountain Dew", "Iced Tea", "Lemonade",
          "Fruit Punch"]
drinks_dropdown = ttk.Combobox(drink_menu, values=drinks, width=40, state="readonly")
drinks_dropdown.grid(row=2, column=0)
drinks_dropdown.current(0)

drink_sizes_lbl = Label(drink_menu, text="Sizes", width=35, bg="#94ACB7", fg="#F3F3f3", font=helv16)
drink_sizes_lbl.grid(row=3, column=0)
drink_sizes = ["Small - $2.25", "Large - $2.50"]
drink_sizes_dropdown = ttk.Combobox(drink_menu, values=drink_sizes, width=40, state="readonly")
drink_sizes_dropdown.grid(row=4, column=0)
drink_sizes_dropdown.current(0)

drink_submit = Button(drink_menu, command=drink_submit, font=helv12, text='Add Order', width=15)
drink_submit.grid(row=5, pady=20)

from_drink_to_cat_btn = Button(drink_menu, command=from_drink_to_cat, font=helv12, text='Back to Categories', width=15)
from_drink_to_cat_btn.grid(row=6, pady=(0, 20))


##### Shopping Cart

shopping_cart = Frame(window, bg="#94ACB7", width=350, height=200, borderwidth=5, relief=RIDGE)

total_label = Label(shopping_cart, textvariable=total, width=40, font=helv18, fg="#F3F3F3", bg="#94ACB7")
total_label.grid(row=0, column=0, columnspan=3, pady=10)

checkout_time_lbl = Label(shopping_cart, text="I'd like to pick up my order...", font=helv12, fg="#F3F3F3",
                          bg="#94ACB7")
checkout_time_lbl.grid(row=1, column=0, pady=10, padx=(20, 0))

checkout_times = ["in 15 mins", "in 30 mins", "in 45 mins", "in 1 hour", "in 1 hr 15 mins", "in 1 hr 30 mins",
                  "in 1 hr 45 mins", "in 2 hours"]
checkout_time_dropdown = ttk.Combobox(shopping_cart, values=checkout_times, width=20, state="readonly")
checkout_time_dropdown.grid(row=1, column=1)
checkout_time_dropdown.current(0)

cart = Listbox(shopping_cart, width=60)
cart.grid(row=2, column=0, columnspan=3)

delete_btn = Button(shopping_cart, command=delete_item, font=helv12, text='Delete Item', width=15)
delete_btn.grid(row=3, column=0, pady=(20, 0), columnspan=3)

checkout_btn = Button(shopping_cart, command=checkout, font=helv12, text="Check Out", width=15)
checkout_btn.grid(row=4, column=0, pady=10, columnspan=3)

from_del_to_cat_btn = Button(shopping_cart, command=from_cart_to_cat, font=helv12, text='Back to Categories', width=15)
from_del_to_cat_btn.grid(row=6, pady=(0, 20), columnspan=3)

##### Finish Screen

finish_screen = Frame(window, bg="#94ACB7", width=350, height=200, borderwidth=5, relief=RIDGE)

total_label = Label(finish_screen, textvariable=total, width=40, font=helv18, fg="#F3F3F3", bg="#94ACB7")
total_label.grid(row=0, column=0, columnspan=3, pady=10)

cart2 = Listbox(finish_screen, width=60)
cart2.grid(row=1, column=0, columnspan=3)

from_cart_to_signin_btn = Button(finish_screen, command=from_cart_to_signin, font=helv12, text="Back to Login",
                                 width=15)
from_cart_to_signin_btn.grid(row=3, column=0, columnspan=3, pady=20)
