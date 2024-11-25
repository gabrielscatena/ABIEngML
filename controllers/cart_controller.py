# controllers/cart_controller.py

from flask import Blueprint, render_template, flash, redirect, url_for
from sqlalchemy.orm import Session, joinedload
from models import CartItem, Product
from flask_jwt_extended import jwt_required

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/cart')
@jwt_required()
def view_cart():
    auth_strategy = cart_bp.app.auth_strategy
    user = auth_strategy.get_current_user()
    db: Session = cart_bp.app.SessionLocal()
    cart_items = db.query(CartItem).options(joinedload(CartItem.product)).filter_by(user_id=user.id).all()
    db.close()
    return render_template('cart.html', cart_items=cart_items)

@cart_bp.route('/cart/add/<int:product_id>')
@jwt_required()
def add_to_cart(product_id):
    app = cart_bp.app 
    auth_strategy = cart_bp.app.auth_strategy
    user = auth_strategy.get_current_user()
    if not user:  # Ensure the user is logged in
        flash('You need to log in to add items to the cart.')
        return redirect(url_for('auth.login'))

    db: Session = cart_bp.app.SessionLocal()
    try:
        product = db.get(Product, product_id)
        if not product:
            flash('Product not found.')
            return redirect(url_for('product.index'))

        # Check if the product is already in the cart
        existing_item = db.query(CartItem).filter_by(user_id=user.id, product_id=product_id).first()
        if existing_item:
            existing_item.quantity += 1
            flash(f'Updated quantity for {product.name} in your cart.')
        else:
            new_cart_item = CartItem(user_id=user.id, product_id=product_id, quantity=1)
            db.add(new_cart_item)
            flash(f'Added {product.name} to your cart.')

        db.commit()
    except Exception as e:
        db.rollback()
        app.logger.error(f"Error adding product to cart: {e}", exc_info=True)
        flash('An error occurred while adding the product to your cart. Please try again.')
    finally:
        db.close()

    return redirect(url_for('cart.view_cart'))


@cart_bp.route('/cart/remove/<int:item_id>')
@jwt_required()
def remove_from_cart(item_id):
    auth_strategy = cart_bp.app.auth_strategy
    user = auth_strategy.get_current_user()
    db: Session = cart_bp.app.SessionLocal()
    cart_item = db.get(CartItem, item_id)
    if cart_item and cart_item.user_id == user.id:
        db.delete(cart_item)
        db.commit()
        flash('Item removed from cart.')
    else:
        flash('Item not found in your cart.')
    db.close()
    return redirect(url_for('cart.view_cart'))
