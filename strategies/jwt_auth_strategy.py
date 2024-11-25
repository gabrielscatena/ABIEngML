# strategies/jwt_auth_strategy.py

from flask import current_app, make_response, request, redirect, url_for, flash
from jwt.exceptions import ExpiredSignatureError
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    set_access_cookies,
    unset_jwt_cookies,
    verify_jwt_in_request,
    
)
from sqlalchemy.orm import Session
from functools import wraps
from models import User
from .auth_strategy import AuthStrategy
from werkzeug.security import check_password_hash
import logging

class JWTAuthStrategy(AuthStrategy):
    def __init__(self, app):
        self.app = app

    def authenticate(self, username: str, password: str):
        db: Session = self.app.SessionLocal()
        user = db.query(User).filter_by(username=username).first()
        logging.debug(f"User retrieved: {user}")
        db.close()
        if user:
            password_valid = check_password_hash(user.password_hash, password)
            logging.debug(f"Password valid: {password_valid}")
            if password_valid:
                return user
        return None

    def login(self, user):
        access_token = create_access_token(identity=str(user.id))
        self.app.logger.debug(f"login: Created access token with identity {user.id}")
        next_page = request.args.get('next') or url_for('product.index')  # Redirect to 'next' if provided
        response = make_response(redirect(next_page))
        set_access_cookies(response, access_token)
        self.app.logger.debug(f"login: Set access token cookie for user {user.username}")
        return response


    def logout(self):
        response = make_response(redirect(url_for('product.index')))
        unset_jwt_cookies(response)
        return response

    def get_current_user(self):
        try:
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
            self.app.logger.debug(f"get_current_user: Retrieved user ID {user_id} (type: {type(user_id)})")
            if user_id is None:
                return None

            db = self.app.SessionLocal()
            try:
                user = db.get(User, int(user_id))  
                return user
            finally:
                db.close()
        except Exception as e:
            self.app.logger.error(f"Error in get_current_user: {e}", exc_info=True)
            return None


    def _get_user_by_id(self, user_id):
        db = self.app.SessionLocal()
        user = db.query(User).filter_by(id=user_id).first()
        db.close()
        return user

    def admin_required(self, f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            user = self.get_current_user()
            if not user.is_admin:
                flash('Admin access required.')
                return redirect(url_for('product.index'))
            return f(*args, **kwargs)
        return decorated_function
