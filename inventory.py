# Programme for a Nike shoe warehouse manager to perform stock taking and
# manage stock data.

# ======================== CLASSES & CLASS FUNCTIONS ==========================

# Initialises Shoe object class.
class Shoe:
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

# Returns cost of Shoe class object, formatted to two decimal points (pennies).
## WHERE IS THIS BEING USED?
    def get_cost(self):
        print(f"The cost of the shoe is £{float(self.cost):.2f}.")

# Returns quantity of Shoe class object.
## WHERE IS THIS BEING USED?
    def get_quantity(self):
        print(f"The quantity of the shoes is {self.quantity} units.")

# Returns string representation of Shoe class object.
## This is a custom string function - is there a default if I don't define it?
    def __str__(self):
        print(f"Country: {self.country}\n"
              f"Code: {self.code}\n"
              f"Product: {self.product}\n"
              f"Cost: £{float(self.cost):.2f}\n"
              f"Quantity: {self.quantity}")

# Initialises Inventory object class (list to hold Shoe class objects.)
## Could also just be a list lol - inventory = []
class Inventory:
    def __init__(self):
        self.inventory_list = []


# ============================ LISTS & DICTIONARIES ==========================

# Inventory class object
inventory = Inventory()


# =============================== FUNCTIONS ===================================

# Reads data from file inventory.txt; uses data to create new shoe objects and
# appends these to inventory list.  Skips first line of .txt file (unwanted
# data).  Error handling in place in case file does not exist or is empty.
def read_shoes_data():
    while True:
        try:
            with open("inventory.txt", "r") as f:
                counter = 0
                for line in f:
                    if counter == 0:
                        pass
                    else:
                        line_content = line
                        split_line_content = line_content.split(",")
                        shoe = Shoe(split_line_content[0], split_line_content[1],
                                    split_line_content[2], split_line_content[3], 
                                    split_line_content[4].replace("\n", ""))
                        inventory.inventory_list.append(shoe)
                    counter += 1
            break
        except FileNotFoundError:
            print("Error - product data file not found.")
            print()
            break
    
    if not inventory.inventory_list:
        print("!! WARNING !! - no product data in file. Populate file before "
              "proceeding.")
        print("\n")

# Allows user to input data about and create a new shoe object and adds this
# to the inventory list.  Adds new object data to .txt file.
def capture_shoes():
    print()
    country_input = input("Please enter shoe country: ")
    code_input = input("Please input shoe SKU code: ")
    product_input = input("Please input shoe product name: ")
    while True:
        try:
            cost_input = float(input("Please input shoe cost: £"))
            break
        except ValueError:
            print("Error - please input digits only.")
    while True:
        try:
            quantity_input = int(input("Please input shoe quantity: "))
            break
        except ValueError:
            print("Error - please input digits only.")

    shoe = Shoe(country_input, code_input, product_input, cost_input, 
                quantity_input)
    inventory.inventory_list.append(shoe)

    with open("inventory.txt", "a") as f:
        f.write(f"{country_input},{code_input},{product_input},{cost_input},"
                f"{quantity_input}\n")
    
    print()
    print("New product data added.")

# Iterates over inventory and print details of shoe objects returned.
## Use  __str__ function.
def view_all():
    for shoe in inventory.inventory_list:
        print()
        shoe.__str__()

# Determines which shoe object has the lowest quantity.  Asks user if they want
# to update quantity of this shoe object (restock); if yes, updates shoe object
# quantity.  Updates .txt file with changes.
def re_stock():
    all_quantities = []
    for shoe in inventory.inventory_list:
        all_quantities.append(int(shoe.quantity))

    qt_of_lowest_qt_shoe = min(all_quantities)
    for shoe in inventory.inventory_list:
        if int(shoe.quantity) == qt_of_lowest_qt_shoe:
            print()
            print(f"The/A shoe with (one of) the lowest quantity/ies in stock "
                  f"is {shoe.product} (Code: {shoe.code}).")
            while True:
                print()
                restock_choice = input("Enter 'rs' to update stock quantity "
                                       "for this shoe, or press enter to go "
                                       "back: ")
                if restock_choice.upper() == "RS":
                    while True:
                        try:
                            print()
                            new_qt = int(input("Input new quantity: ")) 
                            break
                        except ValueError:
                            print()
                            print("Error - please input an integer.")
                    shoe.quantity = new_qt
                
                    with open("inventory.txt", "w") as f:
                        f.write("Country,Code,Product,Cost,Quantity\n")
                        for shoe in inventory.inventory_list:
                            f.write(f"{shoe.country},{shoe.code},"
                                    f"{shoe.product},{shoe.cost},"
                                    f"{shoe.quantity}\n")
                        print()
                        print("Product quantity updated.")
                        break
                elif restock_choice == "":
                    break
                else:
                    print()
                    print("Input error - please try again.")

# Allows user to find and print shoe object information based on SKU code.
def search_shoe():
    print()
    code_search = input("Please enter the SKU code of the shoe: ")
    print()
    sku_match_count = 0
    for shoe in inventory.inventory_list:
        if shoe.code == code_search:
            print("Search result:")
            shoe.__str__()
            sku_match_count += 1
    
    if sku_match_count == 0:
        print("No match found.")

# Calculates and displays total inventory value for each shoe object.
def value_per_item():
    for shoe in inventory.inventory_list:
        shoe_value = float(shoe.cost) * int(shoe.quantity)
        print()
        print(f"Total value of {shoe.product} (Code: {shoe.code}) in stock: "
              f"£{float(shoe_value):.2f}")

# Determines which shoe object has the highest quantity.  Prints message
# announcing that this shoe is on sale.
## WORKS.
def highest_qty():
    print()
    all_quantities = []
    for shoe in inventory.inventory_list:
        all_quantities.append(int(shoe.quantity))

    qt_of_highest_qt_shoe = max(all_quantities)

    for shoe in inventory.inventory_list:
        if int(shoe.quantity) == qt_of_highest_qt_shoe:
            print(f"{shoe.product} (Code: {shoe.code}) is now ON SALE.")


# ================================= PROGRAMME =================================

print()
print("--------------------- Shoe Inventory Admin System ---------------------")
print() 

# Menu allowing user to input to execute any of the functions.

menu_text = '''          MAIN MENU

a  - Add data for new shoe product type to inventory.
vd - View data for all types of shoe product in inventory.
rs - View and restock lowest stock product type(s).
s  - Search for product information using SKU code.
vv - View total stock value for each product type.
sn - Generate sale notice for highest stock product type(s).
e  - Exit.

     Enter letter code: '''

while True:
    read_shoes_data()
    menu_choice = input(menu_text).strip().lower()
    print()

    if menu_choice == "a":
        print()
        print("          ADD NEW PRODUCT TYPE")
        capture_shoes()
        print("\n")
    
    elif menu_choice == "vd":
        print()
        print("          ALL PRODUCTS DATA")
        view_all()
        print("\n")

    elif menu_choice == "rs":
        print()
        print("          RESTOCK PRODUCT")
        re_stock()
        print("\n")
    
    elif menu_choice == "s":
        print()
        print("          PRODUCT SEARCH")
        search_shoe()
        print("\n")
    
    elif menu_choice == "vv":
        print()
        print("          VIEW PRODUCT STOCK VALUE")
        value_per_item()
        print("\n")
    
    elif menu_choice == "sn":
        print()
        print("          SALE NOTICE")
        highest_qty()
        print("\n")
    
    elif menu_choice == "e":
        print("Goodbye.")
        print()
        exit()
    
    else:
        print("Input error.")
        print()