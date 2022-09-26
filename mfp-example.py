import myfitnesspal
from MyFoodItem import MyFoodItem
import re

# Filter list to only list containing container or package terms in servings with grams 
def extractUsableFoodItems(food_items):
    new_food_items = []
    for item in food_items:
        for serving in item.servings:
            #print(type(serving.unit))
            if ("container" in serving.unit) and (("grams" in serving.unit) or ("g" in serving.unit)):
                grams = extractUsableGramsFromFoodItem(serving.unit)
                #print(type(item))
                mfi = MyFoodItem(item.name, item.brand, item.verified, item.calories, grams)
                new_food_items.append(mfi)
                #print(serving.unit)
                continue
    return new_food_items

# Extract grams measurements from food items using regex
def extractUsableGramsFromFoodItem(item):
    # Forms of grams
    # "X grams"
    # "X gs"
    # "X g"
    # "Xg"
    grams = -1
    gramsWithUnitExpression = "(([0-9])\w+( gs |g| g)|([0-9].)+([0-9])\w+( gs |g| g))"#"([0-9])\w+( gs |g| grams| g)"
    result = re.search(gramsWithUnitExpression, item)
    gramsExpression = "([0-9])+"
    try:
        result = re.search(gramsExpression, result.group(0))
        grams = float(result.group(0))#
    except AttributeError as e: # TODO: Update regex handling to better handle "200.0 gs" form, improve error handling
        print(e)
    return grams

# Calculate quantities of each food item required to satisfy recipe
def calculateQuantities(recipe_quantity, food_items):
    #quantities = []
    for item in food_items:
        item.quantity_needed = round(recipe_quantity / item.grams, 2)

# Pretty print MyFoodItem
def pprintFoodItem(items):
    for item in items:
        print("x{} needed, {}g, {} ({}), cals={}, verified={}".format(
            item.quantity_needed,
            item.grams,
            item.name,
            item.brand,
            #item.servings[3].unit,
            #item.servings,
            item.calories,
            item.verified
        ))

# Pretty print MFP Food Item
def pprintMFPFoodItem(items):
    for item in items:
        print("{} ({}), {}, cals={}, verified={}".format(
            item.name,
            item.brand,
            item.servings,
            item.calories,
            item.verified
        ))

client = myfitnesspal.Client()

food_items = client.get_food_search_results("cream cheese")
#print(dir(food_items[0]))
pprintMFPFoodItem(food_items)

foodItems = extractUsableFoodItems(food_items)

recipeQuantity = 220.0 # 220g of cream cheese needed in recipe
calculateQuantities(recipeQuantity, foodItems)

print(type(foodItems))
pprintFoodItem(foodItems)
print(len(foodItems))



