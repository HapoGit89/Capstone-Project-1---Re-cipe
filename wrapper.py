from flask import Flask, request

import requests

# apiKey = "3de123cdc6f14ce0a9bc46a5e5edeb2d "

def complex_recipe_search(query, veggie, vegan, gluten_free, dairy_free, diets, cuisine, intolerance, exclude):
    """ Returns a python dict containing Spoonacular Compley Search Results for given arguments"""
    
  
    if veggie == True and len(diets)>0:
        diets += ',vegetarian'
    elif veggie == True:
        diets +='vegetarian'
    if vegan == True:
        diets += ',vegan'
    if gluten_free == True:
        diets += ',gluten%20free'
    if dairy_free == True:
        diets += ',dairy%20free'

    url = "https://api.spoonacular.com/recipes/complexSearch?apiKey=3de123cdc6f14ce0a9bc46a5e5edeb2d&number=100" 
    if query:
        url += f"&query={query}"
    if cuisine:
        url += f"&cuisine={cuisine}"
    if diets:
        url += f"&diet={diets}"
    if intolerance:
        url += f"&intolerances={intolerance}"
    if exclude:
        url += f"&excludeIngredients={exclude}"

    print(url)

    response = requests.get(url)
    response_dict = response.json()
    
    resp = response_dict
    formatted_recipes = {'results':[{'spoonacular_id' : recipe['id'], 'title': recipe['title'], 'image_url': recipe ['image']} for recipe in resp['results']], 'totalResults': resp['totalResults']}
    return formatted_recipes




def recipe_detail_search(recipe_spoonacular_id):
    """Returns Recipe Details for given spoonacular_id"""
    
    resp = requests.get(f"https://api.spoonacular.com/recipes/{recipe_spoonacular_id}/information?apiKey=3de123cdc6f14ce0a9bc46a5e5edeb2d")
    response_dict = resp.json()
   
    ingredients = [{'spoonacular_ingredient_id': ingredient['id'], 'name': ingredient['name'], 'image': ingredient['image'], 'amount' : f"{ingredient['amount']} {ingredient['unit']}"} for ingredient in response_dict['extendedIngredients']]
    formatted_details = {'title': response_dict['title'], 'spoonacular_id': response_dict['id'], 'diets': response_dict['diets'], 'readyIn': response_dict['readyInMinutes'], 'image_url': response_dict.get('image'), 'cuisines': response_dict['cuisines'], 'health_score': response_dict['healthScore'], 'ingredients': ingredients, 'steps': response_dict['instructions'], 'summary': response_dict['summary'], 'vegan': response_dict['vegan'], 'vegetarian': response_dict['vegetarian'], 'servings': response_dict['servings'], 'glutenFree': response_dict['glutenFree'], 'dairyFree': response_dict['dairyFree'] }
    return formatted_details































