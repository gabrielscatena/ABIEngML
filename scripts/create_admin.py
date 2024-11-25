# create_admin.py

"""
Script to create an admin user.
"""
# Run at "."
# Usage: python create_admin.py

from database import SessionLocal
from models import User
from werkzeug.security import generate_password_hash

def create_admin():
    """
    Create an admin user in the database.
    """
    db = SessionLocal()
    username = input('Enter admin username: ')
    password = input('Enter admin password: ')
    existing_user = db.query(User).filter_by(username=username).first()
    if existing_user:
        print('User already exists.')
    else:
        hashed_password = generate_password_hash(password, method='scrypt')
        new_user = User(username=username, password_hash=hashed_password, is_admin=True)
        db.add(new_user)
        db.commit()
        print('Admin user created successfully.')
    db.close()

if __name__ == '__main__':
    create_admin()
