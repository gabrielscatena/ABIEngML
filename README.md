# ABIEngML

# Plan of Action for Simple E-commerce Backend

## 1. Requirements
1.1 User Management:
   - Users should be able to register and log in securely.
   - Passwords will be hashed using a library like `werkzeug`.
   - Users should have a profile page to manage their account details.
   - **Learned in the fly**: Secure password storage requires using strong hashing algorithms. Use token like JWT for security.

   
1.2 Product Management:
   - Admins should be able to perform CRUD operations on products.
   - Regular users should only be able to view product lists and details.
   - **Learned in the fly**: Implementing role-based access control (RBAC) using decorators.

1.3 Cart and Order Management:
   - Users can add products to a cart and manage the cart's content.
   - Users can place an order, which clears the cart and stores the order.
   - **Learned in the fly**: Use sessions or a simple dictionary structure to manage cart data per user.

1.4 Data Persistence:
   - Use a file-based database (JSON or SQLite) to store user, product, cart, and order data.
   - **Learned in the fly**: File handling and managing JSON data with Python's `json` module.

1.5 Error Handling:
   - Handle invalid inputs (e.g., malformed product IDs, missing fields in forms).
   - Prevent unauthorized access to admin routes.
   - **Learned in the fly**: Implementing custom error handling classes and using HTTP status codes.

1.6 Testing:
   - Unit tests for user registration, product addition, and order placement.
   - **Learned in the fly**: Testing frameworks like `unittest` or `pytest` for unit tests.
   
1.7 Version Control:
   - Use Git to track changes and commits.

---

## 2. Create a GitHub Repository
- Initialize a GitHub repository for the project.
- Set up the repository with an appropriate structure:
  - `app.py` for the application logic.
  - `models.py` for database models (e.g., user, product, order).
  - `tests.py` for unit tests.
  - `README.md` to explain the project setup and usage... etc.

---

## 3. Create Files and Directories with `create_files.py`
- Write a script (`create_files.py`) to create the following files and directories:
  - `app.py` — Core application logic.
  - `models.py` — Classes for User, Product, Cart, and Order.
  - `tests.py` — Unit tests for all features.
  - `templates/` — Directory to store the HTML templates for rendering views.
  - `static/` — Directory for static CSV.

---

## 4. Write Tests in `tests.py`
- **Tests to be Done:**
  1. **User Registration Test:**
     - Test if a user can register with valid details.
     - Test invalid registration (e.g., weak password, duplicate username).
     - Test if passwords are hashed correctly.
     
  2. **Login Test:**
     - Test successful login with correct credentials.
     - Test failed login with incorrect credentials.
     
  3. **Product Management Test (for Admins):**
     - Test adding a product (only admin).
     - Test editing a product (only admin).
     - Test removing a product (only admin).
     
  4. **Product View Test (for Users):**
     - Test viewing all products.
     - Test viewing a specific product’s details.
     - Test if non-admin users cannot edit or delete products.
     
  5. **Cart and Order Test:**
     - Test adding products to the cart.
     - Test viewing the cart contents.
     - Test placing an order and clearing the cart.
     - Test if the order is stored correctly after placing.
     
  6. **Error Handling Test:**
     - Test unauthorized access to admin routes.
     - Test invalid product IDs when placing an order.
     - Test invalid input during registration.
     
  7. **Persistence Test:**
     - Test that data is correctly saved in the JSON database.
     - Test retrieval of data (user, product, cart, order) after restarting the app.

---

## 5. Write the Core Application Logic in `app.py`
- **Concept:**
  - Use object-oriented programming (OOP) principles like inheritance to create reusable components.
  - Design patterns: Singleton (for managing the database connection), Factory (for creating product or user objects), and Decorator (for adding authentication), Strategy could be used also.
  
- **App Logic:**
  - Define classes for each entity:
    - `User`: Handles user registration, login, and data storage.
    - `Product`: Manages product data (CRUD operations).
    - `Cart`: Handles the logic for adding/removing items and placing orders.
    - `Order`: Stores order details after checkout.
  - Implement role-based authentication, using decorators to manage access (e.g., admin routes).
  - Routes:
    - `/register` for user registration.
    - `/login` for user authentication.
    - `/products` to view all products.
    - `/cart` to view and manage the cart.
    - `/checkout` to place an order.
    
- **HTML Files:**
  - For basic UI rendering, create HTML templates for registration, login, product listing, cart, and order pages.
  - Use simple HTML forms to gather data (e.g., user details, product selection, checkout).
  - **Learned in the fly**: Flask or other simple web frameworks can help quickly integrate routing and rendering HTML templates.

---

## 6. Integrate and Test
- Integrate the application logic with the tests, ensuring all functionality works as expected.
- Debug any issues and make necessary adjustments.
- Ensure all tests pass and the system handles edge cases effectively.

---

## 7. Finalize and Document
- Ensure code is well-documented with comments explaining the logic.
- Prepare a comprehensive `README.md`:
  - Project description.
  - How to set up and run the app.
  - How to test the app.
  - Assumptions made.
  - Any learnings encountered during implementation (e.g., challenges with hashing passwords, implementing role-based access).
  
- Create a final commit in Git and push the code to the repository.
