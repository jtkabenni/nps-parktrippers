import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Visit, Park, Activity

os.environ['DATABASE_URL'] = "postgresql:///parktrippers-test"

from app import app

db.create_all()

class VisitModelTestCase(TestCase):
    """Test views for messages."""

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

        self.u1=u1
        self.u2=u2
        self.v1=v1
        self.v2=v2
        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_visit_model(self):
        """Does basic model work?"""
        self.assertEqual(len(Visit.query.all()), 2)

    def test_user_visits(self):
        """Verify added visits are associated with user"""
        user = User.query.get_or_404(self.u1.username)
        self.assertEqual(len(user.visits), 2)

    def test_visit_add_activities(self):
        """Verify added activities associated with user"""
        a1 = Activity(name = "Hiking on X trail", description = "Description for this hike.", activity_type= "hike", location = "Hike 1 location", visit_id =self.v1.id )
        a2 = Activity(name = "Hiking on XYX trail", description = "Description for second hike.", activity_type= "hike", location = "Hike 2 location", visit_id =self.v1.id )
        db.session.add_all([a1, a2])
        db.session.commit()
        user = User.query.get_or_404(self.u1.username)
        self.assertEqual(len(user.activities),2)



  