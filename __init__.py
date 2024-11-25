import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from app import app
# from .models import Base, User, Product, CartItem, Order, OrderItem
# from .controllers.auth_controller import auth_bp
# from .controllers.product_controller import product_bp
# from .controllers.cart_controller import cart_bp
# from .controllers.order_controller import order_bp
# from .strategies.jwt_auth_strategy import JWTAuthStrategy