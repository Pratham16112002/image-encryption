
dec = decryption(final_img, sbox, x, p)
k3 = Image.fromarray(dec)
k3.save("./pics/decrypted.png")
print(original_image_array)
print(dec)
