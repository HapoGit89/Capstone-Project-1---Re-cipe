"""RecipeIngredients model tests."""

import os
from unittest import TestCase

from models import RecipeIngredients, db, Users, Favourites, Recipes, Ingredients, Ratings
from wrapper import recipe_detail_search

os.environ['DATABASE_URL'] = "postgresql:///recipe_test"


from app import app

db.create_all()

class RecipeModelTestCase(TestCase):
    """Test RecipeIngredient Model"""

    def setUp(self):
        

        Users.query.delete()
        Recipes.query.delete()
        Ingredients.query.delete()
        RecipeIngredients.query.delete()
        Favourites.query.delete()

        new_ingredient = Ingredients(name = "TestIngredient", spoonacular_id = 1234, image = "www.image.com")
        new_ingredient2 = Ingredients(name = "TestIngredient2", spoonacular_id = 1235, image = "www.image2.com")
        db.session.add(new_ingredient)
        db.session.add(new_ingredient2)
        db.session.commit()

        new_recipe = Recipes(title = "testrecipe",
                          spoonacular_id = 124435,
                            diets = ["vegetarian", "ketogenic"],
                              ready_in = 45,
                                image_url="https://img-getpocket.cdn.mozilla.net/296x148/filters:format(jpeg):quality(60):no_upscale():strip_exif()/https%3A%2F%2Fs.zkcdn.net%2FAdvertisers%2F3541e370f92d4729876a5798816e24e5.png",
                                 cuisine=["African", "European"],
                                  health_score = 10,
                                   steps = "These are the steps",
                                    dairy_free = True,
                                     gluten_free= False,
                                      vegan = True,
                                       vegetarian = True,
                                        servings = 2,
                                         summary = "This is a test summary" )
        db.session.add(new_recipe)
        db.session.commit()



        self.client = app.test_client()


    def test_recipeIngredients_model(self):
            """check if recipeIngredients models works """

            ingredient1 = Ingredients.query.filter_by(spoonacular_id=1234).one()
            ingredient2 = Ingredients.query.filter_by(spoonacular_id=1235).one()
            recipe = Recipes.query.first()
            new_recipeingredient = RecipeIngredients(recipe_id = recipe.id, ingredient_id = ingredient1.id, amount = "1Teaspoon")
            db.session.add(new_recipeingredient)
            db.session.commit()
            new_recipeingredient2 = RecipeIngredients(recipe_id = recipe.id, ingredient_id = ingredient2.id, amount = "2Teaspoon")
            db.session.add(new_recipeingredient2)
            db.session.commit()

            self.assertEqual(f"Ingredient {ingredient1.id} is in recipe {recipe.id} with amount 1Teaspoon", new_recipeingredient.__repr__()) # check if __repr__ works
            self.assertEqual(f"Ingredient {ingredient2.id} is in recipe {recipe.id} with amount 2Teaspoon", new_recipeingredient2.__repr__()) # check if __repr__ works 
            self.assertIn(ingredient1, recipe.ingredients) #check if m2m relation works

    def test_recipeIngredients_methods(self):
         
            ingredient1 = Ingredients.query.filter_by(spoonacular_id=1234).one()
            ingredient2 = Ingredients.query.filter_by(spoonacular_id=1235).one()
            recipe = Recipes.query.first()
            new_recipeingredient = RecipeIngredients(recipe_id = recipe.id, ingredient_id = ingredient1.id, amount = "1Teaspoon")
            db.session.add(new_recipeingredient)
            db.session.commit()

            self.assertEqual(True, RecipeIngredients.is_recipe_ingredient_in_db(recipe = recipe, ingredient = ingredient1)) # test if is_recipeingredient_in_db method works
            self.assertEqual(False, RecipeIngredients.is_recipe_ingredient_in_db(recipe = recipe, ingredient = ingredient2))
            
            new_recipe_ingredient2 = RecipeIngredients.add_new_recipe_ingredient(recipe=recipe, ingredient=ingredient2, amount="2Teaspoon")
            self.assertIsInstance(new_recipe_ingredient2, RecipeIngredients) # check if add_new_recipe_ingredient method return right Instance
            self.assertIn("2Teaspoon", new_recipe_ingredient2.__repr__()) # test behaviour of instance created by add_new methd

