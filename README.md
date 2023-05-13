# Capstone-Project-1---Re-cipe

Live at: https://re-cipe.onrender.com

This web service is called Re:Cipe and lets users search for, save and rate cooking recipes.

The features are:

- Recipe search using queries and advanced search filters
- Recipe detail pages listing diet information, ingredients, and preparation steps
- SignIn and LogIn for users
- Marking recipes as "favourites" for logged in users
- Rating recipes for logged in users

I implemented the above features because I wanted to create a free, easy to use recipe website which lets users search for recipes with more advanced filtering methods. This comes from my own experience of recipe web services either being free with only query based searches or being subscription based with advanced filtering. Furthermore, since I personally like to save recipes when I see them in order to try them some time later, I wanted to add a "favourites" and "rating" feature.

A standard user flow could look like:

Without a user profile:
- Accessing the site via https://re-cipe.onrender.com
- Searching for recipes using queries and filters
- Looking at recipe details via "show details" button

With user profile:
- Accesing site via https://re-cipe.onrender.com
- LogIn or SignIn via Navbar
- Searching for recipes
- Acessing recipe details
- Mark down favourite recipes via star icon on recipe detail page
- Access user favourites via navbar
- Rate favourite recipes via heart-icons on "Favourites" Page
- LogOut via navbar




The API used is called "Spoonacular API". 
API Link: https://spoonacular.com/food-api
I like the API for the detailed recipe information and ease of use. However, I encountered some difficulties when certain search filter combinations canceled each other out. Also, when accessing the recipe detail endpoint, some responses did deviate from standard format which I tried to handle in the wrapper functions.

The Teck Stack used to build this web service is:

- HTML
- CSS/Twitter Bootstrap
- Python
- Flask
- WTForms
- Javascript


