import PIL, common, os, math, random
from copy import deepcopy
from PIL import Image, ImageDraw, ImageFont

def getProvinceDict(): # Returns a dictionary with the province ID being the key, and a list of coordinates of every pixel in the province is returned.
    provinceDict = {}
    colorDict = {}
    provinceLines = open("./map/definition.csv", "r").readlines()
    for i in range(len(provinceLines)):
        temp = provinceLines[i].strip().split(";")
        r,g,b = int(temp[1]),int(temp[2]),int(temp[3])
        colorDict[(r,g,b)] = i
    
    provinceMap = Image.open("./map/provinces.bmp")
    imDat = provinceMap.load()
    height, width = provinceMap.size

    for h in range(height):
        for w in range(width):
            pR, pG, pB = imDat[h,w]
            if (pR,pG,pB) != (0,0,0):
                if colorDict[(pR,pG,pB)] not in provinceDict.keys():
                    provinceDict[colorDict[(pR,pG,pB)]] = []
                provinceDict[colorDict[(pR,pG,pB)]].append((h,w))
    provinceMap.close()
    return provinceDict

def getColor(nation):
    nationLines = open("./common/nations/" + nation + ".txt", "r").readlines()
    nationColors = nationLines[5].split(";")[0].strip()
    nationColors = nationColors.split(",")
    nationColors = (int(nationColors[0]),int(nationColors[1]),int(nationColors[2]))

    return nationColors

def drawNation(nation, h, w, pixelArray):
    print("Drawing nation: " + nation.name)
    
    nationPixels = nation.pixels
    lightBorders = []
    heavyBorders = []
    regions = nation.regions
    for r in range(len(regions)):
        pixels = []
        pxlCount = 0 
        region = regions[r]
        provs = region.provinces
        for p in range(len(provs)):
            prov = provs[p]
            pxls = prov.pixels
            for px in range(len(pxls)):
                pixel = pxls[px]
                pixels.append(pixel)
                pixelArray[pixel[0]][pixel[1]] = (0,0,r)
                pxlCount += 1
        print("Region " + region.name + ": " + str(pxlCount) + " pixels")
        
        # LIGHT BORDERS GEN
        for px in range(len(pixels)):
            pxl = pixels[px]
            check = True
            for j in range(-1,2):
                if check:
                    for k in range(-1,2):
                        if not (j == 0 and k == 0):
                            y = pxl[0]+j
                            x = pxl[1]+k
                            if x >= w:
                                x = 0
                            elif x < 0:
                                x = w-1

                            if not (y < 0 or y >= h):
                                if pixelArray[y][x] != (0,0,r):
                                    lightBorders.append((pxl[0],pxl[1]))
                                    break
                else:
                    break
    print("Done with region loop!")
    lightBorders = list(dict.fromkeys(lightBorders))

    for i in range(len(nationPixels)):
        pxl = nationPixels[i]
        pixelArray[pxl[0]][pxl[1]] = nation.color
    
    for px in range(len(nationPixels)):
        pxl = nationPixels[px]
        for j in range(-1,2):
            for k in range(-1,2):
                if not (j == 0 and k == 0):
                    y = pxl[0]+j
                    x = pxl[1]+k
                    if x >= w:
                        x = 0
                    elif x < 0:
                        x = w-1
                    
                    if not (y < 0 or y >= h):
                        if pixelArray[y][x] != (nation.color):
                            heavyBorders.append((pxl[0],pxl[1]))
    heavyBorders = list(dict.fromkeys(heavyBorders))
    
    print(str(len(lightBorders)) + " light borders.")
    print(str(len(heavyBorders)) + " heavy borders.")
    print("Nation " + nation.name + ": DONE!")

    return lightBorders, heavyBorders

def drawPolitical():
    print("DRAWING POLITICAL!")
    provMap = Image.open("./map/provinces.bmp")
    provDat = provMap.load()
    capIcon = Image.open("./map/capitalstar.png")
    cityIcon = Image.open("./map/citycircle.png")
    h,w = provMap.size
    pixelArray = []
    for _ in range(h):
        row = []
        for _ in range(w):
            row.append(()) 
        pixelArray.append(row)
    print("done writing empty array")
    for i in list(common.nationClassDict.keys()):
        nation = common.nationClassDict[i]
        color = nation.color
        lightBorderColor = (int(color[0]*.75),int(color[1]*.75),int(color[2]*.75))
        heavyBorderColor = (int(color[0]*.5),int(color[1]*.5),int(color[2]*.5))
        light, heavy = drawNation(nation,h,w,pixelArray)
        for i in nation.pixels:
            provDat[i[0],i[1]] = nation.color
        for i in light:
            provDat[i[0],i[1]] = lightBorderColor
        for i in heavy:
            provDat[i[0],i[1]] = heavyBorderColor
    
    for hx in range(h):
        for wx in range(w):
            if provDat[hx,wx] == (0,0,0):
                provDat[hx,wx] = (61,109,189)
    
    provMap.save("out.png")
    print("Done drawing political map!")

def getProvinceFromPixel(pixel, provinceDict):
    for key, value in provinceDict.items():
        if pixel in value:
            return key