import cv2
import numpy as np
import math
from cvlib import *
#5a1
def cvimg_to_list(image):
    """
    Recieves a image and returns a list of tuples containing
    b,g,r colors for each pixel
    """ 

    w = image.shape[0]
    h = image.shape[1]
    #list builder that returns all pixels as tuples in a image
    new_list = []
    for x in range (w):
       for y in range (h):
           pixel = image[x,y]
           b = pixel[0]
           g = pixel[1]
           r = pixel[2]
           new_list.append((b,g,r))
    return new_list

#5a2
def gaussian_blur(x,y):

    """
    Calculates negativ gaussian blur for x,y cordinates if
    x and y != 0 then it returns 1.5
    """

    S = 4.5
    if x == 0 and y == 0:
        return 1.5
    else:
        expo  = -((x**2)+(y**2))/(2*S**2)
        return -(1/(2*math.pi*S**2))*math.e**expo


def unsharp_mask(n):

    """
    Recieves a value for n, loops trough all combinations for x and y and stores
    calculations in a list that is returned
    """

    #List builder that returns all x and y values
    minus = -(n//2)
    lista_n = [i + 1 for i in range((minus -1),(n + minus -1))]


    minus = lista_n[0]
    plus = lista_n[-1]

    #List builder that returns all calculations of the gaussian_blur funciton by looping 
    lista_a = [[gaussian_blur(y,x) for x in range(minus,plus+1)] for y in range \
    (minus,plus+1)]

    return lista_a

print(unsharp_mask(3))