# app.py

"""
Main application module for the e-commerce backend.
"""

from flask import Flask, render_template, redirect, url_for, request, flash, session, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import Base, User, Product, CartItem, Order, OrderItem
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional, List
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker, joinedload
from functools import wraps
import logging
from datetime import datetime
# Divide classes using "MVC standard"
# Design pattern use Strategy
# Use JWT token for authentication

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test' ### TIRAR

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

# Initialize the database
app.engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
session_factory = sessionmaker(bind=app.engine)
app.SessionLocal = scoped_session(session_factory)
Base.metadata.create_all(bind=app.engine)

@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

# USE JWT TOKEN FOR AUTHENTICATION
@login_manager.user_loader
def load_user(user_id: int) -> Optional[User]:
    """
    Load a user from the database by ID.
    """
    db: Session = app.SessionLocal()
    user = db.get(User, int(user_id))
    db.close()
    return user

def admin_required(f):
    """
    Decorator to ensure that the user is an admin.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required.')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """
    Home page showing list of products.
    """
    db: Session = app.SessionLocal()
    products: List[Product] = db.query(Product).all()
    db.close()
    return render_template('index.html', products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register a new user.
    """
    if request.method == 'POST':
        logging.debug(f"Form data register: {request.form}")
        username: str = request.form['username']
        password: str = request.form['password']
        db: Session = app.SessionLocal()
        existing_user: Optional[User] = db.query(User).filter_by(username=username).first()
        if not username:
            flash('Username cannot be empty.')
        if existing_user:
            db.close()
            flash('Username already exists.')
            return redirect(url_for('register'))
        if len(password) < 6:
            flash('Password must be at least 6 characters long.')
            return redirect(url_for('register'))
        hashed_password: str = generate_password_hash(password, method='scrypt')
        new_user = User(username=username, password_hash=hashed_password)
        db.add(new_user)
        db.commit()
        db.close()
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log in an existing user.
    """
    if request.method == 'POST':
        logging.debug(f"Form data login: {request.form}")
        username: str = request.form['username']
        password: str = request.form['password']
        db: Session = app.SessionLocal()
        user: Optional[User] = db.query(User).filter_by(username=username).first()
        db.close()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """
    Log out the current user.
    """
    logout_user()
    return redirect(url_for('index'))

# Admin routes for product management
@app.route('/admin/products')
@login_required
@admin_required
def admin_products():
    """
    Admin view to list all products.
    """
    db: Session = app.SessionLocal()
    products: List[Product] = db.query(Product).all()
    db.close()
    return render_template('admin_products.html', products=products)

@app.route('/admin/products/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    """
    Admin view to add a new product.
    """
    if request.method == 'POST':
        logging.debug(f"Form data add product: {request.form}")
        name: str = request.form['name']
        description: str = request.form['description']
        price: float = float(request.form['price'])
        stock: int = int(request.form['stock'])
        db: Session = app.SessionLocal()
        new_product = Product(name=name, description=description, price=price, stock=stock)
        db.add(new_product)
        db.commit()
        db.close()
        flash('Product added successfully.')
        return redirect(url_for('admin_products'))
    return render_template('add_product.html')

@app.route('/admin/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(product_id: int):
    """
    Admin view to edit an existing product.
    """
    db: Session = app.SessionLocal()
    product: Optional[Product] = db.get(Product, product_id)
    if not product:
        db.close()
        flash('Product not found.')
        return redirect(url_for('admin_products'))
    if request.method == 'POST':
        logging.debug(f"Form data edit product: {request.form}")
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = float(request.form['price'])
        product.stock = int(request.form['stock'])
        db.commit()
        db.close()
        flash('Product updated successfully.')
        return redirect(url_for('admin_products'))
    db.close()
    return render_template('edit_product.html', product=product)

@app.route('/admin/products/delete/<int:product_id>', methods=['POST'])
@login_required
@admin_required
def delete_product(product_id: int):
    """
    Admin view to delete a product.
    """
    db: Session = app.SessionLocal()
    product: Optional[Product] = db.get(Product, product_id)
    if product:
        db.delete(product)
        db.commit()
        flash('Product deleted successfully.')
    else:
        flash('Product not found.')
    db.close()
    return redirect(url_for('admin_products'))

# User routes for cart and order management

@app.route('/cart')
@login_required
def view_cart():
    """
    View the current user's cart.
    """
    db: Session = app.SessionLocal()
    cart_items = db.query(CartItem).options(joinedload(CartItem.product)).filter_by(user_id=current_user.id).all()
    # cart_items: List[CartItem] = db.query(CartItem).filter_by(user_id=current_user.id).all()
    db.close()
    return render_template('cart.html', cart_items=cart_items)

@app.route('/cart/add/<int:product_id>')
@login_required
def add_to_cart(product_id: int):
    """
    Add a product to the current user's cart.
    """
    db: Session = app.SessionLocal()
    product: Optional[Product] = db.get(Product, product_id)
    if not product:
        db.close()
        flash('Product not found.')
        return redirect(url_for('index'))
    existing_item: Optional[CartItem] = db.query(CartItem).filter_by(user_id=current_user.id, product_id=product_id).first()
    if existing_item:
        existing_item.quantity += 1
    else:
        new_cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=1)
        db.add(new_cart_item)
    db.commit()
    db.close()
    flash('Product added to cart.')
    return redirect(url_for('view_cart'))

@app.route('/cart/remove/<int:item_id>')
@login_required
def remove_from_cart(item_id: int):
    """
    Remove an item from the current user's cart.
    """
    db: Session = app.SessionLocal()
    cart_item: Optional[CartItem] = db.get(CartItem, item_id)
    if cart_item and cart_item.user_id == current_user.id:
        db.delete(cart_item)
        db.commit()
        flash('Item removed from cart.')
    else:
        flash('Item not found in your cart.')
    db.close()
    return redirect(url_for('view_cart'))

@app.route('/orders')
@login_required
def view_orders():
    """
    View the current user's orders.
    """
    db: Session = app.SessionLocal()
    orders: List[Order] = db.query(Order).options(
        joinedload(Order.items).joinedload(OrderItem.product)
    ).filter_by(user_id=current_user.id).all()
    db.close()
    return render_template('orders.html', orders=orders)


@app.route('/order/place')
@login_required
def place_order():
    """
    Place an order with the items in the current user's cart.
    """
    db: Session = app.SessionLocal()
    cart_items: List[CartItem] = db.query(CartItem).filter_by(user_id=current_user.id).all()
    if not cart_items:
        db.close()
        flash('Your cart is empty.')
        return redirect(url_for('index'))
    total_price: float = 0.0
    order_items: List[OrderItem] = []
    for item in cart_items:
        product: Optional[Product] = db.get(Product, item.product_id)
        if product and product.stock >= item.quantity:
            product.stock -= item.quantity
            total_price += product.price * item.quantity
            order_item = OrderItem(product_id=product.id, quantity=item.quantity)
            order_items.append(order_item)
        else:
            db.close()
            flash(f'Product {product.name} is out of stock or insufficient quantity.')
            return redirect(url_for('view_cart'))
    new_order = Order(user_id=current_user.id, total_price=total_price, items=order_items)
    db.add(new_order)
    # Clear cart
    db.query(CartItem).filter_by(user_id=current_user.id).delete()
    db.commit()
    db.close()
    flash('Order placed successfully.')
    return redirect(url_for('view_orders'))

# Error handling

@app.errorhandler(404)
def page_not_found(error):
    """
    Handle 404 errors.
    """
    return render_template('404.html'), 404

@app.errorhandler(403)
def forbidden(error):
    """
    Handle 403 errors.
    """
    return render_template('403.html'), 403

if __name__ == '__main__':
    app.run(debug=True)
