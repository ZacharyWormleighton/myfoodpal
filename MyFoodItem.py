from myfitnesspal import fooditem

class MyFoodItem(fooditem.FoodItem):
    def __init__(self, name, brand, verified, calories, grams):
        super().__init__(self, name, brand, verified, calories)
        self.grams = grams
        self.quantity_needed = 0.0