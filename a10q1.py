#Tyler Boechler
#tjb404
#11294509
#Mark Keil

import numpy as np

#a list to understand the file data
data_comprehension = ["grid", "firefruit", "waterfruit", "grassfruit", "joltfruit"]

def import_data(file_name):
    """
Imports a file of the grid data and takes in each line as its respective value representation into a dictionary
param file_name: the name of the .txt file
returns: a dictionary of the data with its respective keys
    """
    #opening file and initial variables
    file = open(file_name, "r")
    data = {}
    data_list = []
    #What the data in the file represents
    
    # a counter for list indices
    counter = 0
    
    for line in file:
        #iterating through the file and adding the data to the dictionary with its respective label
        data_list.append(line.rstrip().split())
        
        if counter == 0:
            data[data_comprehension[counter]] = int(data_list[counter].pop())
        else: 
            data[data_comprehension[counter]] = data_list[counter]
        #moving to next
        counter += 1
    
    for items in range(1, len(data)):
        for values in range(len(data[data_comprehension[items]])):
            data[data_comprehension[items]][values] = data[data_comprehension[items]][values].split(",")
    file.close()

    return data

def fruit_implementation(fruit_type, data, final_list):
    """
upon recieving coordinates of fruit and a grid, puts the fruit in the grid
param fruit_type: the specific type of the fruit
param data: The coordinates of all fruit
param: final_list, a list grid of the field

    """
    #iterating through every coordinate given
    for elements in data[fruit_type]:
        #putting first letter of fruit in that array coord
        final_list[int(elements[1])][int(elements[0])] = fruit_type[0]

def grid_creation(data):
    """
Transforms the dictionary of data into an array (grid)
param data: a dictionary of data to be interpreted to an array
returns: an array of the data
    """
    #make a 2 dimensional list of string "0"s
    final_list = []
    for i in range(data["grid"]):
        start_list = []
        for j in range(data["grid"]):
            start_list.append("0")
        final_list.append(start_list)
    
    #putting the fruit into the list
    for elements in data_comprehension[1:]:
       fruit_implementation(elements, data, final_list)
    
    #transforming into arrays
    final_list = np.array(final_list)

    return final_list


def calculate_neighbours(grid, y, x):
    """
Finds the neighbouring fruits of an empty space on the grid at a specific coord
param grid: the grid of the field and fruit
param y: the y coordinate of the space
param x: the x coordinate of the space
returns: a list of all types of fruit around the spaces
    """
    
    #finding neighbouring fruits
    neighbours = []
    
    #looking in a 3x3 around the coordinate
    for i in range(y-1, y+2):
        for j in range(x-1, x+2):
            #dont look at elements that dont exist
            if i >= 0 and j >= 0 and i < len(grid) and j < len(grid[0]):
                #only add if its a fruit and a fruit we havent already seen
                if grid[i][j] != "0":
                    if grid[i][j] not in neighbours:
                        neighbours.append(grid[i][j])
    return neighbours

def which_growth(neighbours):
    #rules are JOLT over all, Fire over grass, grass over water, water over fire, all are mega
    """
Applies the rules of which fruit will spread to a list of neighbours and returns the dominant
param neighbours: a list of neighbouring fruits
returns: the right neighbour as a string of the letter
    """
    #megafruit is most dominant
    if "m" in neighbours or len(neighbours) == 4:
        return "m"
    
    #joltfruit is second dominant
    elif "j" in neighbours:
            return "j"
    
    #if theres only one fruit, return that
    elif len(neighbours) == 1:
        return(neighbours[0])
    
    #if theres three, no dominant
    elif len(neighbours) == 3:
        return "0"
    
    else:
        #the last possibilities
        if "f" in neighbours and "w" in neighbours:
            return "w"
        
        elif "f" in neighbours and "g" in neighbours:
            return "f"
        
        elif "g" in neighbours and "w" in neighbours:
            return "g"
        
        else:
            return "0"

def grid_spread(grid, year):
    """
Simulates the spread of the plants in the grid for one year and collection of fruit
param grid: The initial array grid of the field
param year: A boolean parameter if it's not the first year for fruit counting
returns: The next year array 
    """
    #next year will start as same array, altered
    next_gen = grid.copy()
    
    #iterate through every square
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            #check if its a tree or not
            if grid[i][j] == "0":
                #if its a tree, find its neighbours and what will grow there then set to next gen
                neighbours = calculate_neighbours(grid, i, j)
                next_gen[i][j] = which_growth(neighbours)
                neighbours = []
                
            else:
                if(year):
                    #if it is a fruit and not the initial year, add one to fruit collection
                    for elements in fruit_collected:
                        if grid[i][j] == elements[0]:
                            fruit_collected[elements] += 1
    return next_gen
files = ["pokefruit_pewterfarm", "pokefruit_celadonfarm", "pokefruit_palletfarm", "pokefruit_saffronfarm", "pokefruit_viridianfarm"]
file_name = files[4]

#making the starting grid
farm = grid_creation(import_data(file_name + ".txt"))

#counter is the year
counter = 0
#a dictionary to store fruit
fruit_collected = {"firefruit":0, "waterfruit":0, "grassfruit":0, "joltfruit":0, "megafruit":0}
last_year_fruit= {}

while True:
    #don't know how long we repeat
    #make a copy of fruit incase its the last year to see how much is made in last year
    most_recent_fruit = fruit_collected.copy()
    #genreate next year
    next_gen = grid_spread(farm, counter!=0)
    
    #check arrays if equal
    equal = farm == next_gen

    if equal.all():
        #if equal, find the last year of fruit and end loop
        for value in fruit_collected:
            last_year_fruit[value] = fruit_collected[value]-most_recent_fruit[value]
        break
    #add a year and reset farm
    counter += 1
    farm = next_gen


#printing everything
print("Fruit yield from final year.")
print("*********************************************")
for values in last_year_fruit:
    print(values[0].upper() + values[1:] + " : " + str(last_year_fruit[values]))
    
print("\n")

print("Fruit yield from ", str(counter), " years.")
print("*********************************************")
for values in fruit_collected:
    print(values[0].upper() + values[1:] + " : " + str(fruit_collected[values]))
