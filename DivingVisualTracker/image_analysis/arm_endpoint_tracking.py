#Tyler Boechler

import cv2 as cv
import numpy as np
import sys, os, time

sys.path.append(os.path)

index = {"black": np.array([0, 0, 0]), "white": np.array([255, 255, 255]), "red": np.array([0, 0, 255]), "green": np.array([0, 255, 0]), "blue": np.array([255, 0, 0]), "light blue": np.array([255, 157, 0]), "cyan": np.array([255, 255, 0]), "aqua": np.array([190, 255, 0]), "pink": np.array([255, 0, 190]), "magenta": np.array([255, 0, 255]), "purple": np.array([255, 0, 100]), "light green": np.array([0, 255, 150]), "yellow": np.array([0, 255, 255]), "orange": np.array([0, 165, 255])}
reversed_index = {}
for k in index:
        reversed_index[str(index[k])] = k

# print(reversed_index)


def find_pixel_neighbours(img, x, y):
    neighbours = []
    startx = -1 
    endx = 2
    starty = -1 
    endy = 2

    if x + 1 >= len(img):
        endx = 1

    if x == 0:
        startx = 0

    if y + 1 >= len(img[0]):
        endy = 1

    if y == 0:
        starty = 0

    if len(neighbours) == 0:
        for i in range(startx, endx):
            n1 = []
            for j in range(starty, endy):
                #if i == 0 and j == 0:
                   # continue
               # else:
                n1.append(img[x+i][y+j])
            #print(n1)
            neighbours.append(n1)
    return np.array(neighbours)

def find_colour_in_image(img):
    new_array = np.zeros((len(img), len(img[0]), 3), np.uint8, 'C')
    
    counter = [0, 0]
    np.set_printoptions(threshold=np. inf)
    for i in range(0, len(img)):
        for j in range(0, int(len(img[i]))):
            
                #print(img[i][j])


            local_pixel = img[i][j]
            r = local_pixel[2]
            g = local_pixel[1]
            b = local_pixel[0]

            new_r = 0 
            new_g = 0
            new_b = 0
            

            #WHITE DOMINANT COLOUR
            if r >= 175 and g >= 175 and b >= 175:
                new_r = 255
                new_g = 255
                new_b = 255
            
            #BLACK DOMINANT COLOUR
            elif r <= 50 and g <= 50 and b <= 50:
                new_r = 0
                new_g = 0
                new_b = 0
            
            #RED DOMINANT COLOUR
            elif r >= g and r > b:
                if g / r > 0.4:
                    if g/r > 0.75:
                        #YELLOW
                        new_g = 255
                    else:
                        #ORANGE
                        new_g = 165
                else:
                    if b / r > 0.55:
                        #MAGENTA
                        new_b = 255

                new_r = 255


            #GREEN DOMINANT COLOUR
            elif g >= r and g >= b:
                if r / g > 0.5:
                    if r/g > 0.75:
                        #YELLOW
                        new_r = 255
                    else:
                        #LIGHT GREEN
                        new_r = 150
                else:
                    if b / g > 0.6:
                        if b/g > 85:
                            #LIGHT BLUE
                            new_b = 255
                        else:
                            #AQUA 
                            new_b = 190
                            
                new_g = 255
            

            #BLUE DOMINANT COLOUR
            elif b >= r and b >= g:
                if g / b > 0.5:
                    if g/b > 0.75:
                        #CYAN
                        new_g = 255
                    else:
                        #LIGHT BLUE
                        new_g = 157
                    
                else:
                    if r / b > 0.3:
                        if r/b > 0.5:
                            if r/b > 0.75:
                                #MAGENTA
                                new_r = 255
                            else:
                                #PINK
                                new_r = 190
                        else:
                            #PURPLE
                            new_r = 100
                    
                        
                new_b = 255
            
            #UNKNOWN
            else:
                print(img[i][j])
                new_r = 0
                new_g = 0
                new_b = 0

            new_array[i][j] = np.array([new_b, new_g, new_r])
            counter[1] += 1
        counter[0] += 1

    print(counter)
    return new_array

def is_edge_of_shape(array):
    id = array[1][1]
    #print(id, "id")
    counter = 0
    for a in array:
        for each in a:
            if not np.array_equal(each, id):
                counter += 1
    
    return counter >= 3 and counter <= 5

def find_all_shape_edges(filtered_img):
    
    edge_colours = {}
    for k in index.keys():
        edge_colours[k] = []

    colour_edges = np.zeros((len(filtered_img), len(filtered_img[0]), 3), np.uint8, 'C')
    for i in range(len(filtered_img)):
        for j in range(len(filtered_img[i])):
            ninebynine = find_pixel_neighbours(filtered_img, i, j)
            if is_edge_of_shape(ninebynine):
                colour_edges[i][j] = filtered_img[i][j]
                edge_colours[reversed_index[str(filtered_img[i][j])]].append((i, j))

    return (colour_edges, edge_colours)

