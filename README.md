# ABEESnBev - Simple E-Commerce Backend

## **Table of Contents**
- [Introduction](#introduction)
- [Plan of Action for Simple E-commerce Backend](#plan-of-action-for-simple-e-commerce-backend)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Project Folder Structure](#project-folder-structure)
- [Design Decisions](#design-decisions)
- [Known Issues](#known-issues)
- [Future Improvements](#future-improvements)
- [License](#license)

---

## **Introduction**
**ABEESnBev** is a simple e-commerce backend system designed to simulate an online shopping experience. Users can register, browse products, add items to their carts, and place orders. Administrators can manage products, ensuring only authorized actions are taken.

This project demonstrates the implementation of Python-based web development with proper testing, modularity, and clean architecture principles.

---
## **Plan of Action for Simple E-commerce Backend**

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
  - Use object-oriented programming (OOP) principles and create reusable components.
  - Design patterns: Singleton (for managing the database connection), Factory (for creating product or user objects), and Decorator (for adding authentication), Strategy should be used also.
  - Use MVC (Model-View-Controller) to create the classes
  
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

--- 

## **Features**
### **User Management**
- User registration and login.
- Secure password storage with hashing (bcrypt).
- Role-based access control (admin vs regular users).

### **Product Management**
- Admins can add, edit, and delete products.
- Regular users can view a list of products and their details.

### **Cart and Order Management**
- Users can add items to a cart.
- Users can view their cart, place orders, and clear their cart after placing an order.
- Order history is stored for future reference.

### **Error Handling**
- Comprehensive error handling for invalid inputs, unauthorized access, and missing products.
- Custom error pages for `403 Forbidden` and `404 Not Found`.

### **Testing**
- Unit tests for critical functions such as user registration, product addition, and order placement.
- Test coverage includes authentication, CRUD operations, and cart functionalities.

---

## **Technologies Used**
- **Backend Framework**: Flask
- **Database**: SQLite (persistent and lightweight database)
- **Authentication**: Flask-JWT-Extended
- **Frontend**: HTML, CSS (with Jinja2 templating for dynamic content)
- **Testing**: Pytest
- **Other**:
  - SQLAlchemy (ORM for database management)

---

## **Installation**

### Prerequisites
- Python 3.10 or higher
- pip (Python package installer)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/gabrielscatena/ABIEngML.git
   cd ABIEngML
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # For Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

---

## **Usage**

### Admin Panel
- Log in with an admin account.
- Access the product management interface via the "Admin Dashboard".
- Add, edit, or delete products.

### Shopping
- Register as a user.
- Browse products and add them to your cart.
- Place an order and view your order history.

---

## **Testing**

### Run Tests
To run all unit tests, execute the following command:
```bash
pytest tests.py
```

### Coverage
- Tests are written for:
  - User registration and login.
  - Admin product management.
  - Cart and order functionalities.
- Ensure the codebase is covered with meaningful tests to avoid regressions.

---
## **Project Folder Structure**
```bash
.env  # .env
.env.example # .env is in .gitignore
.git/
README.md  # README.md
__init__.py  # __init__.py
app.py  # app.py
controllers/
│   ├── __init__.py  # __init__.py
│   ├── auth_controller.py  # auth_controller.py
│   ├── cart_controller.py  # cart_controller.py
│   ├── order_controller.py  # order_controller.py
│   ├── product_controller.py  # product_controller.py
database.py  # database.py
docs/
│   ├── Approach_Decisions.md  # Approach_Decisions.md
│   ├── CASE_ENG_ML.md  # CASE_ENG_ML.md
│   ├── LICENSE  # LICENSE
│   ├── steps.md  # steps.md
ecommerce.db  # ecommerce.db
generate_folder_structure.py  # generate_folder_structure.py
models.py  # models.py
requirements.txt  # requirements.txt
scripts/
│   ├── create_admin.py  # create_admin.py
│   ├── create_files.py  # create_files.py
│   ├── create_files_strategy_and_MVC.py  # create_files_strategy_and_MVC.py
│   ├── generate_folder_structure.py  # generate_folder_structure.py
static/
│   ├── styles.css  # styles.css
strategies/
│   ├── __init__.py  # __init__.py
│   ├── auth_strategy.py  # auth_strategy.py
│   ├── jwt_auth_strategy.py  # jwt_auth_strategy.py
templates/
│   ├── 403.html  # 403.html
│   ├── 404.html  # 404.html
│   ├── add_product.html  # add_product.html
│   ├── admin_products.html  # admin_products.html
│   ├── base.html  # base.html
│   ├── cart.html  # cart.html
│   ├── edit_product.html  # edit_product.html
│   ├── footer.html  # footer.html
│   ├── header.html  # header.html
│   ├── index.html  # index.html
│   ├── login.html  # login.html
│   ├── orders.html  # orders.html
│   ├── register.html  # register.html
tests.py  # tests.py
```

**Example of content and variable in .env file**
```bash
SECRET_KEY=
SQLALCHEMY_DATABASE_URI=
JWT_SECRET_KEY=
JWT_TOKEN_LOCATION=
JWT_COOKIE_SECURE=
JWT_COOKIE_CSRF_PROTECT=
JWT_COOKIE_SAMESITE=
JWT_ACCESS_COOKIE_PATH=
JWT_COOKIE_CSRF_PROTECT=
```
---

## **Design Decisions**

1. **Authentication with JWT**:
   - JWT tokens ensure secure and stateless authentication.
   - Simplifies session management in distributed systems.

2. **ORM with SQLAlchemy**:
   - Using SQLAlchemy improves maintainability and reduces direct database query handling.

3. **Separation of Concerns**:
   - Separate routes for user, admin, product, and cart functionalities.
   - Templates and static assets are modularized for easy customization.

4. **Unit Testing with Pytest**:
   - Extensive test coverage ensures critical functionalities are robust.
   - Tests validate edge cases like invalid inputs and unauthorized access.

---

## **Known Issues**
- Cart total is not displayed on the cart page.
- Flash messages lack visual styling (e.g., success vs error feedback).
- Application is not fully responsive on mobile devices.
- No payment option.
---

## **Future Improvements**
1. **Enhanced Styling**:
   - Add mobile responsiveness using media queries.
   - Style flash messages to provide better feedback.
2. **Order History**:
   - Create a dedicated page for users to view their past orders.
3. **Pagination**:
   - Add pagination for product lists to handle a larger dataset.
4. **Error Handling**:
   - Add logging for server-side errors.

---

## **License**
## License
This project is licensed under the MIT License. See the [LICENSE](./docs/LICENSE) file for details.
```
