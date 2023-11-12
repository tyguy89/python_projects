import cv2 as cv
import numpy as np
import sys, os

sys.path.append(os.path.dirname(__file__))


def find_colour_in_image(img):
    new_array = np.zeros((len(img), len(img[0]), 3), np.uint8, 'C')
    counter = [0, 0]
    for i in range(0, len(img)):
        for j in range(0, int(len(img[i]))):

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
            elif r >= g and r >= b:
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

def extract_colours_in_image(path):
    img = cv.imread(path)
    
    #cv.imshow("Display Window", img)
    return find_colour_in_image(img)

def main():

    colour_object = extract_colours_in_image("python_projects/DivingVisualTracker/image_analysis/image0 (3).jpeg")
    cv.imshow("img", colour_object)

    cv.waitKey(0)
    #cv.destroyAllWindows()
main()