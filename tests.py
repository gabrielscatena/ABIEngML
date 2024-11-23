# tests.py        

import unittest
import uuid
from app import app
from models import Base, User, Product, CartItem, Order, OrderItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from werkzeug.security import generate_password_hash, check_password_hash


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

    def tearDown(self):
        """
        Clean up after each test.
        """
        self.db.close()
        self.Session.remove()
        Base.metadata.drop_all(bind=self.engine)
        self.app_context.pop()

    # 1. User Registration Test GREEN
    def test_user_registration_valid_details(self):
        """
        Test user registration with valid details.
        """
        unique_username = f'testuser{uuid.uuid4()}'
        with self.client as client:
            response = client.post('/register', data={
                'username': unique_username,
                'password': 'validPassword123'
            }, follow_redirects=True)
            self.assertIn(b'Registration successful. Please log in.', response.data)

    def test_user_registration_invalid_password(self): # GREEN
        """
        Test user registration with an invalid password (e.g., too short).
        """
        unique_username = f'testuser{uuid.uuid4()}'
        with self.client as client:
            response = client.post('/register', data={
                'username': unique_username,
                'password': '123'
            }, follow_redirects=True)
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
            response = client.post('/register', data={
                'username': unique_username,
                'password': password
            }, follow_redirects=True)
            user = self.db.query(User).filter_by(username=unique_username).first()
            self.assertTrue(check_password_hash(user.password_hash, password))

    # 2. Login Test
    def test_successful_login(self): # GREEN
        """
        Test login with valid credentials.
        """
        test_user = User(username='testuser', password_hash=generate_password_hash('testpass', method='scrypt'))
        self.db.add(test_user)
        self.db.commit()

        with self.client as client:
            response = client.post('/login', data={
                'username': 'testuser',
                'password': 'testpass'
            }, follow_redirects=True)
            self.assertIn(b'Logout', response.data)

    def test_failed_login_invalid_credentials(self): #GREEN
        """
        Test login with invalid credentials (wrong password or username).
        """
        test_user = User(username='testuser', password_hash=generate_password_hash('testpass', method='scrypt'))
        self.db.add(test_user)
        self.db.commit()

        with self.client as client:
            response = client.post('/login', data={
                'username': 'testuser',
                'password': 'wrongpassword'
            }, follow_redirects=True)
            self.assertIn(b'Invalid username or password.', response.data)

    # 3. Product Management Test (for Admins)
    def test_admin_edit_product(self):
        """
        Test editing a product by admin.
        """
        # Create admin user
        admin_user = User(username='admin', password_hash=generate_password_hash('admin', method='scrypt'), is_admin=True)
        self.db.add(admin_user)
        self.db.commit()

        product = Product(name='Test Product', description='Test Description', price=10.0, stock=100)
        self.db.add(product)
        self.db.commit()

        product = self.db.query(Product).get(product.id)

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

            updated_product = self.db.query(Product).get(product.id)
            self.assertEqual(updated_product.name, 'Updated Product')
            self.assertEqual(updated_product.description, 'Updated Description')
            self.assertEqual(updated_product.price, 12.0)
            self.assertEqual(updated_product.stock, 200)

    def test_admin_edit_product(self): # GREEN
        """
        Test editing a product by admin.
        """
        admin_user = User(username='admin', password_hash=generate_password_hash('admin', method='scrypt'), is_admin=True)
        self.db.add(admin_user)
        self.db.commit()
        product = Product(name='Test Product', description='Test Description', price=10.0, stock=100)
        self.db.add(product)
        self.db.commit()
        #product = self.db.query(Product).get(product.id) # DEPRECATED
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
        admin_user = User(username='admin', password_hash=generate_password_hash('admin', method='scrypt'), is_admin=True)
        self.db.add(admin_user)
        self.db.commit()
        product = Product(name='Test Product', description='Test Description', price=10.0, stock=100)
        self.db.add(product)
        self.db.commit()
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
        product = Product(name='Test Product', description='Test Description', price=10.0, stock=100)
        self.db.add(product)
        self.db.commit()

        with self.client as client:
            response = client.get('/', follow_redirects=True)
            self.assertIn(b'Test Product', response.data)

    # def test_user_view_product_details(self): # Already showing all details in Home page
    #     """
    #     Test viewing product details by a user.


    # def test_non_admin_cannot_edit_or_delete_product(self): # Users (is_admin=False) will not see any option to edit or delete products
    #     """
    #     Test that non-admin users cannot edit or delete products.
    #     """


    # 5. Cart and Order Test
    def test_add_product_to_cart(self): # GREEN
        """
        Test adding a product to the cart.
        """
        test_user = User(username='testuser1', password_hash=generate_password_hash('testpass1', method='scrypt'))
        self.db.add(test_user)
        self.db.commit()
        
        product = Product(name='Test Product', description='Test Description', price=10.0, stock=100)
        self.db.add(product)
        self.db.commit()

        db_product = self.db.query(Product).filter_by(name='Test Product').first()
        assert db_product is not None  # Ensure the product is added to the DB
        
        with self.client as client:
            response = client.post('/login', data={'username': 'testuser1', 'password': 'testpass1'}, follow_redirects=True)
            self.assertIn(b'Logout', response.data)
            response = client.get(f'/cart/add/{db_product.id}', follow_redirects=True)

            self.assertIn(b'Test Product', response.data)
            self.assertIn(b'Cart', response.data)  # Check if cart is updated


    def test_view_cart_contents(self): # GREEN
        """
        Test viewing the cart contents.
        """
        test_user = User(username='testuser2', password_hash=generate_password_hash('testpass2', method='scrypt'))
        self.db.add(test_user)
        self.db.commit()

        product = Product(name='Test Product', description='Test Description', price=10.0, stock=100)
        self.db.add(product)
        self.db.commit()

        db_product = self.db.query(Product).filter_by(name='Test Product').first()
        assert db_product is not None  # Ensure the product is added to the DB

        with self.client as client:
            response = client.post('/login', data={'username': 'testuser2', 'password': 'testpass2'}, follow_redirects=True)
            self.assertIn(b'Logout', response.data)
            response = client.get(f'/cart/add/{db_product.id}', follow_redirects=True)

            self.assertIn(b'Test Product', response.data)
            self.assertIn(b'Cart', response.data)  # Check if cart is updated


    def test_place_order(self): # GREEN (1 WARNING FIXED: datetime import timezone. datetime.utcnow is DEPRECATED)
        """
        Test placing an order and clearing the cart.
        """

        test_user = User(username='testuser3', password_hash=generate_password_hash('testpass3', method='scrypt'))
        self.db.add(test_user)
        self.db.commit()

        product = Product(name='Test Product', description='Test Description', price=10.0, stock=100)
        self.db.add(product)
        self.db.commit()

        db_product = self.db.query(Product).filter_by(name='Test Product').first()
        assert db_product is not None  # Ensure the product is added to the DB

        with self.client as client:
            response = client.post('/login', data={'username': 'testuser3', 'password': 'testpass3'}, follow_redirects=True)
            self.assertIn(b'Logout', response.data)

            response = client.get(f'/cart/add/{db_product.id}', follow_redirects=True)
            self.assertIn(b'Product added to cart.', response.data)

            response = client.get('/order/place', follow_redirects=True)
            self.assertIn(b'Order placed successfully.', response.data)

            response = client.get('/cart', follow_redirects=True)
            self.assertIn(b'Your cart is empty.', response.data)


    def test_order_storage_after_placing(self): # GREEN (1 WARNING FIXED: product = self.db.query(Product).get(product.id) is DEPRECATED)
        """
        Test that the order is properly saved in the database after placement.
        """
        test_user = User(username='testuser4', password_hash=generate_password_hash('testpass4', method='scrypt'))
        self.db.add(test_user)
        self.db.commit()

        product = Product(name='Test Product', description='Test Description', price=10.0, stock=100)
        self.db.add(product)
        self.db.commit()
    
        # product = self.db.query(Product).get(product.id) DEPRECATED
        product = self.db.get(Product, product.id)

        with self.client as client:
            response = client.post('/login', data={'username': 'testuser4', 'password': 'testpass4'}, follow_redirects=True)
            self.assertIn(b'Logout', response.data)
    
            response = client.get(f'/cart/add/{product.id}', follow_redirects=True)
            self.assertIn(b'Product added to cart.', response.data)

            response = client.get('/order/place', follow_redirects=True)
            self.assertIn(b'Order placed successfully.', response.data)

            response = client.get('/cart', follow_redirects=True)
            self.assertIn(b'Your cart is empty.', response.data)


    # 6. Error Handling Test
    def test_unauthorized_access_to_admin_routes(self): # GREEN
        """
        Test unauthorized access to admin routes.
        """
        non_admin_user = User(username='user', password_hash=generate_password_hash('userpass', method='scrypt'), is_admin=False)
        self.db.add(non_admin_user)
        self.db.commit()

        with self.client as client:
            response = client.post('/login', data={'username': 'user', 'password': 'userpass'}, follow_redirects=True)
            self.assertIn(b'Logout', response.data)

            response = client.get('/admin/products', follow_redirects=True)
            self.assertIn(b'Admin access required.', response.data)

    def test_invalid_product_id_when_placing_order(self): # GREEN
        """
        Test placing an order with an invalid product ID.
        """
        test_user = User(username='testuser5', password_hash=generate_password_hash('testpass5', method='scrypt'))
        self.db.add(test_user)
        self.db.commit()

        with self.client as client:
            response = client.post('/login', data={'username': 'testuser5', 'password': 'testpass5'}, follow_redirects=True)
            self.assertIn(b'Logout', response.data)

            response = client.get('/order/place?product_id=9999', follow_redirects=True)  # Non-existent product
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
        test_user = User(username='testuser6', password_hash=generate_password_hash('testpass6', method='scrypt'))
        self.db.add(test_user)
        self.db.commit()

        user_from_db = self.db.query(User).filter_by(username='testuser6').first()
        self.assertIsNotNone(user_from_db)
        self.assertEqual(user_from_db.username, 'testuser6')

    def test_data_retrieval_after_restart(self): # GREEN
        """
        Test data retrieval after the database is restarted.
        """
        test_user = User(username='testuser7', password_hash=generate_password_hash('testpass7', method='scrypt'))
        self.db.add(test_user)
        self.db.commit()

        # Simulate database restart by closing and reopening the session
        self.db.close()
        self.Session.remove()
        self.db = self.Session()

        user_from_db = self.db.query(User).filter_by(username='testuser7').first()
        self.assertIsNotNone(user_from_db)
        self.assertEqual(user_from_db.username, 'testuser7')
