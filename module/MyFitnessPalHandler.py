import myfitnesspal
from MyFoodItem import MyFoodItem
from LogLevel import LogLevel
import re

class MyFitnessPalHandler:
    """
    A class to handle MyFitnessPal integration and quantities calculation.

    ...

    Attributes
    ----------
    log_level : LogLevel
        level of logging to output to console
    client : myfitnesspal.Client
        client for MyFitnessPal API
    unprocessed_food_items : [MyFitnessPal.FoodItem]
        list of food items returned from API search
    usable_food_items : MyFoodItem
        list of usable food items that have been processed by MyFoodPal

    Methods
    -------
    __extract_usable_grams_from_food_item(item):
        Returns the number of grams found, using regex, from a food item name or a whole food item serving.
    __extract_usable_food_items(food_items):
        Returns a list of usable MyFoodPal items from a MyFitnessPal food list.
    food_search(search):
        Returns a list of usable MyFoodItem items from the MyFitnessPal DB.
    calculate_quantities(recipe_quantity):
        Returns a list of usable MyFoodItem items after calculating the quantities of each required for the desired recipe quantity.
    pprint_results():
        Pretty prints the MyFoodItem results.
    """
    log_level = LogLevel.DEBUG
    client = None
    unprocessed_food_items = []
    usable_food_items = []

    def __init__(self):
        self.client = myfitnesspal.Client()

    # Extract grams measurements from food items using regex.
    def __extract_usable_grams_from_food_item(self, item):
        '''
        Returns the number of grams found, using regex, from a food item name or a whole food item serving.

                Parameters:
                        item (MyFitnessPal.FoodItem): A valid MyFitnessPal food item

                Returns:
                        grams (float): Number of grams of whole food item
        '''
        # Forms of grams
        # "X grams"
        # "X gs"
        # "X g"
        # "Xg"
        grams = -1
        gramsWithUnitExpression = "(([0-9])\w+( gs |g| g)|([0-9].)+([0-9])\w+( gs |g| g))"
        result = re.search(gramsWithUnitExpression, item)
        gramsExpression = "([0-9])+"
        try:
            result = re.search(gramsExpression, result.group(0))
            grams = float(result.group(0))
        except AttributeError as e: # TODO: Update regex handling to better handle "200.0 gs" form, improve error handling
            if self.log_level == LogLevel.DEBUG:
                print(e)
        if grams < 0 and self.log_level == LogLevel.DEBUG: print("Error: Failed to extract grams") 
        return grams
    
    # Filter list to only those items with grams in the name or container / package serving.
    def __extract_usable_food_items(self, food_items):
        '''
        Returns a list of usable MyFoodPal items from a MyFitnessPal food list.

                Parameters:
                        food_items ([MyFitnessPal.FoodItem]): A list of MyFitnessPal food items

                Returns:
                        usable_food_items ([MyFoodItem]): A list of food items
        '''
        for item in food_items:
            # Check if grams are found in the food item name.
            if ("grams" in item.name) or ("g" in item.name):
                grams = self.__extract_usable_grams_from_food_item(item.name)
                mfi = MyFoodItem(item.name, item.brand, item.verified, item.calories, grams)
                self.usable_food_items.append(mfi)
                continue
            # Check if grams are found in the food item servings (for containers or packages).
            for serving in item.servings:
                if ("container" in serving.unit) and (
                    ("grams" in serving.unit) or ("g" in serving.unit)):
                    grams = self.__extract_usable_grams_from_food_item(serving.unit)
                    mfi = MyFoodItem(item.name, item.brand, item.verified, item.calories, grams)
                    self.usable_food_items.append(mfi)
                    continue
        return self.usable_food_items

    # Perform MyFitnessPal food item search.
    def food_search(self, search):
        '''
        Returns a list of usable MyFoodItem items from the MyFitnessPal DB.

                Parameters:
                        search (string): A food item search term

                Returns:
                        usable_food_items ([MyFoodItem]): A list of food items
        '''
        if (self.log_level == LogLevel.INFO) or (self.log_level == LogLevel.DEBUG): print("Searching...")
        self.unprocessed_food_items = self.client.get_food_search_results(search)
        if (self.log_level == LogLevel.INFO) or (self.log_level == LogLevel.DEBUG): print("Extracting usable food items...")
        self.__extract_usable_food_items(self.unprocessed_food_items)
        return self.usable_food_items

    # Calculate quantities of each food item required to satisfy recipe and update quantities in MyFoodItem object.
    def calculate_quantities(self, recipe_quantity):
        '''
        Returns a list of usable MyFoodItem items after calculating the quantities of each required for the desired recipe quantity.

                Parameters:
                        recipe_quantity (float): A quantity of the food item desired

                Returns:
                        usable_food_items ([MyFoodItem]): A list of food items
        '''
        if (self.log_level == LogLevel.INFO) or (self.log_level == LogLevel.DEBUG): print("Calculating quantities...")
        for item in self.usable_food_items:
            item.quantity_needed = round(recipe_quantity / item.grams, 2)
        return self.usable_food_items
    
    # Pretty print MyFoodItem results
    def pprint_results(self):
        '''
        Pretty prints the MyFoodItem results.
        '''
        for item in self.usable_food_items:
            print("x{} needed, {}g, {} ({}), cals={}, verified={}".format(
                item.quantity_needed,
                item.grams,
                item.name,
                item.brand,
                item.calories,
                item.verified
            ))
