"""Ingredients model tests."""

import os
from unittest import TestCase

from models import RecipeIngredients, db, Users, Favourites, Recipes, Ingredients, Ratings
from wrapper import recipe_detail_search

os.environ['DATABASE_URL'] = "postgresql:///recipe_test"


from app import app

db.create_all()

class IngredientsModelTestCase(TestCase):
    """Test Ingredients Model"""

    def setUp(self):
        

        Users.query.delete()
        Recipes.query.delete()
        Ingredients.query.delete()
        RecipeIngredients.query.delete()
        Favourites.query.delete()
        Ratings.query.delete

        new_recipe = Recipes(title = "TestRecipe", spoonacular_id = 12343)
        db.session.add(new_recipe)
        db.session.commit()

        new_user = Users(username = "Test", email = "Testmail@mail.de", password = "test")
        db.session.add(new_user)
        db.session.commit()
        



        self.client = app.test_client()

    def test_ingredients_model_instances(self):

        new_ingredient = Ingredients(name ="TestIngredient", spoonacular_id = 12344)
        db.session.add(new_ingredient)
        db.session.commit()

        self.assertIn("TestIngredient", new_ingredient.__repr__()) # Test if instance gets created sucessfully and __rep__ works

        recipe = Recipes.query.first()
        new_recipe_ingredients= RecipeIngredients(recipe_id = recipe.id, ingredient_id = new_ingredient.id, amount = "1 Teaspoon")
        db.session.add(new_recipe_ingredients)
        db.session.commit()

        self.assertIn(recipe, new_ingredient.in_recipes) # test if in_recipes relationship works


    def test_ingredients_methods(self):
        new_ingredient = Ingredients(name ="TestIngredient", spoonacular_id = 1234)
        db.session.add(new_ingredient)
        db.session.commit()

        # check if classmethod is_ingredient_in_db is working

        self.assertEqual(True, Ingredients.is_ingredient_in_db(1234)) 
        self.assertEqual(False, Ingredients.is_ingredient_in_db(12345454))