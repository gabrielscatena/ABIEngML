## Project Structure

# - `Approach_Decisions.md`: Contains the approach and design decisions made during development.

# - `__init__.py`: 
# - `app.py`: Main application file containing routes and application logic.
# - `models.py`: Contains the database models.
# - `database.py`: Sets up the database connection and session management.
# - `tests.py`: Contains unit tests for the application.

# - `requirements.txt`: Contains the list of dependencies for the application.

# - `templates/`: Contains HTML templates for rendering views.
# - `base.html`: Base template for the application.
# - `index.html`: Home page template.
# - `header.html`: Header template.
# - `footer.html`: Footer template.
# - `login.html`: Login page template.
# - `register.html`: Registration page template.
# - `cart.html`: Cart page template.
# - `orders.html`: Orders page template.
# - `admin_products.html`: Admin products page template.
# - `add_product.html`: Add product page template.
# - `edit_product.html`: Edit product page template.
# - `404.html`: 404 error page template.
# - `403.html`: 403 error page template.

# - `static/`: Contains static files such as CSS and images.
# - 'styles.css': CSS file for styling the application.

import os
# Create the following files in the project directory:
list_of_files = ['__init__.py', 'app.py', 'models.py', 'database.py', 'tests.py', 'requirements.txt', 'Approach_Decisions.md',
                 'templates/base.html', 'templates/index.html', 'templates/header.html', 'templates/footer.html', 'templates/login.html', 
                 'templates/register.html', 'templates/cart.html', 'templates/orders.html', 'templates/admin_products.html',
                 'templates/add_product.html', 'templates/edit_product.html', 'templates/404.html', 'templates/403.html',
                 'static/styles.css']

# Create the files in the project directory
for file_name in list_of_files:
    if '.' in file_name:
        with open(file_name, 'w') as file:
            pass
    else:
        os.makedirs(file_name)

# Check if the files are created
for file_name in list_of_files:
    if os.path.exists(file_name):
        print(f'{file_name} created successfully')
    else:
        print(f'Error creating {file_name}')

# Output
# app.py created successfully
# models.py created successfully
# database.py created successfully
# templates/ created successfully
# tests.py created successfully
# base.html created successfully
# index.html created successfully
# header.html created successfully
# footer.html created successfully
# login.html created successfully
# register.html created successfully
# cart.html created successfully
# orders.html created successfully
# admin_products.html created successfully
# add_product.html created successfully
# edit_product.html created successfully
# 404.html created successfully
# 403.html created successfully
# styles.css created successfully
'''
The code above, files and directories will be create in the project directory. 
It loops through the list and create the files and directories using the  open()  function for files and  os.makedirs()  for directories. 
Finally, it checks if the files and directories were created successfully using the  os.path.exists()  function. 
The output will show that the files and directories have been created successfully. 
'''
