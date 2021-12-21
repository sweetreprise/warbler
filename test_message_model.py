"""Message model tests."""

# python -m unittest test_message_model.py

import os
from unittest import TestCase

from models import db, User, Message

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

class MessagesModelTestCase(TestCase):
    """Test views for Message model"""

    def setUp(self):

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        u = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url="/static/images/default-pic.png"
        )

        db.session.add(u)
        db.session.commit()

        user = User.query.get_or_404(u.id)

        self.user = user

    def tearDown(self):
        db.session.rollback()

    def test_message_model(self):
        """Does basic model work?"""

        msg = Message(
            text="Test message",
            user_id=self.user.id
        )

        db.session.add(msg)
        db.session.commit()

        self.assertEqual(len(self.user.messages), 1)
        self.assertEqual(self.user.messages[0].text, "Test message")

    def test_message_likes(self):
        """Tests if a liked message shows up in user likes"""

        u = User.signup(
            email="test@mail.com",
            username="testtest",
            password="PASSWORD",
            image_url="/static/images/default-pic.png"
        )

        db.session.add(u)
        db.session.commit()

        m = Message(
            text="Test messageeeee",
            user_id=u.id
        )

        db.session.add(m)
        db.session.commit()

        self.user.likes.append(m)
        db.session.commit()

        self.assertEqual(len(self.user.likes), 1)
        self.assertEqual(self.user.likes[0].text, 'Test messageeeee')


        






