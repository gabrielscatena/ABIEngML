## Project Structure
# - `app.py`: Main application file containing routes and application logic.
# - `models.py`: Contains the database models.
# - `database.py`: Sets up the database connection and session management.
# - `templates/`: Contains HTML templates for rendering views.
# - `static/`: Contains static files such as CSS and images.
# - `tests.py`: Contains unit tests for the application.

import os
# Create the following files in the project directory:
list_of_files = ['app.py', 'models.py', 'database.py', 'templates/', 'tests.py', 'requirements.txt', 'README.md', 'Approach_Decisions.md']

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
'''
In the code above, files and directories will be create in the project directory. 
It loops through the list and create the files and directories using the  open()  function for files and  os.makedirs()  for directories. 
Finally, it checks if the files and directories were created successfully using the  os.path.exists()  function. 
The output will show that the files and directories have been created successfully. 
'''