def extract_shapes_from_np(colour_data: dict, zoning_threshold_x: int, zoning_threshold_y: int): 
    def find_zone(vertex: tuple, zones: dict):
        v_count = len(zones.keys())
        
        for value in list(zones.keys()):
        
            if vertex[0] >= zones[value][0][0] - zoning_threshold_x and vertex[0] <= zones[value][0][1] + zoning_threshold_x and vertex[1] >= zones[value][0][2] - zoning_threshold_y and vertex[1] <= zones[value][0][3] + zoning_threshold_y:
                if vertex[0] < zones[value][0][0] or vertex[0] > zones[value][0][1] or vertex[1] < zones[value][0][2] or vertex[1] > zones[value][0][3]:
                    return_vals = [zones[value][0][0], zones[value][0][1], zones[value][0][2], zones[value][0][3]]
                    if vertex[0] < zones[value][0][0]:
                        return_vals[0] = vertex[0]
                    if vertex[0] > zones[value][0][1]:
                        return_vals[1] = vertex[0]
                    if vertex[1] < zones[value][0][2]:
                        return_vals[2] = vertex[1]
                    if vertex[1] > zones[value][0][3]:
                        return_vals[3] = vertex[1]
                    
                    return (value, (return_vals[0], return_vals[1], return_vals[2], return_vals[3]))
                else:
                    return(value, zones[value][0])
                
        print("ADDING NEW SHAPE", v_count)        
        return (v_count, (vertex[0]-zoning_threshold_x, vertex[0]+zoning_threshold_x, vertex[1]-zoning_threshold_y, vertex[1]+zoning_threshold_y))      

    zones = dict()

    for colour in colour_data.keys():
        zones[colour] = dict()
        for v in colour_data[colour]:
            if len(zones[colour].keys()) == 0:
                zones[colour][0] = ((v[0]-zoning_threshold_x, v[0]+zoning_threshold_x, v[1]-zoning_threshold_y, v[1]+zoning_threshold_y), [v])
            else:
                cur_zones = list(zones[colour].keys())

                v_zone = find_zone(v, zones[colour])

                if v_zone[0] not in cur_zones:
                    zones[colour][v_zone[0]] = (v_zone[1], [v])
                else:
                    #print(zones[colour][v_zone[0]][1])
                    zones[colour][v_zone[0]][1].append(v)
                    #print(zones[colour][v_zone[0]][1])
                    #print("---")
                    zones[colour][v_zone[0]] = (v_zone[1], zones[colour][v_zone[0]][1])

    return zones

def extract_nprgb_path_of_image(path):
    img = cv.imread(path)

    return img

def extract_background(img, colour_data):
    biggest = "white"
    for k in colour_data.keys():
        if len(colour_data[k]) > len(colour_data[biggest]):
            biggest = k
    
    for i in colour_data[biggest]:
        img[i[0]][i[1]] = np.array([0, 0, 0])
    
    return img

def extract_colour(img, colour_data, colour_to_remove):
    colour_edges = np.zeros((len(img), len(img[0]), 3), np.uint8, 'C')
    for v in colour_data[colour_to_remove]:
        colour_edges[v[0]][v[1]] = img[v[0]][v[1]]
    

    return colour_edges

def remove_colour(img, colour_data: dict, colour_to_delete):
    for i in colour_data[colour_to_delete]:
        img[i[0]][i[1]] = np.array([0, 0, 0])
    
    colour_data.pop(colour_to_delete)

    return img

def paint_blank_with_coords(colour_data, canvas, colour):
    color_lottery = [index["aqua"], index["red"], index["blue"], index["white"], index["yellow"], index["orange"], index["green"], index["magenta"], index["pink"], index["aqua"], index["red"], index["blue"], index["white"], index["yellow"], index["orange"], index["green"], index["magenta"]]
    color_lottery += color_lottery
    color_lottery += color_lottery
    color_lottery += color_lottery
    color_lottery += color_lottery
    color_lottery += color_lottery
    color_lottery += color_lottery
    color_lottery += color_lottery
    color_lottery += color_lottery

    for shape in range(len(colour_data)):

        for i in colour_data[shape]:
            canvas[i[0]][i[1]] = color_lottery[shape]

    return canvas

if __name__ == "__main__":

    start = time.time()
    colour_object = extract_nprgb_path_of_image("python_projects/DivingVisualTracker/image_analysis/IMG_8880.jpg")
    blank = np.zeros((len(colour_object), len(colour_object[0]), 3), np.uint8, 'C')

    filtered_image = find_colour_in_image(colour_object)
    edges_of_colours = find_all_shape_edges(filtered_image)
    focus_colour = "orange"
    single_colour = extract_shapes_from_np({focus_colour: edges_of_colours[1][focus_colour]}, 5, 5)
    #print(single_colour)
    print("Process time = " + str(time.time() - start))
    start = time.time()
    shape_list = []

    for i in single_colour[focus_colour].keys():
        shape_list.append(single_colour[focus_colour][i][1])

    blank = paint_blank_with_coords(shape_list, blank, focus_colour)
    cv.imshow("img", blank)
    print("Process time = " + str(time.time() - start))


    cv.waitKey(0)
    cv.destroyAllWindows()

