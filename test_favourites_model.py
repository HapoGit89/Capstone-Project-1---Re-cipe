"""Favourites model tests."""

import os
from unittest import TestCase

from models import RecipeIngredients, db, Users, Favourites, Recipes, Ingredients, Ratings
from wrapper import recipe_detail_search

os.environ['DATABASE_URL'] = "postgresql:///recipe_test"


from app import app

db.create_all()

class FavouritessModelTestCase(TestCase):
    """Test Favourites Model"""

    def setUp(self):
        

        Users.query.delete()
        Recipes.query.delete()
        Ingredients.query.delete()
        RecipeIngredients.query.delete()
        Favourites.query.delete()

        new_recipe = Recipes(title = "TestRecipe", spoonacular_id = 1234)
        db.session.add(new_recipe)
        db.session.commit()

        new_user = Users(username = "Test", email = "Testmail@mail.de", password = "test")
        db.session.add(new_user)
        db.session.commit()
        



        self.client = app.test_client()
    
    def test_favourites_model(self):
        recipe = Recipes.query.first()
        user = Users.query.first()
        new_favourite = Favourites(user_id = user.id, recipe_id = recipe.id )
        db.session.add(new_favourite)
        db.session.commit()

        self.assertEqual(f"Favourite id:{new_favourite.id} for user {user.id} and recipe {recipe.id}", new_favourite.__repr__()) # check if __repr__ function works
        self.assertIn(recipe, user.favourite_recipes) # test if m2m relationship works
        self.assertIn(user, recipe.users) # ""

