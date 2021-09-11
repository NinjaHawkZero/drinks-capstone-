from unittest import TestCase
import os

from app import app, get_drink_id, get_drink_name
from flask import session
from models import User, FavDrink, db

os.environ['DATABASE_URL'] = "postgresql:///test_drinks"


db.create_all()

 # To run tests: FLASK_ENV=production python -m unittest test_views.py
 # python -m unittest test_user.py


class UserModelTestCase(TestCase):

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        u1 = User.register("testuser1", "bojangles", "bojangles@email.com")
        


        u2 = User.register("testuser2", "superbojan", "superbojan@email.com")

        db.session.commit()

        u1 = User.query.get(u1.username)
        u2 = User.query.get(u2.username)

        self.u1 = u1
        self.u2 = u2
       


        self.client = app.test_client()
    

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    

    def test_user_model(self):
        """Testing user model."""

        u = User(username="testuser3",
                email= "testuser@email.com",
                password= "testusbo")
        
        db.session.add(u)
        db.session.commit()

        # User should have no favDrinks
        self.assertEqual(len(u.favorite_drinks), 0)

    
    def test_favDrink_model(self):
        """Testing drink model."""

        
        
        
        fav_drink = FavDrink(name="vodka", username="testuser1", drink_id=1107)

        db.session.add(fav_drink)
        db.session.commit()

        self.assertEqual(fav_drink.drink_id, 1107)
        self.assertEqual(fav_drink.id, 1)

    # SignUp Test
    def test_valid_signup(self):
        """Test user signup."""
        u_test = User.register("testtest", "meeechibo", "testmeechi@email.com")
        
        
        db.session.commit()

        u_test = User.query.get(u_test.username)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username, "testtest")
        self.assertNotEqual(u_test.password, "meeechibo")
        self.assertEqual(u_test.email, "testmeechi@email.com")
        # bcrypt strings should start with $2b$
        self.assertTrue(u_test.password.startswith("$2b$"))


    def test_drink_name(self):
        """Test drink name function."""

        drink_obj = get_drink_name("margarita")

        self.assertTrue(drink_obj[0]["idDrink"].startswith("11007"))


    def test_drink_id(self):
        """Test drink id function."""

        drink_obj = get_drink_id(11007)

        self.assertTrue(drink_obj[0]["strDrink"].startswith("Margarita"))

        