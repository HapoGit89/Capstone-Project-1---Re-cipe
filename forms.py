
from random import choices
from flask_wtf import FlaskForm
from wtforms import StringField, widgets, PasswordField, TextAreaField, BooleanField, SelectField, SelectMultipleField



cuisines = [(' ', 'None'),('african', 'African'), ('american', 'American'), ('british', 'British'), ('cajun', 'Cajun'), ('carribean', 'Carribean'), ('chinese', 'Chinese'), ('eastern european', 'Eastern European'), ('european', 'European'), ('french', 'French'), ('german', 'German'), ('greek', 'Greek'), ('indian', 'Indian'), ('irish', 'Irish'),
             ('italian', 'Italian'), ('japanese', 'Japanese'), ('jewish', 'Jewish'), ('korean', 'Korean'), ('latin american', 'Latin American'), ('mediterranean', 'Meditarranean'), ('mexican', 'Mexican'), ('middle eastern', 'Middle Eastern'), ('nordic', 'Nordic'), ('southern', 'Southern'), ('spanish', 'Spanish'), ('thai', 'Thai'), ('vietnamese', 'Vietnamese')]
diets = [('ketogenic', 'Ketogenic'), ('lacto-vegetarian', 'Lacto-Vegetarian'), ('ovo-vegetarian', 'Ovo-Vegetarian'),
         ('pescetarian', 'Pescetarian'), ('paleo', 'Paleo'), ('primal', 'Primal'), ('low%20fodmap', 'Low FODMAP'), ('whole30', 'Whole30')]
intolerances = [('dairy', 'Dairy'), ('egg', 'Egg'), ('gluten', 'Gluten'), ('grain', 'Grain'), ('peanut', 'Peanut'), ('seafood', 'Seafood'), ('sesame', 'Sesame'), ('shellfish', 'Shellfish'), ('soy', 'Soy'), ('sulfite', 'Sulfite'), ('treenut', 'Tree Nut'), ('wheat', 'Wheat')]




class SearchForm(FlaskForm):
    """Form for complex recipe search"""

    query = StringField('Search for')
    veggie = BooleanField('veggie')
    vegan = BooleanField('vegan')
    gluten_free = BooleanField('gluten-free')
    dairy_free = BooleanField('dairy-free')
    diet = SelectMultipleField('diet (select mulitple pressing cmd)', choices = diets)
    cuisine = SelectField('cuisine', choices = cuisines)
    intolerance = SelectMultipleField('intolerance (select mulitple pressing cmd)', choices = intolerances)
    exclude = StringField ('exclude (if multiple seperate by comma)')

