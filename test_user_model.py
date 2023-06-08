"""User model tests."""

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Visit, Park, Activity

os.environ['DATABASE_URL'] = "postgresql:///parktrippers-test"

from app import app

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Visit.query.delete()
        Park.query.delete()
        u1 = User.register("treeluvr", "treeluvr123", "tree@lover.com", "Jay", "Blanchett")
        u2 = User.register("naturebestfriend", "naturelover123", "nature@lover.com", "Sam", "Blanchett")
        db.session.add_all([u1, u2])
        db.session.commit()
        self.u1=u1
        self.u2=u2
        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()


    def test_user_model(self):
        """Does basic model work?"""
        u = User.register("mountainluvr", "mountainluvr123", "mountain@lover.com", "John", "Blanchett")
        db.session.add(u)
        db.session.commit()
        # User should have no visits or activities 
        self.assertEqual(len(u.visits), 0)
        self.assertEqual(len(u.activities), 0)

    def test_successful_register(self):
        """Verify User.register successfully create a new user given valid credentials"""
        u3 = User.register("mountainluvr", "mountainluvr123", "mountain@lover.com", "John", "Blanchett")
        db.session.add(u3)
        db.session.commit()
        print(f"<<<<<<<<<<<<<<<<<{User.query.all()}")
        self.assertEqual(len(User.query.all()), 3)
        self.assertEqual(u3.username, "mountainluvr")

    def test_invalid_register_duplicate_username(self):
        """Verify User.register fails to create a new user if username is a duplicate"""
        u3 = User.register("treeluvr", "treeluvr123", "tree@lover.com", "Jay", "Blanchett")
        db.session.add(u3)
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_register_missing_username(self):
        """Verify User.register fails to create a new user if username is missing"""
        u3 = User.register(None, "treeluvr123", "tree@lover.com", "Jay", "Blanchett")
        db.session.add(u3)
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_authenticate_user(self):
        """Verify User.authenticate successfully return a user when given a valid username and password"""
        u3 = User.authenticate("treeluvr", "treeluvr123")
        self.assertEqual(u3, self.u1)

    def test_invalid_username_authenticate_user(self):
        """Verify User.authenticate fail to return a user when the username is invalid"""
        u3 = User.authenticate("treelover", "treeluvr123")
        self.assertEqual(u3, False)

    def test_invalid_password_authenticate_user(self):
        """Verify User.authenticate fails to return a user when the password is invalid"""
        u3 = User.authenticate("treeluvr", "passworddd")
        self.assertEqual(u3, False)

