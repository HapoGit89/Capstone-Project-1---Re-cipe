"""User model tests."""

import os
from unittest import TestCase

from models import db, Users, Favourites, Recipes

os.environ['DATABASE_URL'] = "postgresql:///recipe_test"


from app import app

db.create_all()

class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        Users.query.delete()
        Recipes.query.delete()
        Favourites.query.delete()



        self.client = app.test_client()

    def test_user_model_instances(self):

        # create Users instance for testing
        user = Users(username = "Testuser", email= "test@test.de", password = "test")
        db.session.add(user)
        db.session.commit()

        self.assertIn("Testuser", user.__repr__())   #check if __repr__ function works
        self.assertIn("test@test.de", user.__repr__())   #check if __repr__ function works
    
    def test_user_model_methods(self):

        # check if signIn Method works
        user2 = Users.signup(username = "Test2", email = "test2@test2.de", password = "test2")
        db.session.commit()
        
        self.assertIn(user2, Users.query.all())

        # check if user_edit method works
        user2.edit_user(email = "test2user@test.de", password = '')
        self.assertIn("test2user@test.de", user2.__repr__())   

        # check authenticate function
        self.assertEqual(user2, Users.authenticate(username = user2.username, password = "test2"))

        # check render_favourites func

        recipe1 = Recipes(title = "testRecipe", spoonacular_id = 12334)
        recipe2 = Recipes(title = "testRecipe2", spoonacular_id = 122334)
        db.session.add(recipe1)
        db.session.add(recipe2)
        db.session.commit()
        favourite1 = Favourites(user_id = user2.id, recipe_id=recipe1.id)
        favourite2 = Favourites(user_id = user2.id, recipe_id=recipe2.id)
        db.session.add(favourite1)
        db.session.add(favourite2)
        db.session.commit()

        self.assertEqual([12334, 122334], user2.render_favourites_spoonacular_ids())