# response_hard_coded = {'results': [{'id': 653251,           # hard coded sample response for complex Search Endpoint with query = "noodles" and number = 50
#    'title': 'Noodles and Veggies With Peanut Sauce',
#    'image': 'https://spoonacular.com/recipeImages/653251-312x231.jpg',
#    'imageType': 'jpg'},
#   {'id': 658270,
#    'title': 'Rice Noodles With Wonton/chinese Ravioli In Mushroom Sauce',
#    'image': 'https://spoonacular.com/recipeImages/658270-312x231.jpg',
#    'imageType': 'jpg'},
#   {'id': 632854,
#    'title': 'Asian Noodles',
#    'image': 'https://spoonacular.com/recipeImages/632854-312x231.jpg',
#    'imageType': 'jpg'},
#   {'id': 641221,
#    'title': 'Dan Dan Noodles',
#    'image': 'https://spoonacular.com/recipeImages/641221-312x231.jpg',
#    'imageType': 'jpg'},
#   {'id': 795513,
#    'title': 'Zucchini Noodles with Pesto',
#    'image': 'https://spoonacular.com/recipeImages/795513-312x231.jpg',
#    'imageType': 'jpg'},
#   {'id': 664573,
#    'title': 'Vegetable Noodles',
#    'image': 'https://spoonacular.com/recipeImages/664573-312x231.jpg',
#    'imageType': 'jpg'},
#   {'id': 639927,
#    'title': 'Cold Soba Noodles',
#    'image': 'https://spoonacular.com/recipeImages/639927-312x231.jpg',
#    'imageType': 'jpg'},
#   {'id': 634629,
#    'title': 'Beef Lo Mein Noodles',
#    'image': 'https://spoonacular.com/recipeImages/634629-312x231.jpg',
#    'imageType': 'jpg'},
#   {'id': 647384,
#    'title': 'Hot and Spicy Noodles With Vegetables',
#    'image': 'https://spoonacular.com/recipeImages/647384-312x231.jpg',
#    'imageType': 'jpg'},
#   {'id': 665527,
#    'title': 'Yellow Squash Noodles with Tomato Basil Sauce',
#    'image': 'https://spoonacular.com/recipeImages/665527-312x231.jpg',
#    'imageType': 'jpg'},
#   {'id': 637643,
#    'title': 'Cheesy Chicken Noodles',
#    'image': 'https://spoonacular.com/recipeImages/637643-312x231.jpg',
#    'imageType': 'jpg'},
#   {'id': 1096250,
#    'title': 'Pho With Zucchini Noodles',
#    'image': 'https://spoonacular.com/recipeImages/1096250-312x231.jpg',
#    'imageType': 'jpg'},
#   {'id': 649557,
#    'title': 'Lemon Chicken With Noodles',
#    'image': 'https://spoonacular.com/recipeImages/649557-312x231.jpg',
#    'imageType': 'jpg'},
#   {'id': 1095743,
#    'title': 'Coconut Curry Ramen Noodles',
#    'image': 'https://spoonacular.com/recipeImages/1095743-312x231.jpg',
#    'imageType': 'jpg'},
#   {'id': 652078,
#    'title': 'Miso Soup With Thin Noodles',
#    'image': 'https://spoonacular.com/recipeImages/652078-312x231.jpg',
#    'imageType': 'jpg'},
#   {'id': 641111,
#    'title': 'Curry Beef Over Rice Noodles',
#    'image': 'https://spoonacular.com/recipeImages/641111-312x231.jpg',
#    'imageType': 'jpg'},
#   {'id': 662709,
#    'title': 'Szechuan-Style Shirataki Noodles',
#    'image': 'https://spoonacular.com/recipeImages/662709-312x231.jpg',
#    'imageType': 'jpg'},
#   {'id': 658058,
#    'title': 'Red Curry Stew & Vegetable Noodles',
#    'image': 'https://spoonacular.com/recipeImages/658058-312x231.jpg',
#    'imageType': 'jpg'},
#   {'id': 638382,
#    'title': 'Chicken Teriyaki with Soba Noodles',
#    'image': 'https://spoonacular.com/recipeImages/638382-312x231.jpg',
#    'imageType': 'jpg'},
#   {'id': 640666,
#    'title': 'Creamy Mushrooms Over Soba Noodles (Vegan)',
#    'image': 'https://spoonacular.com/recipeImages/640666-312x231.jpg',
#    'imageType': 'jpg'},
#   {'id': 653304,
#    'title': 'Not Momofuku Ginger Scallion Noodles',
#    'image': 'https://spoonacular.com/recipeImages/653304-312x231.jpg',
#    'imageType': 'jpg'},
#   {'id': 654318,
#    'title': 'Pad Se Ew Tofu With Vegetable Noodles',
#    'image': 'https://spoonacular.com/recipeImages/654318-312x231.jpg',
#    'imageType': 'jpg'},
#   {'id': 634421,
#    'title': 'Basil & Black Pepper Beef With Egg Noodles',
#    'image': 'https://spoonacular.com/recipeImages/634421-312x231.jpg',
#    'imageType': 'jpg'},
#   {'id': 661026,
#    'title': 'Spicy Beef, Pepper & Asparagus Udon Noodles',
#    'image': 'https://spoonacular.com/recipeImages/661026-312x231.jpg',
#    'imageType': 'jpg'},
#   {'id': 637440,
#    'title': 'Chapchae (Korean Stir-Fried Noodles)',
#    'image': 'https://spoonacular.com/recipeImages/637440-312x231.jpg',
#    'imageType': 'jpg'},
#   {'id': 649029,
#    'title': 'Korean Bibim Naengmyun (Instant Spicy Cold Noodles)',
#    'image': 'https://spoonacular.com/recipeImages/649029-312x231.jpg',
#    'imageType': 'jpg'},
#   {'id': 633876,
#    'title': 'Baked Ziti',
#    'image': 'https://spoonacular.com/recipeImages/633876-312x231.jpg',
#    'imageType': 'jpg'},
#   {'id': 633711,
#    'title': 'Baked Penne',
#    'image': 'https://spoonacular.com/recipeImages/633711-312x231.jpg',
#    'imageType': 'jpg'},
#   {'id': 659907,
#    'title': 'Shrimp & Orzo',
#    'image': 'https://spoonacular.com/recipeImages/659907-312x231.jpg',
#    'imageType': 'jpg'},
#   {'id': 633766,
#    'title': 'Baked Rigatoni',
#    'image': 'https://spoonacular.com/recipeImages/633766-312x231.jpg',
#    'imageType': 'jpg'}],
#  'offset': 0,
#  'number': 30,
#  'totalResults': 262}


