# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  December 30, 2024 14:24:49
# Database: sqlite:////tmp/tmp.xQylehHROW-01JGBZ623EY4HGW44ZCR5FF8WD/RestaurantManagement/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *

Base = SAFRSBaseX



class Customer(Base):  # type: ignore
    """
    description: This stores customer details who visit or purchase from the restaurant.
    """
    __tablename__ = 'customers'
    _s_collection_name = 'Customer'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    email = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    OrderList : Mapped[List["Order"]] = relationship(back_populates="customer")
    ReservationList : Mapped[List["Reservation"]] = relationship(back_populates="customer")



class Employee(Base):  # type: ignore
    """
    description: Dataset capturing employee information working within the restaurant.
    """
    __tablename__ = 'employees'
    _s_collection_name = 'Employee'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(String)
    phone = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)



class Restaurant(Base):  # type: ignore
    """
    description: This table stores data about each restaurant including contact information and location.
    """
    __tablename__ = 'restaurants'
    _s_collection_name = 'Restaurant'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    phone = Column(String)
    email = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    MenuList : Mapped[List["Menu"]] = relationship(back_populates="restaurant")
    OrderList : Mapped[List["Order"]] = relationship(back_populates="restaurant")
    ReservationList : Mapped[List["Reservation"]] = relationship(back_populates="restaurant")



class Supplier(Base):  # type: ignore
    """
    description: Stores details of suppliers who provide ingredients or products to the restaurant.
    """
    __tablename__ = 'suppliers'
    _s_collection_name = 'Supplier'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact = Column(String)
    email = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    IngredientList : Mapped[List["Ingredient"]] = relationship(back_populates="supplier")



class Ingredient(Base):  # type: ignore
    """
    description: Ingredient table captures information about ingredients needed for menu items, supplier info.
    """
    __tablename__ = 'ingredients'
    _s_collection_name = 'Ingredient'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String)
    supplier_id = Column(ForeignKey('suppliers.id'))

    # parent relationships (access parent)
    supplier : Mapped["Supplier"] = relationship(back_populates=("IngredientList"))

    # child relationships (access children)
    InventoryList : Mapped[List["Inventory"]] = relationship(back_populates="ingredient")



class Menu(Base):  # type: ignore
    """
    description: This table contains list of menus offered by a restaurant.
    """
    __tablename__ = 'menus'
    _s_collection_name = 'Menu'  # type: ignore

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(ForeignKey('restaurants.id'))
    name = Column(String)
    description = Column(String)

    # parent relationships (access parent)
    restaurant : Mapped["Restaurant"] = relationship(back_populates=("MenuList"))

    # child relationships (access children)
    MenuItemList : Mapped[List["MenuItem"]] = relationship(back_populates="menu")



class Order(Base):  # type: ignore
    """
    description: This table stores orders made by customers at a restaurant.
    """
    __tablename__ = 'orders'
    _s_collection_name = 'Order'  # type: ignore

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customers.id'))
    restaurant_id = Column(ForeignKey('restaurants.id'))
    date = Column(DateTime)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("OrderList"))
    restaurant : Mapped["Restaurant"] = relationship(back_populates=("OrderList"))

    # child relationships (access children)
    PaymentList : Mapped[List["Payment"]] = relationship(back_populates="order")
    OrderItemList : Mapped[List["OrderItem"]] = relationship(back_populates="order")



class Reservation(Base):  # type: ignore
    """
    description: Holds data pertaining reserving tables by customers at restaurants.
    """
    __tablename__ = 'reservations'
    _s_collection_name = 'Reservation'  # type: ignore

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customers.id'))
    restaurant_id = Column(ForeignKey('restaurants.id'))
    datetime = Column(DateTime)
    num_people = Column(Integer)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("ReservationList"))
    restaurant : Mapped["Restaurant"] = relationship(back_populates=("ReservationList"))

    # child relationships (access children)



class Inventory(Base):  # type: ignore
    """
    description: Captures information about current inventory level for ingredients, last update history.
    """
    __tablename__ = 'inventory'
    _s_collection_name = 'Inventory'  # type: ignore

    id = Column(Integer, primary_key=True)
    ingredient_id = Column(ForeignKey('ingredients.id'))
    amount = Column(Integer)
    last_updated = Column(DateTime)

    # parent relationships (access parent)
    ingredient : Mapped["Ingredient"] = relationship(back_populates=("InventoryList"))

    # child relationships (access children)



class MenuItem(Base):  # type: ignore
    """
    description: This table lists items in the menus with their descriptions and prices.
    """
    __tablename__ = 'menu_items'
    _s_collection_name = 'MenuItem'  # type: ignore

    id = Column(Integer, primary_key=True)
    menu_id = Column(ForeignKey('menus.id'))
    name = Column(String)
    description = Column(String)
    price = Column(Integer)

    # parent relationships (access parent)
    menu : Mapped["Menu"] = relationship(back_populates=("MenuItemList"))

    # child relationships (access children)
    OrderItemList : Mapped[List["OrderItem"]] = relationship(back_populates="menu_item")



class Payment(Base):  # type: ignore
    """
    description: Payment records storing information about payments made against orders.
    """
    __tablename__ = 'payments'
    _s_collection_name = 'Payment'  # type: ignore

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('orders.id'))
    amount = Column(Integer)
    date = Column(DateTime)

    # parent relationships (access parent)
    order : Mapped["Order"] = relationship(back_populates=("PaymentList"))

    # child relationships (access children)



class OrderItem(Base):  # type: ignore
    """
    description: Linked to orders, this contains individual menu items, quantity ordered in a specific order.
    """
    __tablename__ = 'order_items'
    _s_collection_name = 'OrderItem'  # type: ignore

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('orders.id'))
    menu_item_id = Column(ForeignKey('menu_items.id'))
    quantity = Column(Integer)

    # parent relationships (access parent)
    menu_item : Mapped["MenuItem"] = relationship(back_populates=("OrderItemList"))
    order : Mapped["Order"] = relationship(back_populates=("OrderItemList"))

    # child relationships (access children)
