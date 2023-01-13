#Tyler Boechler
# tjb404
#11294509
#Mark Keil

import numpy as np

from a10q1 import import_data
from a10q1 import fruit_implementation
from a10q1 import grid_creation
from a10q1 import calculate_neighbours
from a10q1 import which_growth
from a10q1 import grid_spread


test_cases_import_data = [

    {"inputs":"pokefruit_celadonfarm.txt",
     "outputs":{'grid':5, 'firefruit': [['0', '2']], 'waterfruit': [['2', '0']], 'grassfruit': [['4', '2']], 'joltfruit': [['2', '4']]},
     "reason":"the file data should written in a dictionary in this manner"},
    
    {"inputs":"pokefruit_saffronfarm.txt",
     "outputs":{'grid': 100, 'firefruit': [['30', '16'], ['32', '49'], ['34', '18']], 'waterfruit': [['34', '32'], ['36', '37'], ['33', '33']], 'grassfruit': [['33', '37'], ['17', '18'], ['42', '26']], 'joltfruit': [['19', '21'], ['23', '21']]},
     "reason":"The output for a grid with multiple fruit coordinates"}]

test_cases_fruit_implementation = [

    
    """
    This function is not a fruitful function, testing was done by printing the array before and after the letters were put in and visually observed, as it alters a variable grid in a seperate function
    """]
    
test_cases_grid_creation = [

    {"inputs":{'grid':5, 'firefruit': [['0', '2']], 'waterfruit': [['2', '0']], 'grassfruit': [['4', '2']], 'joltfruit': [['2', '4']]},
     "outputs":np.array([['0', '0', 'w', '0', '0'],
                ['0', '0', '0', '0', '0'],
                ['f', '0', '0', '0', 'g'],
                ['0', '0', '0', '0', '0'],
                ['0', '0', 'j', '0', '0']]),
     "reason":"With the data in the dictionary, the arrray should take shape like this"},
    
    {"inputs":{'grid': 7, 'firefruit': [['0', '3'], ['5', '5']], 'waterfruit': [['6', '0'], ['1', '3']], 'grassfruit': [['6', '6'], ['5', '1']], 'joltfruit': [['3', '3']]},
     "outputs":np.array([['0', '0', '0', '0', '0', '0', 'w'],
                ['0', '0', '0', '0', '0', 'g', '0'],
                ['0', '0', '0', '0', '0', '0', '0'],
                ['f', 'w', '0', 'j', '0', '0', '0'],
                ['0', '0', '0', '0', '0', '0', '0'],
                ['0', '0', '0', '0', '0', 'f', '0'],
                ['0', '0', '0', '0', '0', '0', 'g']]),
     "reason":"With data with multiple fruit entries, the array should be like this"}]
    
test_cases_calculate_neighbours = [

    {"inputs":[np.array([['0', '0', '0', '0', '0', '0', 'w'],
                ['0', '0', '0', '0', '0', 'g', '0'],
                ['0', '0', '0', '0', '0', '0', '0'],
                ['f', 'w', '0', 'j', '0', '0', '0'],
                ['0', '0', '0', '0', '0', '0', '0'],
                ['0', '0', '0', '0', '0', 'f', '0'],
                ['0', '0', '0', '0', '0', '0', 'g']]), 2, 3],
     "outputs":["j"],
     "reason":"At the coordinate (3,2), the neighbours are j"},
    
    {"inputs":[np.array([['0', '0', '0', '0', '0', '0', 'w'],
                ['0', '0', '0', '0', '0', 'g', '0'],
                ['0', '0', '0', '0', '0', '0', '0'],
                ['f', 'w', '0', 'j', '0', '0', '0'],
                ['0', '0', '0', '0', '0', '0', '0'],
                ['0', '0', '0', '0', '0', 'f', '0'],
                ['0', '0', '0', '0', '0', '0', 'g']]),0, 0],
     "outputs":[],
     "reason":"there are no neighbours at 0,0"},
    
    {"inputs":[np.array([['0', '0', '0', '0', '0', '0', 'w'],
                ['0', '0', '0', '0', '0', 'g', '0'],
                ['0', '0', '0', '0', '0', '0', '0'],
                ['f', 'w', '0', 'j', '0', '0', '0'],
                ['0', '0', '0', '0', '0', '0', '0'],
                ['0', '0', '0', '0', '0', 'f', '0'],
                ['0', '0', '0', '0', '0', '0', 'g']]),2, 1],
     "outputs":["f", "w"],
     "reason":"there are 2 neighbours at 1,2 f and w"}]

