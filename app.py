
import os
from re import I
from telnetlib import SE
from this import d
from urllib.parse import uses_relative

import json
from flask import Flask, render_template, request, flash, redirect, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

# from forms import UserAddForm, LoginForm, MessageForm, UserEditForm
from models import db, connect_db, Users, Recipes, Ingredients, RecipeIngredients, Favourites, Ratings
from symbol import factor
from wrapper import complex_recipe_search, recipe_detail_search
from forms import SearchForm, UserEdit, UserSignUp, UserLogin

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


@app.before_request
def add_user_to_g():
    """Check before every request if user is logged in. If logged in pass current user object to global flask"""

    if CURR_USER_KEY in session:
        g.user = Users.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


#------Log In and Log Out Funcs

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

#------------------------------



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
        if g.user:
            user = g.user
            favourites = user.render_favourites_spoonacular_ids()
            return render_template("results.html", results=results, form = form, no_of_results=no_of_results, favourites = favourites)
      
        return render_template("results.html", results=results, form = form, no_of_results=no_of_results)

    else:
        
        return render_template("search.html", form = form)
    
@app.route("/recipes/<spoonacular_id>")
def show_recipe_details(spoonacular_id):
    """ check if Recipe in DB and get data or get data from API and commit data to db"""
    if g.user:   # can access page if not logged in but then favourites array is empty
        user = g.user
        favourites = user.render_favourites_spoonacular_ids()
    else: favourites = []

    if Recipes.is_recipe_in_db(spoonacular_id):
        recipe = Recipes.query.filter_by(spoonacular_id = spoonacular_id).one()
        ingredients = recipe.render_ingredients()
        rating = recipe.get_avg_rating()
        return render_template("recipe_details.html", recipe=recipe, ingredients = ingredients, favourites = favourites, rating = rating)
    else:
        recipe = recipe_detail_search(spoonacular_id)
        Recipes.add_new_recipe(recipe)
        db.session.commit()
        recipe_to_render = Recipes.query.filter_by(spoonacular_id = spoonacular_id).one()

        #------Check if all the recipes ingredients are in db if not add to Ingredient and RecipeIngredients table

        for ingredient in recipe['ingredients']:
            
            if Ingredients.is_ingredient_in_db(ingredient['spoonacular_ingredient_id']):
                ingr = Ingredients.query.filter(Ingredients.spoonacular_id == ingredient['spoonacular_ingredient_id']).one()
                if not RecipeIngredients.is_recipe_ingredient_in_db(recipe=recipe_to_render, ingredient=ingr):
                    RecipeIngredients.add_new_recipe_ingredient(recipe = recipe_to_render, ingredient=ingr, amount = ingredient['amount'])                                  
                    db.session.commit()

            else:
                new_ingredient = Ingredients(name = ingredient['name'],
                                            image = f"https://spoonacular.com/cdn/ingredients_100x100/{ingredient['image']}",
                                            spoonacular_id = ingredient['spoonacular_ingredient_id'])
                db.session.add(new_ingredient)
                db.session.commit()

                new_ingredient = Ingredients.query.filter_by(spoonacular_id = ingredient['spoonacular_ingredient_id']).one()
                if not RecipeIngredients.is_recipe_ingredient_in_db(recipe=recipe_to_render, ingredient=new_ingredient):
                    RecipeIngredients.add_new_recipe_ingredient(recipe = recipe_to_render, ingredient=new_ingredient, amount = ingredient['amount'])                                  
                    db.session.commit() 

        recipe_to_render = Recipes.query.filter_by(spoonacular_id=spoonacular_id).one()
        ingredients = recipe_to_render.render_ingredients()
        return render_template("recipe_details.html", recipe=recipe_to_render, ingredients=ingredients, favourites=favourites)

@app.route("/users/signup", methods = ["POST", "GET"])
def sign_up_user():
    """Display User SignUp Form, check f username in database and sign up user"""
    form = UserSignUp()

    if form.validate_on_submit():
        try:
            username = form.username.data
            password = form.password.data
            password_conf = form.password_conf.data
            email = form.email.data
            if password != password_conf:
                flash("Password confirmation not matching", 'danger')
                return render_template('user_signup.html', form=form)
            user = Users.signup(username = username, password = password, email = email)
            db.session.commit()
            

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('user_signup.html', form=form)

        do_login(user)
        flash(f"Welcome, {user.username}", "success")

        return redirect("/")
       
        
    return render_template("user_signup.html", form = form)

