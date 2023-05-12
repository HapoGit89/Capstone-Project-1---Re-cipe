"""View Function integration tests"""

import os
from unittest import TestCase

from models import RecipeIngredients, db, Users, Favourites, Recipes, Ingredients, Ratings
from wrapper import recipe_detail_search

os.environ['DATABASE_URL'] = "postgresql:///recipe_test"


from app import app, CURR_USER_KEY

db.create_all()


app.config['WTF_CSRF_ENABLED'] = False

class ViewFuncTestCase(TestCase):
    """Test View Functions"""

    def setUp(self):
        

        Users.query.delete()
        Recipes.query.delete()
        Ingredients.query.delete()
        RecipeIngredients.query.delete()
        Favourites.query.delete()

        self.client = app.test_client()

        self.testuser = Users.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    )
        
        db.session.commit()
        new_recipe = Recipes(title="testrecipe", spoonacular_id = 1234)
        db.session.add(new_recipe)
        new_recipe2 = Recipes(title="testrecipe2", spoonacular_id = 1235)
        db.session.add(new_recipe2)
        db.session.commit()
        new_favourites=Favourites(recipe_id=new_recipe.id, user_id = self.testuser.id)
        db.session.add(new_favourites)
        db.session.commit()
        
       

        

    
    def test_sign_up(self):
        """can we sign up a user?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            resp = c.post("users/signup", data={"username": "Testuser34", "password": "passIT", "password_conf": "passIT", "email": "testuser2@test.de"})


                 # Test response status code
            self.assertEqual(resp.status_code, 302)
                
            #Test if right URL in redirect
            self.assertIn('href="/"', str(resp.data))


       
    def test_show_search_page(self):
        """does it render the search page as well as the results?"""
        
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            resp = c.get("/search")

            # test if search page gets rendered and right status code returned
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Search Re:Cipe", str(resp.data))

            resp2 = c.post("/search", data={"query": "Noodles", "veggie": True, "vegan": True, "gluten_free": False, "dairy_free": False, "diets": "vegetarian", "cuisine": "European", "intolerance": "Egg", "exclude": "Tomato" })  #this search query should at least return 1 recipe

            self.assertEqual(resp2.status_code, 200)
            # self.assertIn("Results shown", str(resp2.data))
            # self.assertIn(' <div class="card col-md4" style="width: 18rem; margin: 1rem;">', str(resp2.data))

    def test_show_recipe_details(self):
         """is recipe detail page rendered? """
         with self.client as c:
             resp=c.get("/recipes/638382")
             self.assertEqual(resp.status_code, 200)
             self.assertIn('<h1 class="display-4">Chicken Teriyaki with Soba Noodles</h1>', str(resp.data))

    def test_show_start(self):
        """does "/" redirect to search page?"""
        with self.client as c:

            resp = c.get("/")
            self.assertEqual(302, resp.status_code)
            self.assertIn('href="/search"', str(resp.data))


    def test_log_in_user(self):
        """does login route work?"""
        with self.client as c:
            with c.session_transaction() as session:
                     if CURR_USER_KEY in session:
                        del session[CURR_USER_KEY]
            
            resp = c.post("users/login", data={"username": "testuser", "password": "testuser"})

            self.assertEqual(302, resp.status_code)
            with c.session_transaction() as session:
                user = Users.query.first()
                self.assertEqual(user.id, session[CURR_USER_KEY])
                del session[CURR_USER_KEY]

            resp2 = c.post("users/login", data={"username": "testuser", "password": "testus23er"})
            self.assertEqual(200, resp2.status_code)
            self.assertIn("Wrong username", str(resp2.data))
    
    def test_log_out_user(self):
        """does logout route work?"""

        with self.client as c:
            with c.session_transaction() as session:
                user = Users.query.first()
                session[CURR_USER_KEY]=user.id
            resp = c.get("/users/logout")
            self.assertEqual(302, resp.status_code)
            self.assertIn('href="/users/login"', str(resp.data))

    def test_show_favourites(self):
        """does show_favourites route work?"""
        with self.client as c:

            # test if I get favourites when logged in
            with c.session_transaction() as session:
                session[CURR_USER_KEY]=self.testuser.id 
            resp= c.get("/recipes/favourites")  
            self.assertEqual(resp.status_code, 200)
            self.assertIn("testrecipe", str(resp.data))

            # test if I get redirected when not logged in

            with c.session_transaction() as session:
                del session[CURR_USER_KEY]
            resp= c.get("/recipes/favourites")
            self.assertEqual(resp.status_code, 302)
            self.assertIn('href="/"', str(resp.data))
    
    def test_add_favourites(self):
            """check if route for adding favourites works"""
            with self.client as c:
                # test if I can add favs when logged in
                with c.session_transaction() as session:
                    session[CURR_USER_KEY]=self.testuser.id 
                resp= c.post("/recipes/favourites/1235/add")  
                self.assertEqual(resp.status_code, 200)
                self.assertIn("added to favourites", str(resp.data))

                # check if action gets denied when not logged in
                with c.session_transaction() as session:
                    del session[CURR_USER_KEY]
                resp= c.post("/recipes/favourites/1235/add")  
                self.assertEqual(resp.status_code, 302)
                self.assertIn('href="/"', str(resp.data))




            
