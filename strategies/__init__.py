import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from app import app
from strategies.jwt_auth_strategy import JWTAuthStrategy