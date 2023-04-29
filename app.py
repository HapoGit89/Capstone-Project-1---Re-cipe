
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
        message = ''
        if results['totalResults']==0:
            message = "Sorry no results for that Search!"
        return render_template("results.html", results=results, form = form, message = message)

    else:
        
        return render_template("search.html", form = form)


