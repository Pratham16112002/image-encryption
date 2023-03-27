, j = 10, 10
for _ in range(10):
    x, y = henon_map(i/256, j/256)
    i += 1
    j += 1
    print((int(x*256) % 256, int(y*256) % 256))
