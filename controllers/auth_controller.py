# controllers/auth_controller.py

from flask import Blueprint, request, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import Session
import logging
from models import User

auth_bp = Blueprint('auth', __name__)
auth_strategy = None  # Will be set in app.py

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        logging.debug(f"Form data register: {request.form}")
        username = request.form['username']
        password = request.form['password']
        db: Session = auth_bp.app.SessionLocal()

        if not username:
            flash('Username cannot be empty.')
            return redirect(url_for('auth.register'))

        existing_user = db.query(User).filter_by(username=username).first()
        if existing_user:
            db.close()
            flash('Username already exists.')
            return redirect(url_for('auth.register'))

        if len(password) < 6:
            flash('Password must be at least 6 characters long.')
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password, method='scrypt')
        new_user = User(username=username, password_hash=hashed_password)
        db.add(new_user)
        db.commit()
        db.close()

        flash('Registration successful. Please log in.')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        logging.debug(f"Form data login: {request.form}")
        username = request.form['username']
        password = request.form['password']

        user = auth_strategy.authenticate(username, password)
        if user:
            return auth_strategy.login(user)
        else:
            flash('Invalid username or password.')
            return redirect(url_for('auth.login'))
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    return auth_strategy.logout()

@auth_bp.before_app_request
def load_auth_strategy():
    global auth_strategy
    if auth_strategy is None:
        auth_strategy = auth_bp.app.auth_strategy




