import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

the_map = Image.open("./map/inputs/map.png").convert('RGB')
map_data = the_map.load()
map_width, map_height = the_map.size
np_array = np.array(the_map)
np_dot = np.dot(np_array.astype(np.uint32),[1,256,65536])

unique, indices = np.unique(np_array, return_index=True)
print(unique)

print(np_array[indices])