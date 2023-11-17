#Tyler Boechler

import cv2 as cv
import numpy as np
import sys, os

sys.path.append(os.path)

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
    np. set_printoptions(threshold=np. inf)
    for i in range(0, len(img)):
        for j in range(0, int(len(img[i]))):
            
                #print(img[i][j])


            local_pixel = img[i][j]
            r = local_pixel[0]
            g = local_pixel[1]
            b = local_pixel[2]

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
                        #PINK
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
                                #PINK
                                new_r = 255
                            else:
                                #MAGENTA
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

            new_array[i][j] = np.array([new_r, new_g, new_b])
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
    colour_edges = np.zeros((len(filtered_img), len(filtered_img[0]), 3), np.uint8, 'C')
    for i in range(len(filtered_img)):
        for j in range(len(filtered_img[i])):
            ninebynine = find_pixel_neighbours(filtered_img, i, j)
            if is_edge_of_shape(ninebynine):
                colour_edges[i][j] = filtered_img[i][j]

    return colour_edges
def extract_shapes_from_np(img, start_coord, range1, range2):
    #Extracts shapes from a given range and area on the np image
    #Square, Rectangle, Circle, Ellipse, Triangle
    assert start_coord[0] + range1 < len(img) and start_coord[1] + range2 < len(img[0]), "Out of bounds"


    
    #Ideas for extraction : 
    #Finding a background colour would make my life easier or sewing a giant green blanket
    # A shape flood fill algorithm
    # A shape perimeter / area detection with brute force analysis or simple neural network
    # Use filters on image to get it to a less colourful noise format
    # Rely heavily on markup of frames
    # Add extra parameters and logic in pixel creation for all pixels that have 3 neighbours of a different colour and then keep differnt colours as seperate objects 

def extract_nprgb_path_of_image(path):
    img = cv.imread(path)
    

    return img

def main():

    #index = {"red": [255, 0, 0], "green": [0, 255, 0], "blue": [0, 0, 255], "light blue": [0, 157, 255], "cyan": [0, 255, 255], "aqua": [0, 255, 190], "pink": [255, 0, 255], "magenta": [190, 0, 255], "purple": [100, 0, 255], "light green": [150, 255, 0], "yellow": [255, 255, 0], "orange": [255, 165, 0]}
    #reversed_index = {}
    #for k in index:
       # reversed_index[str(index[k])] = k
    

    colour_object = extract_nprgb_path_of_image("python_projects/DivingVisualTracker/image_analysis/image0 (4).jpeg")
    
    filtered_image = find_colour_in_image(colour_object)
    edges_of_colours = find_all_shape_edges(filtered_image)

    cv.imshow("img", edges_of_colours)


    cv.waitKey(0)
    cv.destroyAllWindows()
main()
