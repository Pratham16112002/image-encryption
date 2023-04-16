from PIL import Image
from numpy import array
import numpy as np
import key
import analysis
import math
# Loading the image
img = Image.open('Lena.png')
# making an array of the original image
original_image_array = array(img)
height, width = original_image_array.shape


# Initialize the final image
final_img = np.full((height, width), -1, dtype=np.uint8)
# padded_image = np.zeros((1024, 1024), dtype=np.uint8)


sum = key.pxsum(original_image_array)
sbox, initialx, initialp, x, p = key.sbox(sum, height, width, 256)
# fsbox = key.fsbox(sbox)


def dnaencoding(matrix, x, p, mkey=key.mkey_gen(512, 512)):
    height, width = matrix.shape
    for _ in range(10**3):
        x, p = key.mmap(x, p)
    for i in range(height):
        for j in range(width):
            x, p = key.mmap(x, p)
            rule = math.floor(x*8)
            value = key.int_binary(matrix[i, j])
            key_value = key.int_binary(mkey[i, j])
            pairs = [value[i:i+2] for i in range(0, len(value), 2)]
            key_pairs = [key_value[i:i+2] for i in range(0, len(key_value), 2)]
            modified_pairs = [key.dnavalues(
                rule, pair) for pair in pairs]
            modified_key_pairs = [key.dnavalues(
                rule, pair) for pair in key_pairs]
            final_pairs = [key.dnaxor(
                modified_pairs[i], modified_key_pairs[i]) for i in range(4)]
            final_pairs = [key.dnavalues(
                rule, _, pair) for pair in final_pairs]
            final_value = ''.join(final_pairs)
            matrix[i, j] = key.binary_int(final_value)
    return matrix


def findshifted(sbox, x, prevshift, pixel):
    shifts = ((math.floor(x*256))+prevshift) % 256
    result = np.roll(sbox, shifts)
    return result[pixel], shifts, result


def finddeshifted(sbox, x, prevshift, pixel):
    shifts = ((math.floor(x*256))+prevshift) % 256
    result = np.roll(sbox, shifts)
    s = list(result)
    res = s.index(pixel)
    return res, shifts, result


def sub(matrix, sbox, x, p, final_img):
    print("x", x)
    prevshift = 0
    for _ in range(pow(10, 3)):
        x, p = key.mmap(x, p)
    print(x)
    height, width = matrix.shape
    bi, bj = 0, 0
    ei, ej = 511, 511
    for i in range(height):
        for j in range(width):
            x, p = key.mmap(x, p)
            px, prevshift, sbox = findshifted(
                sbox, x, prevshift, matrix[i, j])
            if (x <= 0.5):
                final_img[bi, bj] = px
                bj += 1
                if (bj >= 512):
                    bj = 0
                    bi += 1
            if (x > 0.5):
                final_img[ei, ej] = px
                ej -= 1
                if (ej < 0):
                    ej = 511
                    ei -= 1
    return final_img


def decryption(matrix, sbox, x, p):
    print("x", x)
    height, width = matrix.shape
    reverse = np.full((height, width), -1, dtype=np.uint8)
    prevshift = 0
    for _ in range(pow(10, 3)):
        x, p = key.mmap(x, p)
    print(x)
    height, width = matrix.shape
    bi, bj = 0, 0
    ei, ej = 511, 511
    for i in range(height):
        for j in range(width):
            x, p = key.mmap(x, p)

            if (x <= 0.5):
                px, prevshift, sbox, = finddeshifted(
                    sbox, x, prevshift, matrix[bi, bj])
                reverse[i, j] = px
                bj += 1
                if (bj >= 512):
                    bj = 0
                    bi += 1
            if (x > 0.5):
                px, prevshift, sbox = finddeshifted(
                    sbox, x, prevshift, matrix[ei, ej])
                reverse[i, j] = px
                ej -= 1
                if (ej < 0):
                    ej = 511
                    ei -= 1
    return reverse


# dnaencoded = dnaencoding(original_image_array, x, p)
# final_img = sub(dnaencoded, sbox, x, p, final_img)
final_img = sub(original_image_array, sbox, x, p, final_img)
k = Image.fromarray(final_img)
k.save('./pics/final1404.png')

img2 = np.copy(original_image_array)
img2[0][0] = 150
lk = Image.fromarray(img2)
lk.save("./pics/img2.png")
final_img2 = np.zeros((512, 512), dtype=np.uint8)
final_img2 = sub(img2, sbox, x, p, final_img2)
print("CC: ", analysis.correlation_coefficient(original_image_array, final_img))
analysis.histogram(original_image_array, final_img)
npcr, uaci = analysis.NPCR_UACI_worker(final_img, final_img2)
print("npcr: ", npcr, "%\tUaci: ", uaci, "%")
print("Entropy encypted", analysis.entropy(final_img))
# print("DNA", analysis.entropy(dnaencoded))
print("Entropy original", analysis.entropy(original_image_array))
k2 = Image.fromarray(final_img2)
k2.save('./pics/final14042.png')


dec = decryption(final_img, sbox, x, p)
k3 = Image.fromarray(dec)
k3.save("./pics/decrypted1404.png")
