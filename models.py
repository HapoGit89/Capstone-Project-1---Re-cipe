
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)


class Users(db.Model):
    """ Users Table """

    __tablename__ = "users"

    def  __repr__(self):
        return f"<User {self.id}, Name: {self.username}, Email: {self.email} "

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    username = db.Column(db.Text, unique = True,
                         nullable = False)
    password = db.Column (db.Text,
                          nullable = False
                          )
    email = db.Column(db.Text,
                      nullable = False)
    diet = db.Column(db.Text)

    favourite_recipes = db.relationship(
        "Recipes",
        secondary="favourites",
        backref = 'favouring_users'
    )
    ratings = db.relationship("Ratings", backref="rating_user", cascade="all, delete-orphan")
    rated_recipes = db.relationship(
        "Recipes",
        secondary="ratings", viewonly = True,
        backref = 'rating_users'
    )
    


class Recipes(db.Model):
    """ Recipes Table """

    __tablename__ = "recipes"

    def  __repr__(self):
        return f"<Recipe{self.id}, Title: {self.title}, spoonacular_id: {self.spoonacular_id} "

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    title = db.Column(db.Text,
                         nullable = False)
    spoonacular_id = db.Column(db.Integer, unique = True,
                               nullable = False)
    diets = db.Column(db.JSON)
    ready_in = db.Column(db.Integer)
    image_url = db.Column(db.String)
    cuisine = db.Column(db.String)
    health_score = db.Column(db.Integer)
    steps = db.Column(db.JSON)
    dairy_free = db.Column(db.Boolean)
    servings = db.Column(db.Integer)
    summary = db.Column(db.Text)
    users = db.relationship(
        "Users",
        secondary="favourites", viewonly = True,
        backref = 'favoured_recipes')
    ingredients = db.relationship(
        "Ingredients",
        secondary="recipe_ingredients",
        backref = 'recipes')
    recipe_ratings = db.relationship("Ratings", backref="ratied_recipe", cascade="all, delete-orphan")
    rated_by = db.relationship(
        "Users",
        secondary="ratings",
        backref = 'recipes_rated'
    )


class Ingredients(db.Model):
        """Ingredients Table"""

        __tablename__ = "ingredients"

        def __repr__(self):
            return f"Ingredient {self.id}, {self.name}"


        id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
        name = db.Column(db.String(50), unique = True,
                         nullable = False)
        image = db.Column(db.Text)
        spoonacular_id = db.Column(db.Integer, unique = True,
                          nullable = False)
        in_recipes = db.relationship(
        "Recipes",
        secondary="recipe_ingredients", viewonly = True,
        backref = 'used_ingredients')

        


class Favourites(db.Model):
        """Favourites Table"""

        __tablename__ = "favourites"

        def __repr__(self):
            return f"Favourite id:{self.id} for user {self.user_id} and recipe {self.recipe_id}"

        id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
        user_id = db.Column(db.Integer,
                db.ForeignKey('users.id', ondelete='cascade'))
        recipe_id = db.Column(db.Integer,
                    db.ForeignKey('recipes.id', ondelete='cascade'))
        db.UniqueConstraint('user_id', 'recipe_id')
        




class Ratings(db.Model):
        """Ratings Table"""

        __tablename__ = "ratings"

        def __repr__(self):
            return f"Rating id:{self.id} for user {self.user_id} and recipe {self.recipe_id} rating {self.rating}"

        id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
        rating = db.Column(db.Integer, 
                           nullable = False)
        user_id = db.Column(db.Integer,
                db.ForeignKey('users.id', ondelete='cascade'))
        recipe_id = db.Column(db.Integer,
                    db.ForeignKey('recipes.id', ondelete='cascade'))
        db.UniqueConstraint('user_id', 'recipe_id')

class RecipeIngredients(db.Model):
        """Ingredients used in Recipes"""

        __tablename__ = 'recipe_ingredients' 

        id = db.Column(
            db.Integer,
            primary_key=True
        )

        ingredient_id = db.Column(
            db.Integer,
            db.ForeignKey('ingredients.id', ondelete='cascade')
        )

        recipe_id = db.Column(
            db.Integer,
            db.ForeignKey('recipes.id', ondelete='cascade'),
            unique=True
        )
        db.UniqueConstraint('recipe_id', 'ingredient_id')






    