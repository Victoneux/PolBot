import os

def getRegions(nation):
    nationLines = open("./common/nations/" + nation + ".txt", "r").readlines()
    regions = (nationLines[2].split(";")[0]).split(",")
    for i in range(len(regions)):
        regions[i] = regions[i].strip()
    return regions

def getProvinces(nation):
    regions = getRegions(nation)
    provinces = []

    for i in range(len(regions)):
        line = (open("./common/states/" + regions[i] + ".txt", "r").readlines())[1]
        line = line.split(";")[0].strip()
        p = line.split(",")
        for i in p:
            provinces.append(i)
    
    return provinces

