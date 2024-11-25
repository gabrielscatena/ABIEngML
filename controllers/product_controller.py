# controllers/product_controller.py

from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from sqlalchemy.orm import Session
from models import Product
from flask_jwt_extended import jwt_required
from functools import wraps
import logging

product_bp = Blueprint('product', __name__)

def admin_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        auth_strategy = current_app.auth_strategy
        user = auth_strategy.get_current_user()
        if not user.is_admin:
            flash('Admin access required.')
            return redirect(url_for('product.index'))
        return f(*args, **kwargs)
    return decorated_function

@product_bp.route('/')
def index():
    db: Session = product_bp.app.SessionLocal()
    products = db.query(Product).all()
    db.close()
    return render_template('index.html', products=products)

@product_bp.route('/admin/products')
@admin_required
def admin_products():
    db: Session = product_bp.app.SessionLocal()
    products = db.query(Product).all()
    db.close()
    return render_template('admin_products.html', products=products)

@product_bp.route('/admin/products/add', methods=['GET', 'POST'])
@admin_required
def add_product():
    if request.method == 'POST':
        logging.debug(f"Form data add product: {request.form}")
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        db: Session = product_bp.app.SessionLocal()
        new_product = Product(name=name, description=description, price=price, stock=stock)
        db.add(new_product)
        db.commit()
        db.close()
        flash('Product added successfully.')
        return redirect(url_for('product.admin_products'))
    return render_template('add_product.html')

@product_bp.route('/admin/products/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def edit_product(product_id):
    db: Session = product_bp.app.SessionLocal()
    product = db.get(Product, product_id)
    if not product:
        db.close()
        flash('Product not found.')
        return redirect(url_for('product.admin_products'))
    if request.method == 'POST':
        logging.debug(f"Form data edit product: {request.form}")
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = float(request.form['price'])
        product.stock = int(request.form['stock'])
        db.commit()
        db.close()
        flash('Product updated successfully.')
        return redirect(url_for('product.admin_products'))
    db.close()
    return render_template('edit_product.html', product=product)

@product_bp.route('/admin/products/delete/<int:product_id>', methods=['POST'])
@admin_required
def delete_product(product_id):
    db: Session = product_bp.app.SessionLocal()
    product = db.get(Product, product_id)
    if product:
        db.delete(product)
        db.commit()
        flash('Product deleted successfully.')
    else:
        flash('Product not found.')
    db.close()
    return redirect(url_for('product.admin_products'))
