import numpy as np
from numpy.fft import fft
from numpy.polynomial import polynomial as P


def keygen(n, q, sigma):
    # Generate random polynomial f(x) of degree n-1
    f = np.random.normal(0, sigma, n)

    # Compute the secret key s by taking the FFT of f(x)
    s = np.round(q * fft(f).real) % q

    # Generate the public key by evaluating f(x) at n points
    # generate random n numbers from {0, 1, ..., q-1}
    A = np.random.randint(0, q, n)
    # generate n small error terms from Gaussian distribution
    e = np.random.normal(0, sigma, n)
    t = np.round(q * np.multiply(f, A) + e) % q

    return (A, t), s


def encrypt_block(block, public_key, q, sigma):
    n = len(block)
    k = len(public_key)
    m = np.array([0] * k)

    # Generate error terms
    error_terms = np.random.normal(scale=sigma, size=k)
    error_terms = [int(round(x)) for x in error_terms]

    # Compute the polynomial
    polynomial = P.polyadd(block, error_terms)

    # Compute the syndrome
    syndrome = [0] * n
    for i in range(n):
        for j in range(k):
            syndrome[i] += public_key[j][i] * error_terms[j]
        syndrome[i] = (-syndrome[i]) % q

    # Add the syndrome to the polynomial
    polynomial = P.polyadd(polynomial, syndrome)

    # Map the polynomial to a vector
    v = np.array([0] * n)
    for i in range(n):
        v[i] = polynomial[n-1-i] % q

    # Return the ciphertext
    return (v, m)


# n = 256
# q = 3329
# sigma = 2.0

# # Generate a symmetric key using a cryptographically secure random number generator
# symmetric_key = generate_symmetric_key()

# # Encrypt the message using a symmetric-key encryption algorithm like AES
# message = b"Hello, World!"
# encrypted_message = encrypt_message(message, symmetric_key)

# # Pad the encrypted message to a multiple of the Kyber block size
# padded_message = pad_message(encrypted_message, n)

# # Divide the padded message into blocks of size equal to the Kyber block size
# message_blocks = divide_into_blocks(padded_message, n)

# # Encrypt each block using the Kyber public key to obtain a ciphertext block
# ciphertext_blocks = []
# for block in message_blocks:
#     ciphertext_block = encrypt_block(block, public_key, q, sigma)
#     ciphertext_blocks.append(ciphertext_block)

# # Concatenate the ciphertext blocks to obtain the full ciphertext
# ciphertext = concatenate_blocks(ciphertext_blocks)

# print("Ciphertext: ", ciphertext)
