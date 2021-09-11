"""View tests"""

import os
from unittest import TestCase

from app import app
from flask import session
from models import db, connect_db, User, FavDrink


os.environ['DATABASE_URL'] = "postgresql:///test_drinks"



db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class ViewTestCase(TestCase):
    """Test views"""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()
        self.client = app.test_client()

        self.testuser = User.register(username="testuser1", password="bojangles", email="bojangles@email.com")
        


        u2 = User.register("testuser2", "superbojan", "superbojan@email.com")

        

        
        u2 = User.query.get(u2.username)

        self.u2 = u2

        db.session.commit()
       


        
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    
    def test_register_view(self):
        """Test Registration view"""

        with self.client as c:

            resp = c.get('/register')
            self.assertIn("<h1>Signup</h1>", str(resp.data))



    def test_login_view(self):
        """Test login view"""

        with self.client as c:

            resp = c.get('/login')
            self.assertIn("<h1>Login a user</h1>", str(resp.data))


    def test_login_redirect_view(self):
        """Test login view redirect."""
        with self.client as c:
            with c.session_transaction() as sess:
                sess['username'] = self.testuser.username
            
            resp = c.get('/login')
            self.assertIn("testuser1", str(resp.data))
       
    def test_user_show(self):
        """Test user route and if user data is in response."""
        with self.client as c:
            with c.session_transaction() as sess:
                sess['username'] = self.testuser.username
                
            resp = c.get(f"/users/{self.testuser.username}")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("testuser1", str(resp.data))

    
    def test_logout(self):
        """Test Logout route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['username'] = self.testuser.username
            
            resp = c.get("/logout")
            self.assertEqual(resp.status_code, 302)
            self.assertIn("<title>Redirecting...</title>", str(resp.data))
    
    
                

                