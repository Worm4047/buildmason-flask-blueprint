# test_models.py

import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from app.models.user import db, User

app = create_app()

class TestUserModel(unittest.TestCase):

    def setUp(self):
        # Configure the Flask app for testing
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

        # Create the database tables
        db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_user(self):
        with app.app_context():
            user = User(email='test@example.com', password='password123', name='John Doe')
            db.session.add(user)
            db.session.commit()

            queried_user = User.query.filter_by(email='test@example.com').first()

            self.assertIsNotNone(queried_user)
            self.assertEqual(queried_user.email, 'test@example.com')
            self.assertEqual(queried_user.password, 'password123')
            self.assertEqual(queried_user.name, 'John Doe')

    def test_duplicate_email(self):
        with app.app_context():
            user1 = User(email='test@example.com', password='password123', name='John Doe')
            user2 = User(email='test@example.com', password='anotherpassword', name='Jane Doe')

            db.session.add(user1)
            db.session.commit()

            # Attempt to add user2 with the same email should raise an IntegrityError
            with self.assertRaises(Exception):
                db.session.add(user2)
                db.session.commit()

if __name__ == '__main__':
    unittest.main()
