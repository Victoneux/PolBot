import PIL, nations
from PIL import Image
def getColors(nation):
    provinces = nations.getProvinces(nation)
    provinceLines = open("./map/definition.csv", "r").readlines()
    colors = []

    for i in range(len(provinces)):
        province = int(provinces[i].strip())
        if provinceLines[province].startswith(str(provinces[i])):
            line = provinceLines[province]
            line = line.split(";")
            r,g,b = line[1],line[2],line[3]
            colors.append([r,g,b.strip()])
    
    nationLines = open("./common/nations/" + nation + ".txt", "r").readlines()
    nationColors = nationLines[5].split(";")[0].strip()
    nationColors = nationColors.split(",")
    for i in range(len(nationColors)):
        nationColors[i] = int(nationColors[i].strip())

    return colors, tuple(nationColors)

def drawNation(nation):
    provinceMap = Image.open("./map/provinces.bmp")
    mapData = provinceMap.load()
    height, width = provinceMap.size
    borderColor = tuple([50,50,50])
    provColors, nationColor = getColors(nation)
    print("Processing image...")
    for l1 in range(height):
        for l2 in range(width):
            r,g,b = mapData[l1,l2]
            if not (r == 0 and g == 0 and b == 0):
                if [str(r),str(g),str(b)] in provColors:
                    mapData[l1,l2] = nationColor
    
    for l1 in range(height):
        for l2 in range(width):
            borderPixel = False
            if mapData[l1,l2] == nationColor:
                try:
                    if mapData[l1+1,l2] != nationColor:
                        borderPixel = True
                except:
                    pass
                try:
                    if mapData[l1+1,l2+1] != nationColor:
                        borderPixel = True
                except:
                    pass
                try:
                    if mapData[l1+1,l2-1] != nationColor:
                        borderPixel = True
                except:
                    pass
                try:
                    if mapData[l1,l2-1] != nationColor:
                        borderPixel = True
                except:
                    pass
                try:
                    if mapData[l1,l2+1] != nationColor:
                        borderPixel = True
                except:
                    pass
                try:
                    if mapData[l1-1,l2] != nationColor:
                        borderPixel = True
                except:
                    pass
                try:
                    if mapData[l1-1,l2-1] != nationColor:
                        borderPixel = True
                except:
                    pass
                try:
                    if mapData[l1-1,l2+1] != nationColor:
                        borderPixel = True
                except:
                    pass

                if borderPixel == True:
                    mapData[l1,l2] = borderColor

    provinceMap.save('new.bmp')


            
            

