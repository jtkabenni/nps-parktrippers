import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Visit, Park, Activity

os.environ['DATABASE_URL'] = "postgresql:///parktrippers-test"
from app import app, CURR_USER_KEY

db.create_all()

class UserModelTestCase(TestCase):
    """Test views for user routes."""

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


    def test_index_unauthenticated(self):
        """View sign up and login when unauthenticated"""
        response = self.client.get('/') 
        self.assertIn(b"Sign up",response.data )
        self.assertIn(b"Login",response.data )
        self.assertNotIn(b"Log out",response.data )
    
    def test_users_unauthenticated(self):
        """View other user profile as unauthenticated user"""
        with self.client as c:
          with c.session_transaction() as sess:
            sess[CURR_USER_KEY] = self.u1.username
          response = self.client.get('/naturebestfriend',follow_redirects=True)
          self.assertIn(b"Welcome back", response.data)
    
