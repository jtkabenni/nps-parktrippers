import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Visit, Park, Activity

os.environ['DATABASE_URL'] = "postgresql:///parktrippers-test"
from app import app, CURR_USER_KEY

db.create_all()

class VisitModelTestCase(TestCase):
    """Test views for user routes."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Visit.query.delete()
        Park.query.delete()
        u1 = User.register("treeluvr", "treeluvr123", "tree@lover.com", "Jay", "Blanchett")
        u2 = User.register("naturebestfriend", "naturelover123", "nature@lover.com", "Sam", "Blanchett")
        p1 =Park(park_code = "acad", park_name = "Acadia National Park")
        p2 =Park(park_code = "bibe", park_name = "Big Bend National Park")
        db.session.add_all([u1, u2, p1, p2])
        db.session.commit()
        v1 = Visit(start_date = "2023-7-1", end_date="2023-7-13", park_code = "acad", username = u1.username)
        v2 = Visit(start_date = "2023-7-3", end_date="2023-7-10", park_code = "bibe", username = u1.username)
        db.session.add_all([v1, v2])
        db.session.commit()
        a1 = Activity(name = "Hiking on X trail", description = "Description for this hike.", activity_type= "hike", location = "Hike 1 location", visit_id =v1.id )
        a2 = Activity(name = "Hiking on XYX trail", description = "Description for second hike.", activity_type= "hike", location = "Hike 2 location", visit_id =v1.id )

        db.session.add_all([a1, a2])
        db.session.commit()

        self.u1=u1
        self.u2=u2
        self.v1=v1
        self.v2=v2
        self.a1=a1
        self.a2=a2
        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_index_unauthenticated(self):
        """View sign up and login when unauthenticated"""
        response = self.client.get('/') 
        self.assertIn(b"Sign up",response.data )
        self.assertIn(b"Login",response.data )
        self.assertNotIn(b"Log out",response.data )
    
    def test_view_visits(self):
        """View profile"""
        with self.client as c:
          with c.session_transaction() as sess:
            sess[CURR_USER_KEY] = self.u1.username
          response = self.client.get(f'/{self.u1.username}',follow_redirects=True)
          self.assertIn(b"Acadia National Park", response.data)
          self.assertIn(b"Big Bend National Park", response.data)
          self.assertIn(b"Saturday July 01, 2023 to Thursday July 13, 2023", response.data)

    def test_view_visits_detail(self):
        """View visit detail page"""
        with self.client as c:
          with c.session_transaction() as sess:
            sess[CURR_USER_KEY] = self.u1.username
          response = self.client.get(f'/{self.u1.username}/visits/{self.v1.id}',follow_redirects=True)
          self.assertIn(b"Add activity notes here", response.data)
          self.assertIn(b"Hiking on X trail", response.data)
          self.assertIn(b"Add new activity", response.data)

    
