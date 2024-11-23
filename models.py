# models.py

"""
This module defines the database models for the e-commerce backend.
"""

from database import Base
from typing import List
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from flask_login import UserMixin

class User(UserMixin, Base):
    """
    Represents a user in the system.

    Attributes:
        id (int): Primary key.
        username (str): Unique username.
        password_hash (str): Hashed password.
        is_admin (bool): Flag indicating if the user is an admin.
        cart_items (List[CartItem]): List of items in the user's cart.
        orders (List[Order]): List of orders placed by the user.
    """
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True)
    username: str = Column(String(150), unique=True, nullable=False)
    password_hash: str = Column(String(150), nullable=False)
    is_admin: bool = Column(Boolean, default=False)
    cart_items = relationship('CartItem', back_populates='user', cascade='all, delete-orphan')
    orders = relationship('Order', back_populates='user', cascade='all, delete-orphan')

class Product(Base):
    """
    Represents a product in the catalog.

    Attributes:
        id (int): Primary key.
        name (str): Name of the product.
        description (str): Description of the product.
        price (float): Price of the product.
        stock (int): Quantity available in stock.
    """
    __tablename__ = 'products'

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(150), nullable=False)
    description: str = Column(String(500))
    price: float = Column(Float, nullable=False)
    stock: int = Column(Integer, default=0)

class CartItem(Base):
    """
    Represents an item in a user's cart.

    Attributes:
        id (int): Primary key.
        user_id (int): Foreign key to the user.
        product_id (int): Foreign key to the product.
        quantity (int): Quantity of the product in the cart.
        user (User): The user who owns the cart item.
        product (Product): The product added to the cart.
    """
    __tablename__ = 'cart_items'

    id: int = Column(Integer, primary_key=True)
    user_id: int = Column(Integer, ForeignKey('users.id'))
    product_id: int = Column(Integer, ForeignKey('products.id'))
    quantity: int = Column(Integer, default=1)

    user = relationship('User', back_populates='cart_items')
    product = relationship('Product')

class Order(Base):
    """
    Represents an order placed by a user.

    Attributes:
        id (int): Primary key.
        user_id (int): Foreign key to the user.
        timestamp (datetime): Time when the order was placed.
        total_price (float): Total price of the order.
        items (List[OrderItem]): List of items in the order.
        user (User): The user who placed the order.
    """
    __tablename__ = 'orders'

    id: int = Column(Integer, primary_key=True)
    user_id: int = Column(Integer, ForeignKey('users.id'))
    timestamp: datetime = Column(DateTime, default=datetime.now(timezone.utc))
    total_price: float = Column(Float)
    items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')
    user = relationship('User', back_populates='orders')

class OrderItem(Base):
    """
    Represents an item in an order.

    Attributes:
        id (int): Primary key.
        order_id (int): Foreign key to the order.
        product_id (int): Foreign key to the product.
        quantity (int): Quantity of the product ordered.
        order (Order): The order containing this item.
        product (Product): The product that was ordered.
    """
    __tablename__ = 'order_items'

    id: int = Column(Integer, primary_key=True)
    order_id: int = Column(Integer, ForeignKey('orders.id'))
    product_id: int = Column(Integer, ForeignKey('products.id'))
    quantity: int = Column(Integer)

    order = relationship('Order', back_populates='items')
    product = relationship('Product')