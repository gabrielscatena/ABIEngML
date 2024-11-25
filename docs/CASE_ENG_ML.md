# Simple E-commerce Backend

## Problem Statement:
Create a backend system for a simple e-commerce platform where users can register, view a list of products, add products to a cart, and place an order. You should also implement basic user authentication and ensure that users can only view and manipulate their own data.

## Requirements:

### User Management:
- Users should be able to register, log in, and manage their account.
- Passwords should be securely stored (e.g., hashed).

### Product Management:
- Admins should be able to add, edit, and remove products.
- Regular users should be able to view a list of products and details of each product.

### Cart and Order Management:
- Users should be able to add products to a cart.
- Users should be able to view their cart and place an order.
- Once an order is placed, the cart should be cleared, and the order details should be saved.

### Data Persistence:
- Store user, product, cart, and order data in a file-based database (e.g., JSON, SQLite).

### Testing:
- Write basic unit tests for persona-critical functions like user registration, product addition, and order placement.

### Error Handling:
- Handle common errors such as invalid inputs, unauthorized access, and unavailable products.

### Version Control:
- Use Git to manage your project. Make regular commits and document your work in a README file.

## Tested Competencies:

### Problem-Solving Skills:
- The challenge requires designing and implementing a solution that involves multiple components (users, products, orders), testing the candidate’s ability to break down complex problems using Software Engineering best practices.

### Programming Fundamentals:
- The candidate will need to use object-oriented design, design patterns, basic data structures (e.g., lists, dictionaries), control flow, and functions to manage the application’s logic.

### Code Quality:
- The candidate’s ability to write clean, readable code is tested by the need to organize different components of the application, adhere to DRY (Don't Repeat Yourself) principles, and provide comments where necessary indicating input parameters, return values, and ensuring function signatures contain variable annotations.

### Testing and Debugging:
- Writing unit tests for key functions assesses testing skills, while debugging the implementation is necessary to ensure the application works as expected. TDD is validated and preferred by reviewing the commit history.

### Language Proficiency:
- Demonstration of Python proficiency by implementing the application with correct syntax, using appropriate libraries, and following best practices (e.g., comments, variable annotations, list comprehensions, etc.).

### Version Control:
- Use of Git can be assessed by reviewing the solution’s commit history indicating branch management, and overall use of basic version control.

### Communication Skills:
- Explaining the solution approach in the well-formatted `README.md`, documenting their implementation and should describe any assumptions made. (Often problems are not well-formed and require a bit of decision-making. Use this as an opportunity to show how well you identify missing or incomplete information and press forward with a solution that is under test.)

### Adaptability and Learning:
- If unfamiliar with certain aspects (like user authentication or writing tests), use the `README.md` to identify areas you had to look up to learn on the fly, as a demonstration of the ability to adapt.

## Challenge Instructions:

### Anticipated Time Required:
Less than 4 hours

### Tools Required:
- Python
- The IDE of your choosing
- Internet access
- Git

### Deliverables:
1. The codebase in a compressed file containing the entire git repository.
    - NOTE: Be sure to include the `.git` file for inspection of commits.
2. A `README.md` file containing at a minimum:
    - A general project description
    - How to set up and run the application
    - How to test the application
    - Any assumptions made
    - Any learnings you had to do to design and/or implement the solution.
3. A description of the approach taken, and any trade-offs or decisions made during implementation.
    - NOTE: Consider discussing the use of Object-Oriented design, leveraging Python Protocols over inheritance (recommended), Design Patterns, and anything you believe would be a good callout for this challenge illustrating your programming, systems thinking, and general expertise.