# receipt_details_response_hard_coded = {'vegetarian': True,
#  'vegan': False,
#  'glutenFree': False,
#  'dairyFree': False,
#  'veryHealthy': True,
#  'cheap': False,
#  'veryPopular': False,
#  'sustainable': False,
#  'lowFodmap': False,
#  'weightWatcherSmartPoints': 13,
#  'gaps': 'no',
#  'preparationMinutes': -1,
#  'cookingMinutes': -1,
#  'aggregateLikes': 3,
#  'healthScore': 79,
#  'creditsText': 'foodista.com',
#  'sourceName': 'foodista.com',
#  'pricePerServing': 185.54,
#  'extendedIngredients': [{'id': 11090,
#    'aisle': 'Produce',
#    'image': 'broccoli.jpg',
#    'consistency': 'SOLID',
#    'name': 'broccoli flowerets',
#    'nameClean': 'broccoli',
#    'original': '14 ounces frozen broccoli flowerets',
#    'originalName': 'frozen broccoli flowerets',
#    'amount': 14.0,
#    'unit': 'ounces',
#    'meta': ['frozen'],
#    'measures': {'us': {'amount': 14.0,
#      'unitShort': 'oz',
#      'unitLong': 'ounces'},
#     'metric': {'amount': 396.893, 'unitShort': 'g', 'unitLong': 'grams'}}},
#   {'id': 2003,
#    'aisle': 'Spices and Seasonings',
#    'image': 'basil.jpg',
#    'consistency': 'SOLID',
#    'name': 'basil',
#    'nameClean': 'dried basil',
#    'original': '1 teaspoon dried basil',
#    'originalName': 'dried basil',
#    'amount': 1.0,
#    'unit': 'teaspoon',
#    'meta': ['dried'],
#    'measures': {'us': {'amount': 1.0,
#      'unitShort': 'tsp',
#      'unitLong': 'teaspoon'},
#     'metric': {'amount': 1.0, 'unitShort': 'tsp', 'unitLong': 'teaspoon'}}},
#   {'id': 2018,
#    'aisle': 'Spices and Seasonings',
#    'image': 'fennel-seeds.jpg',
#    'consistency': 'SOLID',
#    'name': 'fennel seeds',
#    'nameClean': 'fennel seeds',
#    'original': '1/4 teaspoon fennel seeds',
#    'originalName': 'fennel seeds',
#    'amount': 0.25,
#    'unit': 'teaspoon',
#    'meta': [],
#    'measures': {'us': {'amount': 0.25,
#      'unitShort': 'tsps',
#      'unitLong': 'teaspoons'},
#     'metric': {'amount': 0.25, 'unitShort': 'tsps', 'unitLong': 'teaspoons'}}},
#   {'id': 10011549,
#    'aisle': 'Pasta and Rice',
#    'image': 'tomato-sauce-or-pasta-sauce.jpg',
#    'consistency': 'SOLID',
#    'name': 'pasta sauce',
#    'nameClean': 'pasta sauce',
#    'original': '26 ounces pasta sauce',
#    'originalName': 'pasta sauce',
#    'amount': 26.0,
#    'unit': 'ounces',
#    'meta': [],
#    'measures': {'us': {'amount': 26.0,
#      'unitShort': 'oz',
#      'unitLong': 'ounces'},
#     'metric': {'amount': 737.088, 'unitShort': 'g', 'unitLong': 'grams'}}},
#   {'id': 11220420,
#    'aisle': 'Pasta and Rice',
#    'image': 'rigatoni.jpg',
#    'consistency': 'SOLID',
#    'name': 'rigatoni',
#    'nameClean': 'rigatoni',
#    'original': '1 pound rigatoni',
#    'originalName': 'rigatoni',
#    'amount': 1.0,
#    'unit': 'pound',
#    'meta': [],
#    'measures': {'us': {'amount': 1.0, 'unitShort': 'lb', 'unitLong': 'pound'},
#     'metric': {'amount': 453.592, 'unitShort': 'g', 'unitLong': 'grams'}}},
#   {'id': 1001026,
#    'aisle': 'Cheese',
#    'image': 'shredded-cheese-white.jpg',
#    'consistency': 'SOLID',
#    'name': 'mozzarella cheese',
#    'nameClean': 'shredded mozzarella',
#    'original': '6 ounces mozzarella cheese, part skim milk shredded',
#    'originalName': 'mozzarella cheese, part skim milk shredded',
#    'amount': 6.0,
#    'unit': 'ounces',
#    'meta': ['shredded'],
#    'measures': {'us': {'amount': 6.0, 'unitShort': 'oz', 'unitLong': 'ounces'},
#     'metric': {'amount': 170.097, 'unitShort': 'g', 'unitLong': 'grams'}}},
#   {'id': 11529,
#    'aisle': 'Produce',
#    'image': 'tomato.png',
#    'consistency': 'SOLID',
#    'name': 'ready-cut tomatoes',
#    'nameClean': 'tomato',
#    'original': '14 1/2 ounces canned ready-cut diced tomatoes drained',
#    'originalName': 'canned ready-cut diced tomatoes drained',
#    'amount': 14.5,
#    'unit': 'ounces',
#    'meta': ['diced', 'canned', 'drained'],
#    'measures': {'us': {'amount': 14.5,
#      'unitShort': 'oz',
#      'unitLong': 'ounces'},
#     'metric': {'amount': 411.068, 'unitShort': 'g', 'unitLong': 'grams'}}},
#   {'id': 16147,
#    'aisle': 'Frozen',
#    'image': 'veggie-burger-patty.png',
#    'consistency': 'SOLID',
#    'name': 'vegetable burger crumbles',
#    'nameClean': 'veggie burger',
#    'original': '6 ounces frozen vegetable burger crumbles',
#    'originalName': 'frozen vegetable burger crumbles',
#    'amount': 6.0,
#    'unit': 'ounces',
#    'meta': ['frozen'],
#    'measures': {'us': {'amount': 6.0, 'unitShort': 'oz', 'unitLong': 'ounces'},
#     'metric': {'amount': 170.097, 'unitShort': 'g', 'unitLong': 'grams'}}}],
#  'id': 633766,
#  'title': 'Baked Rigatoni',
#  'readyInMinutes': 45,
#  'servings': 6,
#  'sourceUrl': 'http://www.foodista.com/recipe/78KGC5QF/baked-rigatoni',
#  'image': 'https://spoonacular.com/recipeImages/633766-556x370.jpg',
#  'imageType': 'jpg',
#  'summary': 'Need a <b>lacto ovo vegetarian main course</b>? Baked Rigatoni could be a spectacular recipe to try. One serving contains <b>481 calories</b>, <b>25g of protein</b>, and <b>10g of fat</b>. This recipe serves 6. For <b>$1.86 per serving</b>, this recipe <b>covers 34%</b> of your daily requirements of vitamins and minerals. 3 people have made this recipe and would make it again. A mixture of broccoli flowerets, basil, vegetable burger crumbles, and a handful of other ingredients are all it takes to make this recipe so flavorful. From preparation to the plate, this recipe takes approximately <b>45 minutes</b>. It is brought to you by Foodista. Overall, this recipe earns a <b>spectacular spoonacular score of 93%</b>. Users who liked this recipe also liked <a href="https://spoonacular.com/recipes/rigatoni-al-forno-baked-rigatoni-with-roasted-asparagus-and-on-115058">Rigatoni Al Forno (Baked Rigatoni) with Roasted Asparagus and On</a>, <a href="https://spoonacular.com/recipes/baked-rigatoni-76933">Baked Rigatoni</a>, and <a href="https://spoonacular.com/recipes/baked-rigatoni-408338">Baked Rigatoni</a>.',
#  'cuisines': [],
#  'dishTypes': ['side dish', 'lunch', 'main course', 'main dish', 'dinner'],
#  'diets': ['lacto ovo vegetarian'],
#  'occasions': [],
#  'winePairing': {'pairedWines': [], 'pairingText': '', 'productMatches': []},
#  'instructions': '<ol><li>1. Preheat oven to 400 degrees. Cook pasta according to package directions, drain.</li><li>2. Combine pasta, pasta sauce, tomatoes, broccoli, burger crumbles, basil, fennel seeds and 4 oz. of the mozzarella in a 9x13 baking dish. Top with remaining 2 oz. mozzarella. Bake until heated through, about 20 minutes.</li></ol>',
#  'analyzedInstructions': [{'name': '',
#    'steps': [{'number': 1,
#      'step': 'Preheat oven to 400 degrees. Cook pasta according to package directions, drain.',
#      'ingredients': [{'id': 20420,
#        'name': 'pasta',
#        'localizedName': 'pasta',
#        'image': 'fusilli.jpg'}],
#      'equipment': [{'id': 404784,
#        'name': 'oven',
#        'localizedName': 'oven',
#        'image': 'oven.jpg'}]},
#     {'number': 2,
#      'step': 'Combine pasta, pasta sauce, tomatoes, broccoli, burger crumbles, basil, fennel seeds and 4 oz. of the mozzarella in a 9x13 baking dish. Top with remaining 2 oz. mozzarella.',
#      'ingredients': [{'id': 2018,
#        'name': 'fennel seeds',
#        'localizedName': 'fennel seeds',
#        'image': 'fennel-seeds.jpg'},
#       {'id': 10011549,
#        'name': 'pasta sauce',
#        'localizedName': 'pasta sauce',
#        'image': 'tomato-sauce-or-pasta-sauce.jpg'},
#       {'id': 1026,
#        'name': 'mozzarella',
#        'localizedName': 'mozzarella',
#        'image': 'mozzarella.png'},
#       {'id': 11090,
#        'name': 'broccoli',
#        'localizedName': 'broccoli',
#        'image': 'broccoli.jpg'},
#       {'id': 11529,
#        'name': 'tomato',
#        'localizedName': 'tomato',
#        'image': 'tomato.png'},
#       {'id': 2044,
#        'name': 'basil',
#        'localizedName': 'basil',
#        'image': 'basil.jpg'},
#       {'id': 20420,
#        'name': 'pasta',
#        'localizedName': 'pasta',
#        'image': 'fusilli.jpg'}],
#      'equipment': [{'id': 404646,
#        'name': 'baking pan',
#        'localizedName': 'baking pan',
#        'image': 'roasting-pan.jpg'}]},
#     {'number': 3,
#      'step': 'Bake until heated through, about 20 minutes.',
#      'ingredients': [],
#      'equipment': [{'id': 404784,
#        'name': 'oven',
#        'localizedName': 'oven',
#        'image': 'oven.jpg'}],
#      'length': {'number': 20, 'unit': 'minutes'}}]}],
#  'originalId': None,
#  'spoonacularSourceUrl': 'https://spoonacular.com/baked-rigatoni-633766'}





