import hashlib

# example matrix
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# apply SHA-256 hash function to each row of the matrix
for row in matrix:
    # concatenate elements of the row into a single string
    row_str = ''.join(str(x) for x in row)
    # apply SHA-256 to the string and print the resulting hash value
    hash_value = hashlib.sha256(row_str.encode()).hexdigest()
    print(int(hash_value[:8], 16))
