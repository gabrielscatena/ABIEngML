import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from app import app
from models import Base, User, Product, CartItem, Order, OrderItem