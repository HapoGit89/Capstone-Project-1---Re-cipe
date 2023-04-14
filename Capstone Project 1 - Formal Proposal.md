# Capstone Project 1 - Proposal

__Project Goal:__  
The project goal is to offer a cooking recipe resource for users who want to be able to use very detailed search filters in order to take into account their intolerances, allergies, nutrition needs and tastes. The site should furthermore enable users to sign up and save favourite recipies as well as search filters to their account. Furthermore, recipes should include nutrition, health, sustainability and pricing facts.

__User Profile:__  
The site will mainly aim at users whose eating habits are challenged by food intolerances and allergies, special diets like vegan and vegatarian or are in need of very particular nutritients.

__Data used:__
I'm planning on using the [spoonacular api] (https://spoonacular.com/food-api). This is mainly due to the fact that spoonacular offers very detailed query options and over 5000 recipes. The complexSearch endpoint of this API enables queries with very detailed filters such as max/min nutrients, intolerances, cuisine type and many more. Nevertheless, the project should be built in a way that an api change can be accomplished with little adaptation.

__Project Setup:__

The project should be using a database made up of three relations with a M2M relationship. This should include a user table, recipe table and a savedrecipe table as a join table. The user table will include sensitive data which has to be handled with special care and should also use hash functions for sing in and login. 

The main challenge posed by the API  is the limit of queries included in the free plan. A solution for this is to design the backend with the goal to have as few api requests as possible and also use hard coded template data during the development stage. Furthermore I aim to use a API wrapper which formats the data coming from the API for use in the view functions. This should enable a more easy process of changing APIs if needed.

The user flow has two different experiences for logged in and not logged in users. Both start at a landing page which let the users search for recipes with basic filters. Logged in users can make use of more detailed search filters. Furthermore, on found recipes, logged in users should be able to save recipes and also click on ingredients in order to get more information. Moreover, logged in users should be able to save search filters for future requests. The save recipe and save search features are outside the CRUD scope.