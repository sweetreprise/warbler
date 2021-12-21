"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data


class UserModelTestCase(TestCase):
    """Test views for User model"""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        user1 = User.signup(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD",
            image_url="/static/images/default-pic.png"
        )

        user2 = User.signup(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD",
            image_url="/static/images/default-pic.png"
        )

        db.session.add(user1, user2)
        db.session.commit()

        u1 = User.query.get(user1.id)
        u2 = User.query.get(user2.id)

        self.u1 = u1
        self.u2 = u2


    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()


    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)


    def test_repr(self):
        """Does the repr method work as expected?"""

        self.u1.__repr__()

        self.assertEqual(str(self.u1), f"<User #{self.u1.id}: {self.u1.username}, {self.u1.email}>")

    ########### USER FOLLOWER TESTS ###########

    def test_followers(self):
        """Tests if a user 2 is shown on user 1's followers list"""
        # add user 2 to user 1's followers
        self.u1.followers.append(self.u2)
        db.session.commit()

        # user 2 should be following 1 user and have 0 followers
        self.assertEqual(len(self.u2.following), 1)
        self.assertEqual(len(self.u2.followers), 0)

        # user 1 should be following 0 users and have 1 follower
        self.assertEqual(len(self.u1.following), 0)
        self.assertEqual(len(self.u1.followers), 1)

        # ID of user 2 should be equal to the id of user 1's followers at index 0
        self.assertTrue(self.u1.followers[0].id == self.u2.id)
        # ID of user 1 should be equal to the id of user 2's following at index 0
        self.assertTrue(self.u2.following[0].id == self.u1.id)

    def test_is_following(self):
        """Does the is_following method work?"""
        # add user 2 to user 1's followers
        self.u1.followers.append(self.u2)
        db.session.commit()

        self.assertTrue(self.u2.is_following(self.u1))
        self.assertFalse(self.u1.is_following(self.u2))

    def test_is_followed_by(self):
        """Does the is_followed_by method work?"""
        # add user 2 to user 1's followers
        self.u1.followers.append(self.u2)
        db.session.commit()

        self.assertTrue(self.u1.is_followed_by(self.u2))
        self.assertFalse(self.u2.is_followed_by(self.u1))

    ########### USER SIGNUP TESTS ###########

    def test_signup_success(self):
        """Does User.signup successfully create a new user given
        valid credentials?"""
        
        self.assertEqual(self.u1.email, "test1@test.com")
        self.assertEqual(self.u1.username, "testuser1")
        self.assertEqual(self.u1.image_url, "/static/images/default-pic.png")

        # user's bio and location should be None when first signing up
        self.assertIsNone(self.u1.bio)
        self.assertIsNone(self.u1.location)

        # user's password should not be stored as a string but as a hashed password
        self.assertNotEqual(self.u1.password, "HASHED_PASSWORD")
        self.assertIn('$2b$', self.u1.password)

    def test_signup_duplicate(self):
        """Does User.signup fail to create a new user with duplicate credentials?"""
        #create a new user with a username and email identical to our test user 1
        User.signup(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD",
            image_url="/static/images/default-pic.png"
        )

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
    
    def test_invalid_username(self):
        """Does User.signup fail to create new user with username set to None?"""
        User.signup(
            email="test@test.com",
            username=None,
            password="HASHED_PASSWORD",
            image_url="/static/images/default-pic.png"
        )

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
        
    def test_invalid_password(self):
        """Does User.signup fail to create new user with password set to None?"""

        with self.assertRaises(ValueError) as context:
            User.signup(
                email="test@test.com",
                username="TestTest",
                password=None,
                image_url="/static/images/default-pic.png"
            )

    ########### AUTHENTICATION TESTS ###########

    def test_valid_user(self):
        """Does User.authenticate successfully return a user when given a valid username and password?"""

        valid_user = User.authenticate(self.u1.username, "HASHED_PASSWORD")
        self.assertEqual(self.u1, valid_user)

    def test_invalid_username(self):
        """Does User.authenticate fail to return a user when the username is invalid?"""

        invalid_user = User.authenticate("Testtest", "HASHED_PASSWORD")
        self.assertFalse(invalid_user)

    def test_invalid_password(self):
        """Does User.authenticate fail to return a user when the password is invalid?"""

        invalid_user = User.authenticate(self.u1.username, "invalid_password")
        self.assertFalse(invalid_user)

        




        

    




        
