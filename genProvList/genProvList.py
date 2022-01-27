## Generate a province list based on an image with the colors, assumedly a copy of the provinces wanted to add.
import PIL
from PIL import Image

provinceMap = Image.open("./genProvList/provinces.bmp")
mapData = provinceMap.load()
height, width = provinceMap.size

colors = []

provinceMap = Image.open("./genProvList/provinces.bmp")
mapData = provinceMap.load()
height, width = provinceMap.size
print("Processing image...")
for l1 in range(height):
    for l2 in range(width):
        r,g,b = mapData[l1,l2]
        if not (r == 0 and g == 0 and b == 0):
            if not [r,g,b] in colors:
                colors.append([r,g,b])
                print(r,g,b)

output = open("./genProvList/output.txt", "w")
outText = ""

for i in colors:
    text = str(i[0]) + ";" + str(i[1]) + ";" + str(i[2])
    provinceLines = open("./map/definition.csv").readlines()
    for i in range(len(provinceLines)):
        if text in provinceLines[i]:
            outText += provinceLines[i].split(";")[0].strip() + ","
            print(text)

output.write(outText)
