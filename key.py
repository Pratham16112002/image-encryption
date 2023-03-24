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
    R = 4
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


def henon_map(x, y, a=1.4, b=0.3):
    """Applies the Henon map to coordinates x, y with parameters a and b."""
    x_new = y + 1 - a * x**2
    y_new = b * x
    return x_new, y_new


def applyhenon(matrix, iterations):
    nrows, ncols = matrix.shape
    for _ in range(iterations):
        for i in range(nrows):
            for j in range(ncols):
                x, y = henon_map(i/nrows, j/ncols)
                new_i, new_j = int(x * nrows), int(y * ncols)
                if new_i >= nrows:
                    new_i = nrows - 1
                if new_j >= ncols:
                    new_j = ncols - 1
                matrix[i, j] = matrix[new_i, new_j]
    return matrix


def arnold(matrix, iteration):
    K = 5
    height, width = matrix.shape
    temp = np.empty((height, width), dtype=int)
    for i in range(iteration):
        for x in range(height):
            for y in range(height):
                x_new = (x + y) % height
                y_new = (K*x + y) % height
                temp[x, y] = matrix[x_new, y_new]
    return temp

