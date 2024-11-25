# tests.py        

import unittest
import uuid
from app import app
from models import Base, User, Product, CartItem, Order, OrderItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from werkzeug.security import generate_password_hash, check_password_hash

''' bash
Single test:
Usage: pytest tests.py::EcommerceTestCase::test_data_retrieval_after_restart

All tests
Usage: pytest tests.py
'''


class EcommerceTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up a test client and initialize the in-memory database.
        """
        self.engine = create_engine('sqlite:///:memory:')
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        Base.metadata.create_all(bind=self.engine)
        self.db = self.Session()

        app.config['TESTING'] = True
        app.engine = self.engine
        app.SessionLocal = self.Session

        self.app_context = app.app_context()
        self.app_context.push()

        self.client = app.test_client()

        # Create a default test user
        self.test_user = self.create_user('testuser', 'testpass')

    def tearDown(self):
        """
        Clean up after each test.
        """
        self.db.close()
        self.Session.remove()
        Base.metadata.drop_all(bind=self.engine)
        self.app_context.pop()

    # Helper methods below (DRY)    
    def login_user(self, username, password):
        """
        Helper function to login a user for the tests and return the response.
        """
        response = self.client.post('/login', data={'username': username, 'password': password}, follow_redirects=True)
        return response
 
    def create_user(self, username, password):
        user = User(username=username, password_hash=generate_password_hash(password, method='scrypt'))
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def create_product(self, name, description, price, stock):
        product = Product(name=name, description=description, price=price, stock=stock)
        self.db.add(product)
        self.db.commit()
        return product

    def register_unique_user(self, password):
        """
        Helper function to register a user with a username and password.
        """
        unique_username = f'testuser{uuid.uuid4()}'
        response = self.client.post('/register', data={
            'username': unique_username,
            'password': password
        }, follow_redirects=True)
        return response

    def place_order_and_verify_cart(self, client, product_id):
        response = client.get(f'/cart/add/{product_id}', follow_redirects=True)
        self.assertIn(b'Added Test Product to your cart.', response.data)

        response = client.get('/order/place', follow_redirects=True)
        self.assertIn(b'Order placed successfully.', response.data)  # Confirm the order was placed successfully


    # 1. User Registration Test GREEN
    def test_user_registration_valid_details(self) -> None: # GREEN
        """
        Test user registration with valid details.
        """
        response = self.register_unique_user('validPassword1')
        self.assertIn(b'Registration successful. Please log in.', response.data)

    def test_user_registration_invalid_password(self): # GREEN
        """
        Test user registration with an invalid password (e.g., too short).
        """
        response = self.register_unique_user('123')  # Short password
        self.assertIn(b'Password must be at least 6 characters long.', response.data) # TODO

    def test_user_registration_duplicate_username(self): # GREEN
        """
        Test user registration with a duplicate username.
        """
        unique_username = f'testuser{uuid.uuid4()}'
        with self.client as client:
            # First registration
            client.post('/register', data={
                'username': unique_username,
                'password': 'validPassword123'
            }, follow_redirects=True)

            # Second registration with the same username
            response = client.post('/register', data={
                'username': unique_username,
                'password': 'validPassword123'
            }, follow_redirects=True)
            self.assertIn(b'Username already exists.', response.data)


    def test_password_hashing(self): # GREEN
        """
        Test that the password is properly hashed during registration.
        """
        unique_username = f'testuser{uuid.uuid4()}'
        password = 'validPassword123'
        with self.client as client:
            client.post('/register', data={
                'username': unique_username,
                'password': password
            }, follow_redirects=True)
            user = self.db.query(User).filter_by(username=unique_username).first()
            self.assertNotEqual(user.password_hash, password)
            self.assertTrue(check_password_hash(user.password_hash, password))

   
    # 2. Login Test
    def test_successful_login(self): # GREEN
        """
        Test login with valid credentials.
        """
        self.login_user('testuser', 'testpass')

    def test_failed_login_invalid_credentials(self):
        """
        Test login with invalid credentials (wrong password or username).
        """
        response = self.login_user('testuser', 'wrongpassword')  # Attempt to login with incorrect credentials
        
        # Assert the error message for invalid credentials
        self.assertIn(b'Invalid username or password.', response.data)


    # 3. Product Management Test (for Admins)
    def test_admin_edit_product(self): # GREEN
        """
        Test editing a product by admin.
        """
        self.create_user('admin', 'admin')
        self.db.query(User).filter_by(username='admin').update({"is_admin": True})  # Set admin flag to True
        
        product = self.create_product('Test Product', 'Test Description', 10.0, 100)
        product = self.db.get(Product, product.id)

        assert product is not None

        with self.client as client:
            response = client.post('/login', data={'username': 'admin', 'password': 'admin'}, follow_redirects=True)
            self.assertIn(b'Logout', response.data)
            response = client.post(f'/admin/products/edit/{product.id}', data={
                'name': 'Updated Product',
                'description': 'Updated Description',
                'price': '12.0',
                'stock': '200'
            }, follow_redirects=True)
            self.assertIn(b'Product updated successfully', response.data)
            #updated_product = self.db.query(Product).get(product.id) # DEPRECATED
            updated_product = self.db.get(Product, product.id)
            self.assertEqual(updated_product.name, 'Updated Product')
            self.assertEqual(updated_product.description, 'Updated Description')
            self.assertEqual(updated_product.price, 12.0)
            self.assertEqual(updated_product.stock, 200)


    def test_admin_remove_product(self): #GREEN
        """
        Test removing a product by admin.
        """
        self.create_user('admin', 'admin')
        self.db.query(User).filter_by(username='admin').update({"is_admin": True})  # Set admin flag to True
        
        product = self.create_product('Test Product', 'Test Description', 10.0, 100)
        product = self.db.get(Product, product.id)

        with self.client as client:
            response = client.post('/login', data={'username': 'admin', 'password': 'admin'}, follow_redirects=True)
            self.assertIn(b'Logout', response.data)
            response = client.post(f'/admin/products/delete/{product.id}', follow_redirects=True)        
            self.assertIn(b'Product deleted successfully.', response.data)
            deleted_product = self.db.get(Product, product.id)
            self.assertIsNone(deleted_product)  # The product should no longer be in the database


    # 4. Product View Test (for Users)
    def test_user_view_all_products(self): # GREEN
        """
        Test viewing all products by a user.
        """
        self.create_product('Test Product', 'Test Description', 10.0, 100)

        with self.client as client:
            response = client.get('/', follow_redirects=True)
            self.assertIn(b'Test Product', response.data)

    # 5. Cart and Order Test
    def test_add_product_to_cart(self): # GREEN
        """
        Test adding a product to the cart.
        """
        #self.create_user('testuser1', 'testpass1')
        
        self.create_product('Test Product', 'Test Description', 10.0, 100)

        db_product = self.db.query(Product).filter_by(name='Test Product').first()
        assert db_product is not None  # Ensure the product is added to the DB
        
        with self.client as client:
            response = client.post('/login', data={'username': 'testuser', 'password': 'testpass'}, follow_redirects=True)
            self.assertIn(b'Logout', response.data)
            response = client.get(f'/cart/add/{db_product.id}', follow_redirects=True)

            self.assertIn(b'Test Product', response.data)
            self.assertIn(b'Cart', response.data)  # Check if cart is updated


    def test_view_cart_contents(self): # GREEN
        """
        Test viewing the cart contents.
        """
        #self.create_user('testuser2','testpass2')
        self.create_product('Test Product', 'Test Description', 10.0, 100)

        db_product = self.db.query(Product).filter_by(name='Test Product').first()
        assert db_product is not None  # Ensure the product is added to the DB

        with self.client as client:
            response = client.post('/login', data={'username': 'testuser', 'password': 'testpass'}, follow_redirects=True)
            self.assertIn(b'Logout', response.data)
            response = client.get(f'/cart/add/{db_product.id}', follow_redirects=True)

            self.assertIn(b'Test Product', response.data)
            self.assertIn(b'Cart', response.data)  # Check if cart is updated


    def test_place_order(self): # GREEN (1 WARNING FIXED: datetime import timezone. datetime.utcnow is DEPRECATED)
        """
        Test placing an order and clearing the cart.
        """

        #self.create_user('testuser','testpass')
        self.create_product('Test Product', 'Test Description', 10.0, 100)

        db_product = self.db.query(Product).filter_by(name='Test Product').first()
        assert db_product is not None  

        with self.client as client:
            response = client.post('/login', data={'username': 'testuser', 'password': 'testpass'}, follow_redirects=True)
            self.assertIn(b'Logout', response.data)

            response = client.get(f'/cart/add/{db_product.id}', follow_redirects=True)
            self.assertIn(b'Added Test Product to your cart.', response.data)

            response = client.get('/order/place', follow_redirects=True)
            self.assertIn(b'Order placed successfully.', response.data)

            response = client.get('/cart', follow_redirects=True)
            self.assertIn(b'Your cart is empty.', response.data)


    def test_order_storage_after_placing(self):  # GREEN
        """
        Test that the order is properly saved in the database after placement.
        """
        product = self.create_product('Test Product', 'Test Description', 10.0, 100)

        product = self.db.get(Product, product.id)

        response = self.login_user('testuser', 'testpass')
        self.assertIn(b'Logout', response.data)  # Verify login was successful

        self.place_order_and_verify_cart(self.client, product.id)

        user_id = self.db.query(User).filter_by(username='testuser').first().id

        order = self.db.query(Order).filter_by(user_id=user_id).first()
        self.assertIsNotNone(order, "Order was not stored in the database.")

    # 6. Error Handling Test
    def test_unauthorized_access_to_admin_routes(self): # GREEN
        """
        Test unauthorized access to admin routes.
        """
        self.create_user('user','userpass')

        with self.client as client:
            response = self.login_user('user', 'userpass')
            self.assertIn(b'Logout', response.data)

            response = client.get('/admin/products', follow_redirects=True)
            self.assertIn(b'Admin access required.', response.data)


    def test_invalid_product_id_when_placing_order(self):
        """
        Test placing an order with an invalid product ID.
        """
        response = self.login_user('testuser', 'testpass')
        self.assertIn(b'No products available.', response.data)

    def test_invalid_input_during_registration(self): # GREEN
        """
        Test invalid input during user registration.
        """
        with self.client as client:
            response = client.post('/register', data={
                'username': '',  # Empty username
                'password': 'validPassword123'
            }, follow_redirects=True)
            self.assertIn(b'Username cannot be empty.', response.data)

    # 7. Persistence Test
    def test_data_saved_in_database(self): # GREEN
        """
        Test data persistence in the database.
        """
        user_from_db = self.db.query(User).filter_by(username='testuser').first()
        self.assertIsNotNone(user_from_db)
        self.assertEqual(user_from_db.username, 'testuser')

    def test_data_retrieval_after_restart(self): # GREEN
        """
        Test data retrieval after the database is restarted.
        """
    # Simulate database restart by closing and reopening the session
        self.db.close()
        self.Session.remove()
        self.db = self.Session()

        user_from_db = self.db.query(User).filter_by(username='testuser').first()
        self.assertIsNotNone(user_from_db)
        self.assertEqual(user_from_db.username, 'testuser')

