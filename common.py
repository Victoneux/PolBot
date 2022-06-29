import discord
import os, random, mapping, math, pickle
from smtplib import SMTPRecipientsRefused
from PIL import Image

def initialize():
    global regionDict, pixelDictRegions, regionClassDict, nationClassDict, ideaClassDict, mapWidth, mapHeight, map
    regionDict = mapping.getMapDict()
    map = Image.open("./map/map.bmp")
    mapWidth, mapHeight = map.size

    pixelDictRegions = {}
    for x in list(regionDict.keys()):
        pixels = regionDict[x]
        for px in pixels:
            pixelDictRegions[px] = x

    regionClassDict = {}
    readRegions()
    nationClassDict = {}
    readNations()
    ideaClassDict = {}
    readIdeologies()

    print("Initialized!")

def minimalInitialize():
    global pixelDictRegions
    regionDict = mapping.getMapict()
    pixelDictRegions = {}
    for x in list(regionDict.keys()):
        pixels = regionDict[x]
        for px in pixels:
            pixelDictRegions[px] = x

class region:
    def __init__(self, nation, name, longName, capital, autonomy, description):
        self.name = name
        self.nation = nation
        self.longName = longName
        self.capital = capital
        self.autonomy = autonomy
        self.description = description

        self.pixels = regionDict[f"{nation}/{name}"]
        self.area = calculateArea(self.pixels)

    def embed(self):
        theEmbed = discord.Embed(title=self.longName, color=int('%02x%02x%02x' % nationClassDict[self.nation].color, 16), description=self.description)
        theEmbed.add_field(name="area", value=f"{str(self.area)} km²")
        theEmbed.set_footer(text="©2022 VicCO. All Gay Rights Reserved.")
        return theEmbed

class nation:
    def __init__(self, regions, name, longName, color, capital, description, idea, history):
        self.regions = regions
        self.name = name
        self.longName = longName
        self.color = color
        self.capital = capital
        self.description = description
        self.ideology = int(idea)
        self.history = history

        self.pixels = []
        self.area = 0
        for i in regions:
            regPixels = i.pixels
            self.area += i.area
            for i in regPixels:
                self.pixels.append(i)
        self.area = round(self.area, 2)

    def toString(self):
        return "Nation " + self.longName + " has a landmass of " + str(int(self.area)) + " km^2"
    def embed(self):
        # theEmbed = discord.Embed(title=self.longName, color=int('%02x%02x%02x' % self.color, 16), description=self.description)
        # theEmbed.add_field(name="Area", value=(str(self.area) + " km²"))
        # theEmbed.add_field(name="History", value=self.history, inline=False)
        # theEmbed.set_footer(text="©2022 VicCO. All Gay Rights Reserved.")
        theEmbed = discord.Embed(title=self.longName, color=int('%02x%02x%02x' % self.color, 16), description = self.description)
        theEmbed.add_field(name="area", value = f"{str(self.area)} km²")
        theEmbed.add_field(name="History", value=self.history, inline=False)
        theEmbed.set_footer(text="©2022 VicCO. All Gay Rights Reserved.")
        return theEmbed

class ideology:
    def __init__(self, name, description):
        self.name = name
        self.description = description

def readRegions():
    files = []
    directories = os.listdir("./common/regions/")
    for directory in directories:
        things = os.listdir("./common/regions/" + directory)
        for thing in things:
            files.append(directory + "/" + thing)
    for f in files:
        lines = open("./common/regions/" + str(f), "r").readlines()
        name = f.split(".")[0].split("/")[-1]
        directory = f.split(".")[0].split("/")[0]
        nation = f.split(".")[0].split("/")[0]
        color = lines[0].split(";")[0].strip().split(",")
        color = (int(color[0].strip()),int(color[1].strip()),int(color[2].strip()))
        longName = lines[1].split(";")[0].strip()
        capital = int(lines[2].split(";")[0].strip())
        autonomy = int(lines[3].split(";")[0].strip())
        desc = lines[4].split(";")[0].strip()
        regionClassDict[f"{directory}/{name}"] = region(nation,name,longName,capital,autonomy,desc)

def readNations():
    files = []
    directories = os.listdir("./common/nations")
    for directory in directories:
        things = os.listdir("./common/nations/" + directory)
        for thing in things:
            files.append(directory + "/" + thing)
    for f in files:
        lines = open("./common/nations/" + str(f), "r").readlines()
        name = f.split(".")[0].split("/")[-1]
        longName = lines[0].split(";")[0].strip()
        shortName = lines[1].split(";")[0].strip()
        regions = os.listdir(f"common/regions/{name}/")
        regions2 = []
        for region in regions:
            region = region.split('.')[0]
            regions2.append(regionClassDict[f"{name}/{region}"])
        color = lines[2].split(";")[0].strip().split(",")
        color = (int(color[0].strip()),int(color[1].strip()),int(color[2].strip()))
        desc = lines[3].split(";")[0].strip()
        capital = int(lines[4].split(";")[0].strip())
        ideology = int(lines[5].split(";")[0].strip())
        history = lines[6].split(";")[0].strip()

        nationClassDict[name] = nation(regions2,shortName,longName,color,capital,desc,ideology,history)

def readIdeologies():
    files = os.listdir("./common/ideologies")
    for f in files:
        lines = open("./common/ideologies/" + str(f), "r").readlines()
        name = lines[0].split(";")[0].strip()
        desc = lines[1].split(";")[0].strip()
        thing = int(f.split(".")[0])
        ideaClassDict[thing] = ideology(name, desc)

def calculateArea(pixels):
    provinceMap = Image.open("./map/map.bmp")
    width, height = provinceMap.size
    provinceMap.close()

    radius = 6378
    def getAngle(h):
        max = height/2
        return (h/max)*90
    totArea = 0
    for x in range(len(pixels)):
        h = pixels[x][1]
        if h > height/2:
            h = height - h
        h = height/2 -h
        area = (math.sin(math.radians(getAngle(h)))*2*math.pi*radius*radius) - (math.sin(math.radians(getAngle(h-1)))*2*math.pi*radius*radius)
        area = area/width
        totArea += area
    return totArea

def getRegions(nation):
    nationLines = open("./common/nations/" + nation + ".txt", "r").readlines()
    regions = (nationLines[2].split(";")[0]).split(",")
    for i in range(len(regions)):
        regions[i] = regions[i].strip()
    return regions