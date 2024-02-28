#Anton Wegeström antwe841
#Christopher Wåtz chrwa634
#Uppgift5c

import cv2
import random
import math
import numpy as np
from cvlib import *
#from lab5_a import *
#from uppgift5b import *


def test_pixel_constraint():
    """ performs several test on the pixel constraint function """

    #the first element in then tuple is the in data and the second is result
    #test1: gives a pixel in range
    #test2 and 3: gives a pixel on the edge of the range
    #test4: an extreme case
    test_data = (((101, 101, 101), 1),
                 ((100, 100, 100), 0),
                 ((102, 102, 102), 0),
                 ((100000, 100000, 100000), 0))

    #test if the variabel is a function
    test_function = pixel_constraint(100, 102, 100, 102, 100, 102)
    assert(callable(test_function) == True)

    #test if the given a specific data gives the expected result
    for test in test_data:
        assert test_function(test[0]) == test[1]


def test_generator_from_image():
    """Tests generator_from_image"""

    #the first element in then tuple is the in data and the second is result
    #Does the index from 0 to 2, which is all the pixel in the generator
    #next line checks if using negative index also works
    test_data = ((0, (0,0,0)), (1, (0,128,255)), (2, (255,0,128)),
                (-1,(255,0,128)), (-2,(0,128,255)), (-3,(0,0,0)))

    #test if the variabel is a function
    test_function = generator_from_image([(0,0,0), (0,128,255), (255,0,128)])
    assert(callable(test_function) == True)

    #test if the given a specific data gives the expected result
    for test in test_data:
        assert test_function(test[0]) == test[1]


def test_combine_images():
    """Test the combine_images function"""

    #the first element in then tuple is the in data and the second is result
    #gives a picture like list which consist of three pixels
    test_data_1 = (([(1,1,226),(23,24,224),(55,65,227)],
                    [(0,0,0),(1,1,1),(0,0,0)]),
                   ([(34,24,224),(54,23,226),(5,98,230)],
                    [(1,1,1),(0,0,0),(0,0,0)]))

    def generator1(index):
        return(0, 0, 0)

    def generator2(index):
        return(1, 1, 1)

    condition_1 = pixel_constraint(0, 255, 0, 255, 225, 255)

    for test in test_data_1:
        assert combine_images(test[0], condition_1, generator1, generator2) == test[1]

    print("combine_images passed all the tests!")


def generator_from_image(orig_list):
    """Converts an image in list form to a function returning the
        color of a given pixel."""
    def gen_func(pixel):
        """Returns the rgb value of a pixel."""
        try:
            return orig_list[pixel]
        except IndexError:
            raise IndexError("Generator from Image: That pixel does not exist")

    return gen_func


def pixel_constraint(hlow, hhigh, slow, shigh, vlow, vhigh):
    """Returns a function that checks if a given pixel is range of given hsv
    parameters."""
    def pixel_checker(pixel):
        """Checks if a given pixel is in the correct range of saturation, hue
        and value."""
        if len(pixel) != 3:
            raise IndexError("Pixel constraint: The given tuple " +\
            "could not be interperted as a pixel please input tuples with"
            " atleast 3 elements")
        if isinstance(pixel[0], str) or \
           isinstance(pixel[1], str) or \
           isinstance(pixel[2], str):
           raise TypeError("Pixel Constraint: The given tuple " +
           "had one or more element which were not an interger or float")

        h = pixel[0]
        s = pixel[1]
        v = pixel[2]

        if  hlow < h and h < hhigh\
        and slow < s and s < shigh\
        and vlow < v and v < vhigh:
            return 1

        else:
            return 0

    return pixel_checker


def combine_images(hsv_list, condition, generator1, generator2):
    """Combines two images"""
    try:
        mask = 0
        mask = list(map(condition, hsv_list))
        final_image = []


        for i in range(len(hsv_list)):
            pixel_weight = mask[i]
            pixel1 = generator1(i)
            pixel2 = generator2(i)
            hue = pixel1[0] * pixel_weight + pixel2[0] * (1 - pixel_weight)
            saturation = pixel1[1] * pixel_weight + pixel2[1] * (1 - pixel_weight)
            value = pixel1[2] * pixel_weight + pixel2[2] * (1 - pixel_weight)
            final_image.append((hue, saturation, value))

        return final_image

    except IndexError:
        raise

    except TypeError:
        raise


def test_combine_images2():
    """Tests combine_images"""
    plane_img = cv2.imread("plane.jpg")
    condition = pixel_constraint(100, 150, 50, 200, 100, 255)

    hsv_list = cvimg_to_list(cv2.cvtColor(plane_img, cv2.COLOR_BGR2HSV))
    plane_img_list = cvimg_to_list(plane_img)

    def generator1(index):
        val = random.random() * 255 if random.random() > 0.99 else 0
        return (val, val, val)

    generator2 = generator_from_image(plane_img_list)

    result = combine_images([(0,0,1),(0,0,'a')], condition, generator1, generator2)

    print(result)