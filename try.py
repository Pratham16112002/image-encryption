from PIL import Image
from numpy import array
import numpy as np
import key
import analysis
import random
img = Image.open('Lena.png')

ar = array(img)
height, width = ar.shape
random_float = random.uniform(0, 1)
x = 0.4+(random_float/5)
shuffled = np.zeros((512, 512), dtype=int)

cube = 512


def shuffle(matrix, height=None, width=None):
    if height is None and width is None:
        height, width = matrix.shape
    keys = key.coordinate_generator(height, width)
    final = np.full(height*width, -1, dtype=int)
    keys = keys.flatten()
    matrix = matrix.flatten()
    for i in range(len(keys)):
        final[i] = matrix[keys[i]]
    final = np.reshape(final, (height, width))
    return final


def shuffler(s):
    for i in range(0, 512, cube):
        for j in range(0, 512, cube):
            print(i, j)
            submatrix = s[i:i+cube, j:j+cube]
            changes = shuffle(submatrix, cube, cube)
            s[i:i+cube, j:j+cube] = changes
    return s


shuffled = shuffler(ar)

k = Image.fromarray(shuffled.astype(np.uint8))
k.save('./pics/chaotic{}x{}shuffle.png'.format(cube, cube))
