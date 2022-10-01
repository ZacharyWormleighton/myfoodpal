from myfitnesspal import fooditem

class MyFoodItem(fooditem.FoodItem):
    """
    A class to extend MyFitnessPal food items with a quantity for whole food item grams and quantity needed for recipe.

    ...

    Attributes
    ----------
    grams : float
        number of grams in whole food item
    quantity_needed : float
        number of whole food items required for recipe
    """
    grams = 0.0
    quantity_needed = 0.0

    def __init__(self, name, brand, verified, calories, grams):
        super().__init__(self, name, brand, verified, calories)
        self.grams = grams
        self.quantity_needed = 0.0