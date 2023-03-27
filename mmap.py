import numpy as np
import random
import math
random_float = random.uniform(0, 1)
x = 0.4+(random_float/5)
p = random.uniform(0.25, 0.5)
print(x)


def next(x, p):
    if x <= 0.5 and x >= 0:
        xn = (x/p)*(2-(x/p))
    if x <= 1 and x > 0.5:
        xn = ((1-x)/p)*(2-((1-x)/p))
    pn = 0.25 + ((p+x) % 0.25)
    return xn, pn


z = np.empty((10, 10), dtype=int)
sum = 0
for i in range(10):
    for j in range(10):
        x, p = next(x, p)
        z[i, j] = math.trunc(x*256)
        sum += z[i, j]

print(x)
# Define the tent map function


def tent_map(x, p):
    if x < p:
        return x/p
    else:
        return (1-x)/(1-p)

# Define the S-box generation function


def generate_sbox(Spx, N, M):
    # Initialize the list Sn with values from 0 to 255
    Sn = list(range(256))
    # Initialize the empty list Sb
    Sb = []
    # Calculate the value of Spx, which is the sum of all pixels of the plain-image
    Spx = Spx
    # Drop the first 10^3 recurrence values
    # p = 0.721
    random_float = random.uniform(0, 1)
    x = 0.4+(random_float/5)
    x = (x+(Spx/(3 * 255 * N * M)) % 1)
    for i in range(10**3):
        x, p = next(x, p)
    # Generate the permutation using the Fisher-Yates algorithm
    while len(Sn) > 0:
        x, p = next(x, p)
        index = math.floor(x * len(Sn))
        Sb.append(Sn[index])
        del Sn[index]
    # Return the generated S-box
    return np.array(Sb).reshape(16, 16)


print(generate_sbox(sum, 10, 10))
