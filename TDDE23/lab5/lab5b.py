import cv2
import random
import math
import numpy as np
from cvlib import *
from lab5a import *



#5b1
def pixel_constraint(hlow, hhigh, slow, shigh, vlow, vhigh):
    """Returns a function that checks if a given pixel is range of given hsv
    parameters."""
    def pixel_checker(pixel):
        """Checks if a given pixel is in the correct range of saturation, hue
        and value."""

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
        return orig_list[pixel]
    return index_pixel


#5b3
def combine_images(hsv_list, condition, generator1, generator2):
    """
    Combines two images by creating a mask with numbers between 0 and 1 or a mask with numbers 0 or 1 
    depending on what condition is called, returns a list containing the manipulated pixels
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
    
#_____________________________________________________________TESTS__________________________________________________________________
def test1():
    hsv_plane = cv2.cvtColor(cv2.imread("plane.jpg"), cv2.COLOR_BGR2HSV)
    plane_list = cvimg_to_list(hsv_plane)

    is_sky = pixel_constraint(100, 150, 50, 200, 100, 255)
    sky_pixels = list(map(lambda x: x * 255, map(is_sky, plane_list)))

    cv2.imshow('sky', greyscale_list_to_cvimg(sky_pixels, hsv_plane.shape[0], hsv_plane.shape[1]))
    cv2.waitKey(0)

def test2():
    orig_img = cv2.imread("plane.jpg")
    orig_list = cvimg_to_list(orig_img)

    generator = generator_from_image(orig_list)

    new_list = [generator(i) for i in range(len(orig_list))]

    cv2.imshow('new', rgblist_to_cvimg(new_list, orig_img.shape[0], orig_img.shape[1]))
    cv2.waitKey(0) 
       
def test3():
    # Lä?s in en bild
    plane_img = cv2.imread("plane.jpg")

    # Skapa ett filter som identifierar himlen
    condition = pixel_constraint(100, 150, 50, 200, 100, 255)

    # Omvandla originalbilden till en lista med HSV-fä?rger
    hsv_list = cvimg_to_list(cv2.cvtColor(plane_img, cv2.COLOR_BGR2HSV))
    plane_img_list = cvimg_to_list(plane_img)

    # Skapa en generator som gö?r en stjä?rnhimmel
    def generator1(index):
        val = random.random() * 255 if random.random() > 0.99 else 0
        return (val, val, val)

    # Skapa en generator fö?r den inlä?sta bilden
    generator2 = generator_from_image(plane_img_list)

    # Kombinera de två? bilderna till en, alltså? anvä?nd himmelsfiltret som mask
    result = combine_images(hsv_list, condition, generator1, generator2)

        # Omvandla resultatet till en riktig bild och visa upp den
    new_img = rgblist_to_cvimg(result, plane_img.shape[0], plane_img.shape[1])
    cv2.imshow('Final image', new_img)
    cv2.waitKey(0)

def test4():
    plane_img = cv2.imread("plane.jpg")
    flower_img = cv2.imread("flowers.jpg")
    gradient_img = cv2.imread("gradient.jpg")


    hsv_list = cvimg_to_list(cv2.cvtColor(gradient_img, cv2.COLOR_BGR2HSV))
    plane_img_list = cvimg_to_list(plane_img)
    flower_img_list = cvimg_to_list(flower_img)

    generator1 = generator_from_image(flower_img_list)
    generator2 = generator_from_image(plane_img_list)

    result = combine_images(hsv_list, gradient_condition, generator1, generator2)

    new_img = rgblist_to_cvimg(result, plane_img.shape[0], plane_img.shape[1])
    cv2.imshow('Final image', new_img)
    cv2.waitKey(0)





