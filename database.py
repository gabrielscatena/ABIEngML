# database.py

"""
This module sets up the database connection and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from flask import g

DATABASE_URL = 'sqlite:///ecommerce.db'

engine = create_engine(
    DATABASE_URL, connect_args={'check_same_thread': False}
)
session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal = scoped_session(session_factory)

Base = declarative_base()
