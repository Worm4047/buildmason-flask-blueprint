# {{cookiecutter.project_name}}

This is a simple Flask project that allows user login into the web application. We make use several components
- Flask-Login library for session management
- built-in Flask utility for hashing passwords
- Add protected pages to the app for logged in users only
- Use Flask-SQLAlchemy to create a User model
- Create sign-up and login forms for the users to create accounts and log in
- Flash error messages back to users when something goes wrong
- Use information from the user’s account to display on the profile page

## Getting Started

### Prerequisites

- Python 3.x
- [Virtualenv](https://virtualenv.pypa.io/)


# Project Structure
```
{{cookiecutter.project_name}}/
├── app
│   ├── __init__.py
│   ├── models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── main.py
│   └── templates
│       ├── base.html
│       ├── index.html
│       ├── login.html
│       ├── profile.html
│       └── signup.html
├── requirements.txt
├── run.py
└── tests
    ├── __init__.py
    ├── models
    │   ├── __init__.py
    │   └── test_models.py
    └── routes
        ├── test_auth.py
        └── test_main.py

```

# Components
## Models
The models directory contains SQLAlchemy models. In this example, there is a User model defined in app/models/user.py. This model represents a basic user with id, username, password and email fields.

## Routes
The services directory contains service classes that encapsulate business logic related to the models. `auth.py` takes care of login and signup. `main.py` renders profile and index page

## Main App
The main Flask application is defined in __init__.py. It configures the Flask app, sets up the database, setup login manager to handle user sessions and registers blueprint handlers

# How to Run
## Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Install dependencies:
```
pip install -r requirements.txt
```

## Run the Flask app:
```
(venv) ➜  python3 run.py
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 933-952-624
```
The app will be accessible at http://127.0.0.1:5000/

## How to Test

### Activate the virtual environment (if not activated):

```
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Run the tests:
```
(venv) ➜ pytest tests
======================================================= test session starts =======================================================
platform darwin -- Python 3.11.7, pytest-7.4.4, pluggy-1.3.0
rootdir: /Users/abhi/Developer/MyFlaskBluePrintApp
collected 12 items                                                                                                                

tests/models/test_models.py ..                                                                                              [ 16%]
tests/routes/test_auth.py .......                                                                                           [ 75%]
tests/routes/test_main.py ...                                                                                               [100%]

======================================================= 12 passed in 2.85s ========================================================
```

This script will discover and run all test files in the tests directory.

---
This README provides a basic overview of the project structure, components, and instructions on how to run and test the Flask app. Customize it further based on your project's specific details and requirements.

