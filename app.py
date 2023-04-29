
import os
from telnetlib import SE

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
    return render_template("search.html", form = form)


