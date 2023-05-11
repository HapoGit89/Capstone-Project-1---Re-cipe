"""Ratings model tests."""

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
    
    def test_ratings_model(self):
        recipe = Recipes.query.first()
        user = Users.query.first()
        new_rating = Ratings(user_id=user.id, recipe_id = recipe.id, rating = 3)
        db.session.add(new_rating)
        db.session.commit()

        self.assertEqual(f"Rating id:{new_rating.id} for user {user.id} and recipe {recipe.id} is {new_rating.rating}",
                         new_rating.__repr__()) #test if __repr__ works

    def test_ratings_methods(self):
        recipe = Recipes.query.first()
        user = Users.query.first()
        new_rating = Ratings(user_id=user.id, recipe_id = recipe.id, rating = 3)
        db.session.add(new_rating)
        db.session.commit()

        self.assertEqual(new_rating.serialize_rating(),       #test if serialize func works
                         {'id': new_rating.id,
                       'rating': new_rating.rating,
                       'user_id': new_rating.user_id,
                       'recipe_id': new_rating.recipe_id
                       })      
        
        

