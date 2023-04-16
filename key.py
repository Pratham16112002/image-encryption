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
            r = matrix[i]
            row_sum = np.sum(r, axis=0)
            for j in range(ncols):
                x, y = henon_map(i/row_sum, j/row_sum)
                print(x, y)
                # print(((x % 1) * nrows), ((y % 1) * nrows))
                new_i, new_j = int((x % 1) * nrows), int((y % 1) * ncols)
                # print(new_i, new_j)
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


def tent_map(x, p):
    if x < p:
        return x/p
    else:
        return (1-x)/(1-p)


def pxsum(matrix):
    sum = 0
    height, width = matrix.shape
    for i in range(height):
        for j in range(width):
            sum += matrix[i, j]
    return sum


def mmap(x=None, p=None):
    if x is None:
        x = random.uniform(0, 1)
    if p is None:
        p = random.uniform(0.25, 0.5)
    if x >= 0 and x <= 0.5:
        xn = (x/p)*(2-(x/p))
    if x > 0.5 and x <= 1:
        xn = ((1-x)/p)*(2-((1-x)/p))
    pn = 0.25 + ((p+x) % 0.25)
    return xn, pn


def sbox(sum, r, c, s, x=None, p=None):
    rangelist = list(range(s))
    sbox = []
    if x is None:
        x = random.uniform(0, 1)
    if p is None:
        p = random.uniform(0.25, 0.5)
    x = ((x+(sum/(255 * r * c))) % 1)
    initialx, initialp = x, p
    for _ in range(pow(10, 3)):
        x, p = mmap(x, p)
    while (len(rangelist) > 0):
        x, p = mmap(x, p)
        index = math.floor(x*len(rangelist))
        sbox.append(rangelist[index])
        del rangelist[index]
    return sbox, initialx, initialp, x, p


def fsbox(matrix):
    sbox = np.empty((0, 256), dtype=int)
    matrix = np.array(matrix)
    height = len(matrix)
    for i in range(height):
        shifted = np.roll(matrix, i)
        sbox = np.vstack((sbox, shifted))
    return sbox


def dnavalues(x, y, z=None):
    values = [["00", "11", "10", "01"],
              ["00", "11", "01", "10"],
              ["11", "00", "10", "01"],
              ["11", "00", "01", "10"],
              ["10", "01", "00", "11"],
              ["10", "01", "11", "00"],
              ["01", "10", "00", "11"],
              ["01", "10", "11", "00"],
              ]
    if z is not None:
        if z == "A":
            return values[x][0]
        elif z == "T":
            return values[x][1]
        elif z == "G":
            return values[x][2]
        elif z == "C":
            return values[x][3]
    else:
        i = values[x].index(str(y))
        if i == 0:
            return "A"
        elif i == 1:
            return "T"
        elif i == 2:
            return "G"
        elif i == 3:
            return "C"


def dnaxor(x, y):
    def getnum(z):
        if z == "A":
            return 0
        elif z == "T":
            return 1
        elif z == "G":
            return 2
        elif z == "C":
            return 3
    values = [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 1, 0], [3, 2, 1, 0]]
    z = values[getnum(x)][getnum(y)]
    if z == 0:
        return "A"
    elif z == 1:
        return "T"
    elif z == 2:
        return "G"
    elif z == 3:
        return "C"


def mkey_gen(r, c, x=None, p=None):
    key = np.zeros((r, c), dtype=int)
    for i in range(10**3):
        x, p = mmap(x, p)
    for i in range(0, r):
        for j in range(0, c):
            x, p = mmap(x, p)
            key[i][j] = math.floor(((x)*(256)))
    return key


def int_binary(x):
    return bin(x).replace("0b", "").zfill(8)


def binary_int(x):
    return int(x, 2)
