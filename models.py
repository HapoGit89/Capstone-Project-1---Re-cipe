
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

    def render_favourites_spoonacular_ids(self):
         favourites = [favourite.spoonacular_id for favourite in self.favourite_recipes]
         return favourites
    
    @classmethod
    def signup(cls, username, email, password):
        """Sign up user and add hashed password to DB """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        
        user = Users(
            username=username,
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Checks if user is in db and hashed password mathes password in DB"""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

    
    


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
    diets = db.Column(db.PickleType)
    ready_in = db.Column(db.Integer)
    image_url = db.Column(db.String)
    cuisine = db.Column(db.PickleType)
    health_score = db.Column(db.Integer)
    steps = db.Column(db.Text)
    dairy_free = db.Column(db.Boolean)
    gluten_free = db.Column(db.Boolean)
    vegan = db.Column(db.Boolean)
    vegetarian = db.Column(db.Boolean)
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
    def render_ingredients(self):
        ingredients = [{'name': ingredient.name,
                        'image': ingredient.image,
                        'amount': RecipeIngredients.query.filter(RecipeIngredients.recipe_id == self.id, RecipeIngredients.ingredient_id == ingredient.id).one().amount} for ingredient in self.ingredients]
        return ingredients
    
    @classmethod
    def is_recipe_in_db(cls,recipe_id):
        recipes_in_db_id = [recipe.spoonacular_id for recipe in cls.query.all()]
        if recipe_id in recipes_in_db_id:
             return True
        else:
             return False
    
    @classmethod
    def add_new_recipe(cls, recipe):
        new_recipe = cls(title = recipe['title'],
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
        return new_recipe
         
         




class Ingredients(db.Model):
        """Ingredients Table"""

        __tablename__ = "ingredients"

        def __repr__(self):
            return f"Ingredient {self.id}, {self.name}"


        id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
        name = db.Column(db.String,
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

        __table_args__ = (db.UniqueConstraint('recipe_id', 'user_id', name = "favourite_comb"),)


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

        __table_args__ = (db.UniqueConstraint('recipe_id', 'ingredient_id', name = "recipe_id_comb"),)

        id = db.Column(
            db.Integer,
            primary_key=True
        )

        ingredient_id = db.Column(
            db.Integer,
            db.ForeignKey('ingredients.id', ondelete='cascade')
        )
        amount = db.Column(db.Text)
        
        recipe_id = db.Column(
            db.Integer,
            db.ForeignKey('recipes.id', ondelete='cascade'),
        )

        
        # unique = db.UniqueConstraint('recipe_id', 'ingredient_id', name = "recipe_id_comb")






    