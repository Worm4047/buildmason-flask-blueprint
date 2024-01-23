import unittest
from flask import Flask, url_for
from flask_testing import TestCase
from werkzeug.security import generate_password_hash
from flask_login import LoginManager, current_user, login_user
from app import create_app
from app.models.user import User, db

class TestAuthRoutes(TestCase):

    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        return app

    def setUp(self):
        db.create_all()
        # Mocking Flask-Login's LoginManager for testing
        login_manager = LoginManager()
        login_manager.init_app(self.app)
        login_manager.login_view = 'auth.login'
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login_page_loads(self):
        response = self.client.get(url_for('auth.login'))
        self.assert200(response)
        self.assertTemplateUsed('login.html')

    def test_login_successful(self):
        user = User(email='test@example.com', name='Test User', password=generate_password_hash('password123'))
        db.session.add(user)
        db.session.commit()

        response = self.client.post(url_for('auth.login'), data={'email': 'test@example.com', 'password': 'password123', 'remember': 'on'}, follow_redirects=True)
        self.assertIn(b'Welcome', response.data)

    def test_login_invalid_credentials(self):
        response = self.client.post(url_for('auth.login'), data={'email': 'nonexistent@example.com', 'password': 'wrongpassword'})
        self.assertMessageFlashed('Please check your login details and try again.')

    def test_logout(self):
        self.client.get(url_for('auth.logout'))
        response = self.client.get(url_for('main.profile'),  follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_signup_page_loads(self):
        response = self.client.get(url_for('auth.signup'))
        self.assert200(response)
        self.assertTemplateUsed('signup.html')

    def test_signup_successful(self):
        response = self.client.post(url_for('auth.signup'), data={'email': 'newuser@example.com', 'name': 'New User', 'password': 'newpassword'},  follow_redirects=True)
        self.assertIsNotNone(User.query.filter_by(email='newuser@example.com').first())
        self.assertIn(b'Login', response.data)

    def test_signup_duplicate_email(self):
        user = User(email='existinguser@example.com', name='Existing User', password=generate_password_hash('existingpassword'))
        db.session.add(user)
        db.session.commit()

        response = self.client.post(url_for('auth.signup'), data={'email': 'existinguser@example.com', 'name': 'Another User', 'password': 'newpassword'})
        self.assertMessageFlashed('Email address already exists')

if __name__ == '__main__':
    unittest.main()
