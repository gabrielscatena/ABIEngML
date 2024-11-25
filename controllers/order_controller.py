from flask import Blueprint, render_template, flash, redirect, url_for, current_app
from sqlalchemy.orm import Session, joinedload
from models import Order, OrderItem, CartItem, Product
from flask_jwt_extended import jwt_required

order_bp = Blueprint('order', __name__)

@order_bp.route('/orders')
@jwt_required()
def view_orders():
    # Dynamically retrieve auth_strategy from the app
    auth_strategy = order_bp.app.auth_strategy
    user = auth_strategy.get_current_user()
    if not user:
        flash('You need to log in to view your orders.')
        return redirect(url_for('auth.login'))
    
    db: Session = order_bp.app.SessionLocal()
    orders = db.query(Order).options(
        joinedload(Order.items).joinedload(OrderItem.product)
    ).filter_by(user_id=user.id).all()
    db.close()
    return render_template('orders.html', orders=orders)

@order_bp.route('/order/place', methods=['GET','POST'])
@jwt_required()
def place_order():
    # Dynamically retrieve auth_strategy from the app
    auth_strategy = order_bp.app.auth_strategy
    user = auth_strategy.get_current_user()
    if not user:
        flash('You need to log in to place an order.')
        return redirect(url_for('auth.login'))
    
    db: Session = order_bp.app.SessionLocal()
    cart_items = db.query(CartItem).filter_by(user_id=user.id).all()
    if not cart_items:
        db.close()
        flash('Your cart is empty.')
        return redirect(url_for('product.index'))

    total_price = 0.0
    order_items = []

    for item in cart_items:
        product = db.get(Product, item.product_id)
        if product and product.stock >= item.quantity:
            product.stock -= item.quantity
            total_price += product.price * item.quantity
            order_item = OrderItem(product_id=product.id, quantity=item.quantity)
            order_items.append(order_item)
        else:
            db.close()
            flash(f'Product {product.name} is out of stock or insufficient quantity.')
            return redirect(url_for('cart.view_cart'))

    # Create and save the order
    new_order = Order(user_id=user.id, total_price=total_price, items=order_items)
    db.add(new_order)
    
    # Clear the cart for the user
    db.query(CartItem).filter_by(user_id=user.id).delete()
    
    db.commit()
    db.close()
    flash('Order placed successfully.')
    return redirect(url_for('order.view_orders'))