test_cases_which_growth = [

    {"inputs":["f", "j", "w", "g"],
     "outputs":"m",
     "reason":"A megafruit will grow with all different neighbours"},
    
    {"inputs":["f", "w", "g"],
     "outputs":"0",
     "reason":"With these 3 plants, nothing is dominant"},
    
    {"inputs":["f", "w"],
     "outputs":"w",
     "reason":"w should be returned as water is dominant"},
    
    {"inputs":[],
     "outputs":"0",
     "reason":"The space stays the same with no neighbours"},

    {"inputs":["f"],
     "outputs":"f",
     "reason":"f should be returned as it's the only one"}]

test_cases_grid_spread = [

    {"inputs":np.array([['0', '0', '0', '0', '0', '0', 'w'],
                ['0', '0', '0', '0', '0', 'g', '0'],
                ['0', '0', '0', '0', '0', '0', '0'],
                ['f', 'w', '0', 'j', '0', '0', '0'],
                ['0', '0', '0', '0', '0', '0', '0'],
                ['0', '0', '0', '0', '0', 'f', '0'],
                ['0', '0', '0', '0', '0', '0', 'g']]),
     "outputs":np.array([['0', '0', '0', '0', 'g', 'g', 'w'],
                ['0', '0', '0', '0', 'g', 'g', 'g'],
                ['w', 'w', 'j', 'j', 'j', 'g', 'g'],
                ['f', 'w', 'j', 'j', 'j', '0', '0'],
                ['w', 'w', 'j', 'j', 'j', 'f', 'f'],
                ['0', '0', '0', '0', 'f', 'f', 'f'],
                ['0', '0', '0', '0', 'f', 'f', 'g']]),
     "reason":"This is how the fruit should spread"},
    
    {"inputs":np.array([['0', '0', '0', '0', '0'],
               ['0', '0', 'w', '0', '0'],
               ['0', 'f', '0', 'g', '0'],
               ['0', '0', 'j', '0', '0'],
               ['0', '0', '0', '0', '0']]),
     "outputs":np.array([['0', 'w', 'w', 'w', '0'],
                ['f', 'w', 'w', 'g', 'g'],
                ['f', 'f', 'm', 'g', 'g'],
                ['f', 'j', 'j', 'j', 'g'],
                ['0', 'j', 'j', 'j', '0']]),
     "reason":"A megafruit should be made"}]

#A driver for every function being tested
for test in test_cases_import_data:
    inputs = test["inputs"]
    result = import_data(inputs)
    if result != test["outputs"]:
        print("Testing fault: import_data() returned ",str(result), "on inputs", inputs,
              "(",test["reason"],")")

for test in test_cases_grid_creation:
    inputs = test["inputs"]
    result = grid_creation(inputs)
    equal = result == test["outputs"]
    if not equal.all():
        print("Testing fault: grid_creation() returned ",str(result), "on inputs", inputs,
              "(",test["reason"],")")
        
for test in test_cases_calculate_neighbours:
    inputs = test["inputs"]
    result = calculate_neighbours(inputs[0], inputs[1], inputs[2])
    if result != test["outputs"]:
        print("Testing fault: calculate_neighbours() returned ",str(result), "on inputs", inputs,
              "(",test["reason"],")")
        
for test in test_cases_which_growth:
    inputs = test["inputs"]
    result = which_growth(inputs)
    if result != test["outputs"]:
        print("Testing fault: which_growth() returned ",str(result), "on inputs", inputs,
              "(",test["reason"],")")
        
for test in test_cases_grid_spread:
    inputs = test["inputs"]
    result = grid_spread(inputs, False)
    equal = result == test["outputs"]

    if not equal.all():
        print("Testing fault: grid_spread() returned ",str(result), "on inputs", inputs,
              "(",test["reason"],")")
        
print("\n")
print("test complete")