@app.route("/users/logout")
def log_out_user():
        """log out user"""
        do_logout()
        flash("You are now logged out.", "danger")
        return redirect("/users/login")

@app.route("/users/login", methods = ["POST", "GET"])
def log_in_user():
    """login route whch renders login form and authentificates login data"""
    form = UserLogin()
    if form.validate_on_submit():

            user = Users.authenticate(username = form.username.data, password = form.password.data)
            if user:
                do_login(user = user)
                flash(f"Welcome back, {user.username}", 'success')
                return redirect("/")

            else:
                flash("Wrong username/password", 'danger')
                return render_template('user_login.html', form=form)

    return render_template("user_login.html", form = form)

@app.route("/recipes/favourites")
def show_favourites():
    if g.user:
        user = g.user
        favourites = user.favourite_recipes
        ratings = {rating.recipe_id: rating.rating for rating in Ratings.query.filter_by(user_id = user.id).all()}
        print(f"Ratings:{ratings}")
        return render_template("favourites.html", favourites = favourites, ratings=ratings)
    else:
        flash(f"You need to be logged in for that", 'danger')
        return redirect("/")

@app.route("/recipes/favourites/<spoonacular_id>/add", methods = ["POST"])
def add_recipe_to_favourites(spoonacular_id):
    if g.user:
            user = g.user
            recipe = Recipes.query.filter_by(spoonacular_id = spoonacular_id).one()
            new_favourite = Favourites(user_id = user.id, recipe_id = recipe.id)
            db.session.add(new_favourite)
            db.session.commit()
            return f"recipe {{recipe.id}} added to favourites for user {{user.id}}"
       

    else:
        
        flash(f"You need to be logged in for that", 'danger')
        return redirect("/")
    

@app.route("/recipes/favourites/<spoonacular_id>/remove", methods = ["POST"])
def delete_recipe_from_favourites(spoonacular_id):
    if g.user:
        user = g.user
        recipe = Recipes.query.filter_by(spoonacular_id = spoonacular_id).one()
        favourite = Favourites.query.filter(Favourites.recipe_id==recipe.id, Favourites.user_id==user.id).one()
        db.session.delete(favourite)
        db.session.commit()
        return f"recipe {{recipe.id}} removed from favourites for user {{user.id}}"
       
    else:
        
        flash(f"You need to be logged in for that", 'danger')
        return redirect("/")


@app.route("/users/delete", methods =["GET", "POST"])
def delete_user():
    if g.user:
        user = g.user
        db.session.delete(user)
        db.session.commit()
        flash(f"Deleted user {user.username}", 'danger')
        return redirect("/")
    else:
        flash(f"You need to be logged in for that", 'danger')
        return redirect("/")


@app.route("/users/edit", methods =["GET", "POST"])
def edit_user():
    if g.user:
        user = g.user
        form = UserEdit()

        if form.validate_on_submit():
            if Users.authenticate(username = user.username, password = form.password_conf.data):
                user.edit_user(password = form.new_password.data, email= form.email.data )
                db.session.commit()
                flash(f"User:{user.username} - Data changed", 'success')
                return redirect('/')
            else:
                flash("Wrong password confirmation", 'danger')
                return render_template('user_details.html', form=form, user = user)
        
            
        
        return render_template("user_details.html", user = user, form = form)
    else:
        flash(f"You need to be logged in for that", 'danger')
        return redirect("/")

@app.route("/recipes/favourites/rating", methods =["POST"])
def rate_recipe():
    if g.user:
        user = g.user
        rating = int(request.json["rating"])
        recipe_id = int(request.json["recipe_id"])
        print(rating)
        if Ratings.query.filter(Ratings.recipe_id==recipe_id, Ratings.user_id==user.id).all():
            print("existing rating")
            edit_rating = Ratings.query.filter(Ratings.recipe_id==recipe_id, Ratings.user_id==user.id).one()
            edit_rating.rating = rating
            db.session.add(edit_rating)
            db.session.commit()
            print(Ratings.query.all())
            return jsonify(edit_rating.serialize_rating(), 200)
        else:
            print("new rating")
            new_rating = Ratings(user_id=user.id, recipe_id = recipe_id, rating = rating)
            db.session.add(new_rating)
            db.session.commit()
            print(Ratings.query.all())
            return jsonify(new_rating.serialize_rating(), 200)
    else:
        flash(f"You need to be logged in for that", 'danger')
        return redirect("/")




