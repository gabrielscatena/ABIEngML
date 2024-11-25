import os

# List of files and directories to create
list_of_files = [

    # Controllers
    'controllers/__init__.py',
    'controllers/auth_controller.py',
    'controllers/product_controller.py',
    'controllers/cart_controller.py',
    'controllers/order_controller.py',
    # Strategies
    'strategies/__init__.py',
    'strategies/auth_strategy.py',
    'strategies/jwt_auth_strategy.py']


# Create files and directories
for file_path in list_of_files:
    # Split the file path to get directory names
    dirs = os.path.dirname(file_path)
    # Create directories if they don't exist
    if dirs and not os.path.exists(dirs):
        os.makedirs(dirs)
    # Create the file
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            pass

# Check if the files are created
for file_path in list_of_files:
    if os.path.exists(file_path):
        print(f'{file_path} created successfully')
    else:
        print(f'Error creating {file_path}')

### OUTPUT
# controllers/__init__.py created successfully
# controllers/auth_controller.py created successfully
# controllers/product_controller.py created successfully
# controllers/cart_controller.py created successfully
# controllers/order_controller.py created successfully
# strategies/__init__.py created successfully
# strategies/auth_strategy.py created successfully
# strategies/jwt_auth_strategy.py created successfully