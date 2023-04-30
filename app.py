
import os
from re import I
from telnetlib import SE
from this import d

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

# from forms import UserAddForm, LoginForm, MessageForm, UserEditForm
from models import db, connect_db, Users, Recipes, Ingredients, RecipeIngredients, Favourites
from wrapper import complex_recipe_search, recipe_detail_search
from forms import SearchForm
CURR_USER_KEY = "curr_user"

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///recipe'))
app.config['DEVELOPMENT'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "SHHHHH Secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)


with app.app_context():
    db.create_all()

@app.route("/")
def show_start():
    return redirect("/search")

@app.route("/search", methods = ["GET", "POST"])
def show_search_page():

    form = SearchForm()

    if form.validate_on_submit():
        query = form.query.data
        veggie = form.veggie.data
        vegan = form.vegan.data
        gluten_free = form.gluten_free.data
        dairy_free = form.dairy_free.data
        diets = form.diet.data
        cuisine = form.cuisine.data
        intolerance = form.intolerance.data
        exclude = form.exclude.data

        results = complex_recipe_search(query, veggie, vegan, gluten_free, dairy_free, diets, cuisine, intolerance, exclude)
        no_of_results = len(results['results'])
      
        return render_template("results.html", results=results, form = form, no_of_results=no_of_results)

    else:
        
        return render_template("search.html", form = form)
    
@app.route("/recipes/<spoonacular_id>")
def show_recipe_details(spoonacular_id):
    """ check if Recipe in DB and get data or get data from API and commit data to db"""
   
    if Recipes.query.filter_by(spoonacular_id = spoonacular_id).all():
        recipe = Recipes.query.filter_by(spoonacular_id = spoonacular_id).one()
        print("Recipe is in DB")
        print(recipe)
        return render_template("recipe_details.html", recipe=recipe)
    else:
        recipe = recipe_detail_search(spoonacular_id)
        print("Recipe not in db")
        new_recipe = Recipes(title = recipe['title'],
                            spoonacular_id = recipe['spoonacular_id'],
                            diets = recipe['diets'],
                            ready_in = recipe['readyIn'],
                            image_url = recipe['image_url'],
                            cuisine = recipe['cuisines'],
                            health_score = recipe['health_score'],
                            steps = recipe['steps'],
                            dairy_free = recipe['dairyFree'],
                            gluten_free = recipe['glutenFree'],
                            vegan = recipe['vegan'],
                            vegetarian = recipe ['vegetarian'],
                            servings = recipe['servings'],
                            summary = recipe['summary'])
    
        db.session.add(new_recipe)
        db.session.commit()
        print("after recipe COMMMIT !!!!!!")
        recipe = Recipes.query.filter_by(spoonacular_id=spoonacular_id).one()
        return render_template("recipe_details.html", recipe=recipe)




