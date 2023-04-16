from PIL import Image
from numpy import array
import numpy as np
import key
import analysis
import random
import math
# Loading the image
# img = Image.open('Lena.png')
# making an array of the original image
original_image_array = aarr = np.full((5, 5), -1)
print(original_image_array)
height, width = original_image_array.shape

# dig = original_image_array.diagonal()
# main_diag = original_image_array.diagonal()

# for i in range(2*height-1):
#     if i < (height-1):
#         diag = original_image_array.diagonal(offset=(height-i-1))
#         print(diag, "\n")
#     if i == height:
#         print(main_diag)
#     if i > (height-1):
#         diag = original_image_array.diagonal(offset=height+i)
#         print(diag, "\n")

for i in range(1, 2*height):
    print(np.diag(original_image_array, k=height-i))
u, b = 0, -height+1
# print(np.diag(original_image_array, k=u))
# print(np.diag(original_image_array, k=b))

for i in range(height):
    for j in range(width):
        bottom_diagnols = []
        upper_diagnols = []
        
