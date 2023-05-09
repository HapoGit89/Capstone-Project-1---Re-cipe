"""Recipe model tests."""

import os
from unittest import TestCase

from models import RecipeIngredients, db, Users, Favourites, Recipes, Ingredients, Ratings
from wrapper import recipe_detail_search

os.environ['DATABASE_URL'] = "postgresql:///recipe_test"


from app import app

db.create_all()

class RecipeModelTestCase(TestCase):
    """Test Recipe Model"""

    def setUp(self):
        

        Users.query.delete()
        Recipes.query.delete()
        Ingredients.query.delete()
        RecipeIngredients.query.delete()
        Favourites.query.delete()

        new_ingredient = Ingredients(name = "TestIngredient", spoonacular_id = 1234)
        db.session.add(new_ingredient)
        db.session.commit()

        new_user = Users(username = "Test", email = "Testmail@mail.de", password = "test")
        db.session.add(new_user)
        db.session.commit()
        



        self.client = app.test_client()
    
    def test_recipe_model_instances(self):

        # create Recipe instance for testing
        recipe = Recipes(title = "testrecipe",
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
        
        db.session.add(recipe)
        db.session.commit()

        self.assertIn("testrecipe", recipe.__repr__())   #check if __repr__ function works
        self.assertIn("124435", recipe.__repr__())   #check if __repr__ function works
        self.assertEqual("These are the steps", Recipes.query.filter_by(spoonacular_id = 124435).one().steps)

    def test_recipe_model_methods(self):
        recipe = {'title': "testrecipe2", 
                  'spoonacular_id': 123455,
                    'diets': ['vegan'],
                      'readyIn': 45,
                        'image_url': "www.test.de",
                          'cuisines': ['French'],
                            'health_score': 2,
                              'ingredients': ['ingredients'],
                                'steps': 'These are steps',
                                  'summary': ['This is a summary'],
                                    'vegan': True,
                                    'vegetarian': True,
                                      'servings': 2,
                                        'glutenFree': False,
                                          'dairyFree': False}
        new_recipe = Recipes.add_new_recipe(recipe)
        self.assertEqual("testrecipe2", Recipes.query.filter_by(spoonacular_id = 123455).one().title) # test add_new_recipe method
        self.assertEqual("These are steps", Recipes.query.filter_by(spoonacular_id = 123455).one().steps)

        self.assertEqual(Recipes.is_recipe_in_db(123455), True) # test is_recipe_in_db method
        
        new_recipe_ingredient = RecipeIngredients(recipe_id = new_recipe.id, ingredient_id = Ingredients.query.first().id, amount = "1 Teaspoon")
        db.session.add(new_recipe_ingredient)    
        db.session.commit()

        self.assertIn("1 Teaspoon", new_recipe.render_ingredients()[0].get('amount')) # check if method return value includes amoutn given as argument

        self.assertEqual("N/A", new_recipe.get_avg_rating())  # check if rating for not rated recipe is "N/A"
        new_rating = Ratings(user_id=Users.query.first().id, recipe_id = new_recipe.id, rating = 4)
        db.session.add(new_rating)
        db.session.commit()
        self.assertEqual("4.0/5", new_recipe.get_avg_rating())  # check if rating changes when recipe gets rated
        









