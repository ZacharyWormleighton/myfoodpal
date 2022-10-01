from IOHandler import IOHandler
from MyFitnessPalHandler import MyFitnessPalHandler
from LogLevel import LogLevel

io = IOHandler()
mfp = MyFitnessPalHandler()
mfp.log_level = LogLevel.INFO

print("Enter food search: ")
search = io.input_()
print("Enter quantity in grams (g):")
quantity = io.input_()

if search and quantity:
    mfp.food_search(search)
    mfp.calculate_quantities(float(quantity))
    mfp.pprint_results()
