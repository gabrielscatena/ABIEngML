# app.py


from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_jwt_extended import JWTManager
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__, static_folder='static')

from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Configurations from .env
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

# JWT configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_TOKEN_LOCATION'] = os.getenv('JWT_TOKEN_LOCATION').split(',')
app.config['JWT_COOKIE_SECURE'] = os.getenv('JWT_COOKIE_SECURE').lower() == 'true'
app.config['JWT_COOKIE_CSRF_PROTECT'] = os.getenv('JWT_COOKIE_CSRF_PROTECT').lower() == 'true'
app.config['JWT_COOKIE_SAMESITE'] = os.getenv('JWT_COOKIE_SAMESITE')
app.config['JWT_ACCESS_COOKIE_PATH'] = os.getenv('JWT_ACCESS_COOKIE_PATH')

jwt = JWTManager(app)

# Database setup
app.engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
session_factory = sessionmaker(bind=app.engine)
app.SessionLocal = scoped_session(session_factory)

# Import models and create tables
from models import Base  # Adjust import if needed
Base.metadata.create_all(bind=app.engine)

# Initialize authentication strategy
from strategies.jwt_auth_strategy import JWTAuthStrategy
auth_strategy = JWTAuthStrategy(app)
app.auth_strategy = auth_strategy  

# Context processor must be defined after auth_strategy is initialized
@app.context_processor
def inject_current_user():
    try:
        user = auth_strategy.get_current_user()
        app.logger.debug(f"inject_current_user: Retrieved user {user}")
        return {'current_user': user}
    except Exception as e:
        app.logger.error(f"Error in inject_current_user: {e}")
        return {'current_user': None}

# Import blueprints
from controllers.auth_controller import auth_bp
from controllers.product_controller import product_bp
from controllers.cart_controller import cart_bp
from controllers.order_controller import order_bp

# Provide app and auth_strategy context to blueprints
for bp in [auth_bp, product_bp, cart_bp, order_bp]:
    bp.app = app

# Register blueprints
app.register_blueprint(auth_bp)
for rule in app.url_map.iter_rules():
    if rule.endpoint.startswith("auth."):
        logging.debug(f"Auth route: {rule.endpoint} -> {rule.rule}")

app.register_blueprint(product_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(order_bp)

# Error handlers
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403

if __name__ == '__main__':
    logging.debug(f"Registered routes: {app.url_map}")
    app.run(debug=True)
