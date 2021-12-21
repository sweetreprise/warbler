"""User View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_user_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User, Likes, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

# db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False

class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(
            username="testuser",
            email="test@test.com",
            password="testuser",
            image_url=None
        )
        
        self.u1 = User.signup(
            username="testuser1",
            email="test1@test.com",
            password="testuser1",
            image_url=None
        )
        
        self.u2 = User.signup(
            username="testuser2",
            email="test2@test.com",
            password="testuser2",
            image_url=None
        )
        
        self.u3 = User.signup(
            username="testuser3",
            email="test3@test.com",
            password="testuser3",
            image_url=None
        )

        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_users_list(self):
        """Are users being displayed correctly on /users?"""
        with self.client as c:
            resp = c.get("/users")

            self.assertEqual(resp.status_code, 200)
            self.assertIn("@testuser", str(resp.data))
            self.assertIn("@testuser1", str(resp.data))
            self.assertIn("@testuser2", str(resp.data))
            self.assertIn("@testuser3", str(resp.data))

    def test_users_search(self):
        """Is the search bar returning users?"""
        with self.client as c:
            resp = c.get("/users?q=testuser1")

            self.assertEqual(resp.status_code, 200)
            self.assertIn("@testuser1", str(resp.data))
            self.assertNotIn("@testuser2", str(resp.data))

    def test_show_user(self):
        """Does page show details for a specific user"""
        with self.client as c:
            resp = c.get(f"/users/{self.testuser.id}")

            self.assertEqual(resp.status_code, 200)
            self.assertIn("@testuser", str(resp.data))

