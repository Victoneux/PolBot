num = (180 << 16) + (170 << 8) + (160 << 0)

print(num)

g = num >> 16
num = num - (g << 16)
b = num >> 8
num = num - (b << 8)

print(g)
print(b)
print(num)