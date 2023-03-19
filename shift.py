from PIL import Image
from numpy import array
import numpy as np
import key
import analysis
import random

# Loading the image
img = Image.open('Lena.png')
# making an array of the original image
original_image_array = array(img)
height, width = original_image_array.shape

# Creating k1 and k2 the inital conditions for latin square
k1, x = key.coordinate_generator(1, 1024)
k2, x = key.coordinate_generator(1, 1024, x)
# Crearting the keyt to xor
key3 = key.key_gen(1024, 1024, x)

# Creating the latin square using left shift and right shift
key1 = np.empty((0, 1024), dtype=int)
key2 = np.empty((0, 1024), dtype=int)
# Initialize the final image
final_img = np.zeros((1024, 1024), dtype=np.uint8)
padded_image = np.zeros((1024, 1024), dtype=np.uint8)
padded_image[:512, :512] = original_image_array


def key1_generator(key1, k1):
    for i in range(1024):
        shifted_arr = np.roll(k1, i, axis=1)
        key1 = np.vstack((key1, shifted_arr))
    return key1


def key2_generator(key2, k2):
    for i in range(1024):
        shifted_arr = np.roll(k2, i, axis=1)
        key2 = np.vstack((key2, shifted_arr))
    return key2


key1 = key1_generator(key1, k1)
key2 = key2_generator(key2, k2)


def chaotic_shuffle(final_img, key1, key2, key3):
    # Chaotic shuffle and xor the final key
    for i in range(1024):
        for j in range(1024):
            if (key1[i, j] < 512) and (key2[i, j] < 512):
                print(key1[i, j], key2[i, j])
                final_img[i, j] = original_image_array[key1[i, j], key2[i, j]]
    final_img = key.keyxor(final_img, key3)
    return final_img


final_img = chaotic_shuffle(final_img, key1, key2, key3)


# analysis
print("CC: ", analysis.correlation_coefficient(padded_image, final_img))
img2 = np.copy(original_image_array)
x = random.randint(0, 255)
y = random.randint(0, 255)
img2[x][y] = random.randint(0, 255)
img2 = chaotic_shuffle(img2, key1, key2, key3)
analysis.histogram(original_image_array, final_img)
npcr, uaci = analysis.NPCR_UACI_worker(original_image_array, img2)
print("npcr: ", npcr, "%\tUaci: ", uaci, "%")
print("Entropy", analysis.entropy(final_img))

k = Image.fromarray(final_img)
k.save('./pics/final1903.png')
