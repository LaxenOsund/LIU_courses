from ast import Str
import cv2
import random
import math
import numpy as np
from cvlib import *

def run_tests():
    test_pixel_constraint()
    test_generator_from_image()
    test_combine_images()
    print("all tests passed")


def test_pixel_constraint():
    """ 
    Tests the functionaly of pixel_constraint to make sure we get expected
    outputs and returns True if no flaws were detected.
    """
    #tests usual inputs but also inputs wich are not tuples.
    test_inputs = (((255, 0, 255, 0, 100, 0), (100, 45, 60), 0)\
                , ((0, 10, 0, 10, 10, 30), (10, 10, 20), 1)\
                , ((0, 300, 50, 52, 0, 200), (220, 51, 50), 1)\
                , ((0, 255, 0, 255, 0, 255), "string", None)\
                , ("string", (33, 100, 200), None))
    
    for test in test_inputs:
        a = pixel_constraint(test[0][0], test[0][1], test[0][2],\
                             test[0][3], test[0][4], test[0][5])
        assert a(test[1]) == test[2]

def test_generator_from_image():
    """Tests generator_from_image"""

    test_inputs = ((((33, 22, 11), (230, 255, 100), (251, 2, 81)), 1, (230, 255, 100)), \
                  (((33, 0, 2), (23, 211, 130), (000, 000, 0)), 0, (33 ,0 , 2)), \
                  (((33, 33, 33), (23, 23, 23), (10, 10, 10)), 100, None))
    
    for test in test_inputs:
        a = generator_from_image(test[0])
        assert a(test[1]) == test[2]

def test_combine_images():
    """Tests the functionaly combine_images to make sure we get expected
    outputs and returns True if all tests are passed.
    First two tests assert that basic functionality is correct, third test tests
    two images of different sizes, and the fourth test tests invalid input type.
    """

    # input image list for every test case
    img_lsts = (((1, 1, 1), (85, 85, 85), (200, 200, 200)), \
                ((75, 101, 101), (256, 256, 256), (75, 101, 101)), \
                ((75, 101, 101), (256, 256, 256), (75, 101, 101)), \
                "not a pixel")

    #Maxat värde för hsv
    hsv1 = []
    hsv2 = []
    hsv3 = [(255,255,255),(255,255,255),(255,255,255)]

    condition = pixel_constraint(0,100,0,50,0,120)
    generator1 = generator_from_image([(125,123,100),(50,20,80),(110,130,60)])
    generator2 = generator_from_image([(75,23,200),(150,203,87),(10,30,60)])


    test_case1 = combine_images(hsv1, condition, generator1, generator2)
    assert test_case1 == [(125,123,100),(50,20,80),(110,130,60)]


    test_case2 = combine_images(hsv2, condition, generator1, generator2)
    assert test_case2 == [(75,23,200),(150,203,87),(110,130,60)]


    test_case3 = combine_images(hsv3, condition, generator1, generator2)
    assert test_case3 == [(75,23,200),(150,203,87),(10,30,60)]
                

#________________________________________________________________Code___________________________________________________________________

#5b1
def pixel_constraint(hlow, hhigh, slow, shigh, vlow, vhigh):
    """Returns a function that checks if a given pixel is range of given hsv
    parameters."""
    def pixel_checker(pixel):
        
            """Checks if a given pixel is in the correct range of saturation, hue
            and value."""
            if len(pixel) != 3:
                raise IndexError("Pixel constraint: The given tuple " +\
                "doesnt have exactly 3 elements")
            if isinstance(pixel[0], str) or \
                isinstance(pixel[1], str) or \
                isinstance(pixel[2], str):
                raise TypeError("Pixel Constraint: The given tuple " +
                "had one or more element which were a string")
            h = pixel[0]
            s = pixel[1]
            v = pixel[2]

            if hlow <= h and h <= hhigh and slow <= s and s <= shigh and vlow <= v \
            and v <= vhigh:
                return 1
            else:
                return 0
    return pixel_checker

#5b2
def generator_from_image(orig_list):
    """Converts an image in list form to a function returning the
        color of a given pixel."""
    def index_pixel(pixel):
        """Returns the rgb value of a pixel."""
        try:
            pix = orig_list[pixel]
        except IndexError:
            raise IndexError("generator_from_image failed to find pixel. \
                Pixel does not exist")
        return pix
    return index_pixel


#5b3
def combine_images(hsv_list, condition, generator1, generator2):
    """
    Combines two images by creating a mask with numbers between 
    0 and 1 or a mask with numbers 0 or 1 
    depending on what condition is called, returns a list containing 
    the manipulated pixels
    """
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


#5b4
def gradient_condition(pixel):
    """Returns a value between 0 and 1 representing how dark a pixel is"""
    return pixel[2]/255
    
run_tests()