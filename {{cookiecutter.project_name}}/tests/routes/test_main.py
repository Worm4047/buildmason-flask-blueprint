import unittest
from flask import Flask, url_for
from flask_testing import TestCase
from flask_login import LoginManager, current_user, login_user
from app import create_app
from app.models.user import User, db


class TestMainRoutes(TestCase):

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

        # Create a test user and log them in
        user = User(email='test@example.com', name='Test User', password='password123')
        db.session.add(user)
        db.session.commit()

        # Log the user in
        with self.client:
            login_user(user)
            response = self.client.get(url_for('main.profile'))
            self.assert200(response)
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index_page_loads(self):
        response = self.client.get(url_for('main.index'))
        self.assert200(response)
        self.assertTemplateUsed('index.html')

    def test_profile_page_loads(self):
        response = self.client.get(url_for('main.profile'))
        self.assert200(response)
        self.assertTemplateUsed('profile.html')
        self.assertIn(b'Test User', response.data)  # Check if user's name is displayed

    def test_profile_requires_login(self):
        # Log the user out before accessing the profile page
        self.client.get(url_for('auth.logout'))
        response = self.client.get(url_for('main.profile'), follow_redirects=True)
        self.assert200(response)

if __name__ == '__main__':
    unittest.main()
