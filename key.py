import random
import numpy as np
import math


def key_gen(r, c, x=None):
    """
    Generate logistic chaotic map used for key in range[0-255]
    Argumets:
        r : row of the 2d map required
        c : col of the 2d map required
        x :  initial value of x in logistic function
    Returns:
        matrix of logictic chaotic map
     """
    R = 3.99
    random_float = random.uniform(0, 1)
    if x is None:
        x = 0.4+(random_float/5)
    key = np.zeros((r, c))
    for i in range(1000):
        x = x*R*(1-x)
    for i in range(0, r):
        for j in range(0, c):
            x = x*R*(1-x)
            key[i][j] = round(((x)*(255)))
    return key


def keyxor(matrix, key):
    """
    Xor the image with the key
    Argumets:
        matrix : 2d numpy matrix , the image as a matrix
        key : the key generated from the chaotic function
    Returns:
        2d numpy array of the image after adding of the key
    """
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = int(matrix[i][j]) ^ int(key[i][j])

    return matrix


def coordinate_generator(r, c, x=None):
    """
    Generate logistic chaotic map used for key in range[0-255]
    Argumets:
        r : row of the 2d map required
        c : col of the 2d map required
        x :  initial value of x in logistic function
    Returns:
        matrix of logictic chaotic map
     """
    R = 4
    all = set()
    random_float = random.uniform(0, 1)
    if x is None:
        x = 0.4+(random_float/5)
    key = np.full((r, c), -1, dtype=int)
    for i in range(1000):
        x = x*R*(1-x)
    for i in range(0, r):
        for j in range(0, c):
            while (key[i, j] == -1):
                x = x*R*(1-x)
                if math.trunc(x*c*r) not in all:
                    key[i][j] = math.trunc(x*c*r)
                    all.add(key[i, j])
    return key, x


def henon(matrix):
    a = 1.4
    b = 0.3
    height, width = matrix.shape
    output_matrix = np.zeros((height, width))
    for i in range(height):
        for j in range(width):
            x_n = matrix[i][j]
            y_n = matrix[i][j]
            x_n1 = 1 - a * x_n**2 + y_n
            y_n1 = b * x_n
            output_matrix[i][j] = x_n1
    return output_matrix
