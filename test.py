from PIL import Image
import numpy as np
Image.MAX_IMAGE_PIXELS = None

thing = Image.open("./map/inputs/map.png").convert("RGB")
ar = np.array(thing)

f = np.dot(ar.astype(np.uint32),[1,256,65536])



where = np.where(f == 12498090)

coords = list(zip(where[0],where[1]))

print(where[0])

r = 170
g = 180
b = 190

bgr = (b << 16) + (g << 8) + (r << 0)

print(bgr)