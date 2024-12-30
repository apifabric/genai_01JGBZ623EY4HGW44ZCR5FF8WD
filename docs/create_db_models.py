# using resolved_model self.resolved_model FIXME
# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text, DECIMAL
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from datetime import date   
from datetime import datetime
from typing import List


logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py


from sqlalchemy.dialects.sqlite import *

class Restaurant(Base):
    """description: This table stores data about each restaurant including contact information and location."""
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    address = Column(String)
    phone = Column(String)
    email = Column(String)

class Menu(Base):
    """description: This table contains list of menus offered by a restaurant."""
    __tablename__ = 'menus'
    id = Column(Integer, primary_key=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    name = Column(String)
    description = Column(String)

class MenuItem(Base):
    """description: This table lists items in the menus with their descriptions and prices."""
    __tablename__ = 'menu_items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    menu_id = Column(Integer, ForeignKey('menus.id'))
    name = Column(String)
    description = Column(String)
    price = Column(Integer)

class Customer(Base):
    """description: This stores customer details who visit or purchase from the restaurant."""
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    phone = Column(String)
    email = Column(String)

class Order(Base):
    """description: This table stores orders made by customers at a restaurant."""
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    date = Column(DateTime)

class OrderItem(Base):
    """description: Linked to orders, this contains individual menu items, quantity ordered in a specific order."""
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    menu_item_id = Column(Integer, ForeignKey('menu_items.id'))
    quantity = Column(Integer)

class Supplier(Base):
    """description: Stores details of suppliers who provide ingredients or products to the restaurant."""
    __tablename__ = 'suppliers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    contact = Column(String)
    email = Column(String)

class Ingredient(Base):
    """description: Ingredient table captures information about ingredients needed for menu items, supplier info."""
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'))

class Inventory(Base):
    """description: Captures information about current inventory level for ingredients, last update history."""
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'))
    amount = Column(Integer)
    last_updated = Column(DateTime)

class Employee(Base):
    """description: Dataset capturing employee information working within the restaurant."""
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    role = Column(String)
    phone = Column(String)

class Reservation(Base):
    """description: Holds data pertaining reserving tables by customers at restaurants."""
    __tablename__ = 'reservations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    datetime = Column(DateTime)
    num_people = Column(Integer)

class Payment(Base):
    """description: Payment records storing information about payments made against orders."""
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    amount = Column(Integer)
    date = Column(DateTime)


# end of model classes


try:
    
    
    # ALS/GenAI: Create an SQLite database
    import os
    mgr_db_loc = True
    if mgr_db_loc:
        print(f'creating in manager: sqlite:///system/genai/temp/create_db_models.sqlite')
        engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
    else:
        current_file_path = os.path.dirname(__file__)
        print(f'creating at current_file_path: {current_file_path}')
        engine = create_engine(f'sqlite:///{current_file_path}/create_db_models.sqlite')
    Base.metadata.create_all(engine)
    
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # ALS/GenAI: Prepare for sample data
    
    
    session.commit()
    restaurant1 = Restaurant(name="Fine Dine", address="123 Culinary Blvd", phone="1234567890", email="info@finedine.com")
    restaurant2 = Restaurant(name="Bistro Cafe", address="456 Gourmet Rd", phone="0987654321", email="contact@bistrocafe.com")
    restaurant3 = Restaurant(name="Taste Paradise", address="789 Flavor St", phone="1122334455", email="hello@tasteparadise.com")
    restaurant4 = Restaurant(name="Pizza Palace", address="111 Dough Ave", phone="9988776655", email="pizza@pizzapalace.com")
    menu1 = Menu(restaurant_id=1, name="Summer Menu", description="Seasonal offerings")
    menu2 = Menu(restaurant_id=2, name="Winter Warmers", description="Cozy and warm dishes")
    menu3 = Menu(restaurant_id=3, name="Spring Specials", description="Fresh spring produce")
    menu4 = Menu(restaurant_id=4, name="Autumn Delights", description="Taste of fall")
    menu_item1 = MenuItem(menu_id=1, name="Grilled Chicken", description="Tender grilled chicken", price=15)
    menu_item2 = MenuItem(menu_id=2, name="Creamy Tomato Soup", description="Perfect for winters", price=8)
    menu_item3 = MenuItem(menu_id=3, name="Asparagus Salad", description="Spring fresh salad", price=12)
    menu_item4 = MenuItem(menu_id=4, name="Pumpkin Pie", description="Sweet and savory pie", price=10)
    customer1 = Customer(name="John Doe", phone="2345678901", email="john@doemail.com")
    customer2 = Customer(name="Jane Smith", phone="3456789012", email="jane@smithmail.com")
    customer3 = Customer(name="Daniel Craig", phone="4567890123", email="dan@craigmail.com")
    customer4 = Customer(name="Emily Clark", phone="5678901234", email="emily@clarkmail.com")
    order1 = Order(customer_id=1, restaurant_id=1, date=datetime(2023, 11, 1, 19, 45))
    order2 = Order(customer_id=2, restaurant_id=2, date=datetime(2023, 11, 3, 20, 0))
    order3 = Order(customer_id=3, restaurant_id=3, date=datetime(2023, 11, 4, 18, 30))
    order4 = Order(customer_id=4, restaurant_id=4, date=datetime(2023, 11, 5, 21, 15))
    order_item1 = OrderItem(order_id=1, menu_item_id=1, quantity=2)
    order_item2 = OrderItem(order_id=2, menu_item_id=2, quantity=1)
    order_item3 = OrderItem(order_id=3, menu_item_id=3, quantity=3)
    order_item4 = OrderItem(order_id=4, menu_item_id=4, quantity=1)
    supplier1 = Supplier(name="Fresh Farms", contact="9876543210", email="contact@freshfarms.com")
    supplier2 = Supplier(name="Local Harvest", contact="8765432109", email="info@localharvest.com")
    supplier3 = Supplier(name="Global Foods", contact="7654321098", email="hello@globalfoods.com")
    supplier4 = Supplier(name="Organic Source", contact="6543210987", email="sales@organicsource.com")
    ingredient1 = Ingredient(name="Chicken Breast", supplier_id=1)
    ingredient2 = Ingredient(name="Tomatoes", supplier_id=2)
    ingredient3 = Ingredient(name="Asparagus", supplier_id=3)
    ingredient4 = Ingredient(name="Pumpkin", supplier_id=4)
    inventory1 = Inventory(ingredient_id=1, amount=50, last_updated=datetime(2023, 11, 1))
    inventory2 = Inventory(ingredient_id=2, amount=100, last_updated=datetime(2023, 11, 2))
    inventory3 = Inventory(ingredient_id=3, amount=60, last_updated=datetime(2023, 11, 3))
    inventory4 = Inventory(ingredient_id=4, amount=30, last_updated=datetime(2023, 11, 4))
    employee1 = Employee(name="Alice Brown", role="Chef", phone="3334445556")
    employee2 = Employee(name="Bob White", role="Server", phone="4445556667")
    employee3 = Employee(name="Carol Green", role="Manager", phone="5556667778")
    employee4 = Employee(name="David Black", role="Cleaner", phone="6667778889")
    reservation1 = Reservation(customer_id=1, restaurant_id=1, datetime=datetime(2023, 11, 1, 18, 0), num_people=4)
    reservation2 = Reservation(customer_id=2, restaurant_id=2, datetime=datetime(2023, 11, 2, 19, 0), num_people=2)
    reservation3 = Reservation(customer_id=3, restaurant_id=3, datetime=datetime(2023, 11, 3, 20, 0), num_people=5)
    reservation4 = Reservation(customer_id=4, restaurant_id=4, datetime=datetime(2023, 11, 4, 21, 0), num_people=3)
    payment1 = Payment(order_id=1, amount=30, date=datetime(2023, 11, 1, 20, 0))
    payment2 = Payment(order_id=2, amount=8, date=datetime(2023, 11, 3, 20, 30))
    payment3 = Payment(order_id=3, amount=36, date=datetime(2023, 11, 4, 19, 0))
    payment4 = Payment(order_id=4, amount=10, date=datetime(2023, 11, 5, 21, 30))
    
    
    
    session.add_all([restaurant1, restaurant2, restaurant3, restaurant4, menu1, menu2, menu3, menu4, menu_item1, menu_item2, menu_item3, menu_item4, customer1, customer2, customer3, customer4, order1, order2, order3, order4, order_item1, order_item2, order_item3, order_item4, supplier1, supplier2, supplier3, supplier4, ingredient1, ingredient2, ingredient3, ingredient4, inventory1, inventory2, inventory3, inventory4, employee1, employee2, employee3, employee4, reservation1, reservation2, reservation3, reservation4, payment1, payment2, payment3, payment4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
