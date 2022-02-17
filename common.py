import discord
import os, random, mapping, math, pickle
from smtplib import SMTPRecipientsRefused
from PIL import Image

def initialize():
    global provinceDict, pixelDictProvs, pxlDictRegions, provClassDict, regionClassDict, nationClassDict, defLines, provMapHeight, provMapWidth, provMap, provDat, adjacencies, adjNumbers
    provinceDict = mapping.getProvinceDict()
    defLines = open("./map/definition.csv", "r").readlines()
    provMap = Image.open("./map/provinces.bmp")
    provDat = provMap.load()
    provMapHeight, provMapWidth = provMap.size

    pixelDictProvs = {}
    for x in list(provinceDict.keys()):
        pixels = provinceDict[x]
        for px in pixels:
            pixelDictProvs[px] = x
    pxlDictRegions = {}

    provClassDict = {}
    readProvs()
    if os.path.exists("./map/adjacencies.txt"):
        with open ("./map/adjacencies.txt", "rb") as adjFile:
            adjacencies = pickle.load(adjFile)
        adjFile.close()
        adjNumbers = {}
        genAdjNumbers()

    regionClassDict = {}
    readRegions()
    nationClassDict = {}
    readNations()

    for r in regionClassDict.keys():
        provs = regionClassDict[r].provinces
        for p in provs:
            pxls = p.pixels
            for px in pxls:
                pxlDictRegions[px] = r

    print(pxlDictRegions[(725,2740)])

class building:
    def __init__(self, name, jobs, production, consumption, requiredInfra):
        self.name = name
        self.jobs = jobs
        self.production = production
        self.consumption = consumption
        self.requiredInfra = requiredInfra
    
    def toList(self):
        return [self.name, self.jobs, self.production, self.consumption, self.requiredInfra]

class population:
    def __init__(self, species, population, religions, ideologies, modifiers):
        ## Species: 0 - Reitak, 1 - Sajek, 2 - Akkar, 3 - Pengus, 4 - Humans
        ## Religions: 0 - Atheist, 1 - Catholic, 2 - Protestant, 3 - Alzimianist, 4 - Icinist, 5 - Munduist
        ## Ideologies: 0 - Pure Anarchy
        self.species = species
        self.population = population
        self.religions = religions
        self.ideologies = ideologies
        self.modifiers = modifiers
    
    def toList(self):
        return [self.species, self.population, self.religions, self.ideologies, self.modifiers]

class province:
    def __init__(self, num, populations, buildings):
        self.num = num
        self.name = getProvinceName(num)
        self.buildings = buildings
        self.populations = populations
        self.pixels = provinceDict[num]
        self.area = calculateArea(self.pixels)

class region:
    def __init__(self, provinces, name, longName, capital, autonomy, description, dmz):
        self.provinces = provinces
        self.name = name
        self.longName = longName
        self.capital = capital
        self.autonomy = autonomy
        self.description = description
        self.isDMZ = dmz

        self.pixels = []
        self.area = 0
        for i in provinces:
            provPixels = i.pixels
            self.area += i.area
            for i in provPixels:
                self.pixels.append(i)

class nation:
    def __init__(self, regions, name, longName, color, capital, description, idea):
        self.regions = regions
        self.name = name
        self.longName = longName
        self.color = color
        self.capital = capital
        self.description = description
        self.ideology = idea

        self.pixels = []
        self.area = 0
        for i in regions:
            regPixels = i.pixels
            self.area += i.area
            for i in regPixels:
                self.pixels.append(i)

    def toString(self):
        return "Nation " + self.longName + " has a landmass of " + str(int(self.area)) + " km^2"
    def embed(self):
        theEmbed = discord.Embed(title=self.longName, color=int('%02x%02x%02x' % self.color, 16), description=self.description)
        theEmbed.add_field(name="Test", value="test")
        theEmbed.set_footer(text="©2022 VicCO. All Gay Rights Reserved.")
        return theEmbed
def genProvs():
    reitak = population(0, random.randrange(1,1700), {0:100}, {0:100}, [])
    sajek = population(1, random.randrange(1,1700), {0:100}, {0:100}, [])
    farms = building("farms", 5000, {"food":1}, {}, 1)
    for i in range(63822):
        file = open("./common/provinces/" + str(i) + ".txt", "wb")
        pops = [reitak.toList(),sajek.toList()]
        builds = [farms.toList()]
        thing = [pops,builds]
        pickle.dump(thing, file)

def writeAdjacencies():
    adj = {}
    checkedColors = []
    count = 0
    for h in range(provMapHeight):
        for w in range(provMapWidth):
            if provDat[h,w] != (0,0,0) and (provDat[h,w] not in checkedColors):
                adjColors = []
                checkedColors.append(provDat[h,w])
                prov = getProvinceFromColor(provDat[h,w])
                provPixels = provClassDict[prov].pixels
                if not prov in adj:
                    adj[prov] = []

                for p in provPixels: 
                    hp = p[0]
                    hw = p[1]
                    for j in range(-1,2):
                        for k in range(-1,2):
                            if not (j == 0 and k == 0):
                                a = hp+j
                                b = hw+k
                                if a >= 0 and a < provMapHeight and b >= 0 and b < provMapWidth:
                                    if provDat[a,b] not in adjColors and provDat[a,b] != (0,0,0) and provDat[a,b] != provDat[h,w]:
                                        adjColors.append(provDat[a,b])
                for l in adjColors:
                    adj[prov].append(getProvinceFromColor(l))
                count += 1
                if count % 100 == 0:
                    print(count)
    file = open("./map/adjacencies.txt", "wb")
    pickle.dump(adj, file)
    file.close()
    print("Done writing adjacencies!")
    print(adj[0])

def genAdjNumbers():
    for x in list(adjacencies.keys()):
        prov = x
        amount = len(adjacencies[x])
        adjNumbers[x] = amount

def getProvinceFromColor(color):
    text = ";{0};{1};{2}".format(color[0],color[1],color[2])
    for l in defLines:
        if text in l:
            return int(l.split(";")[0].strip())
    
    return -1

def readProvs():
    files = os.listdir("./common/provinces/")
    for f in files:
        with open("./common/provinces/" + str(f), "rb") as pain:
            id = int(f.split(".")[0].strip())
            list = pickle.load(pain)
            popInfo = list[0]
            buildingInfo = list[1]
            pops = []
            buildings = []
            for i in range(len(popInfo)):
                things = popInfo[i]
                pops.append(population(things[0],things[1],things[2],things[3],things[4]))
            for i in range(len(buildingInfo)):
                things = buildingInfo[i]
                buildings.append(population(things[0],things[1],things[2],things[3],things[4]))
            prov = province(id, pops, buildings)
            provClassDict[id] = prov

def readRegions():
    files = os.listdir("./common/regions/")
    for f in files:
        lines = open("./common/regions/" + str(f), "r").readlines()
        name = f.split(".")[0]
        longName = lines[0].split(";")[0].strip()
        provs = lines[1].split(";")[0].strip().split(",")
        provs2 = []
        for i in provs:
            provs2.append(provClassDict[int(i)])
        capital = int(lines[2].split(";")[0].strip())
        autonomy = int(lines[3].split(";")[0].strip())
        desc = lines[4].split(";")[0].strip()
        dmz = bool(lines[5].split(";")[0].strip())
        regionClassDict[name] = region(provs2,name,longName,capital,autonomy,desc,dmz)

def readNations():
    files = os.listdir("./common/nations/")
    for f in files:
        lines = open("./common/nations/" + str(f), "r").readlines()
        name = f.split(".")[0]
        longName = lines[0].split(";")[0].strip()
        shortName = lines[1].split(";")[0].strip()
        regions = lines[2].split(";")[0].strip().split(",")
        regions2 = []
        for i in regions:
            regions2.append(regionClassDict[i.strip()])
        color = lines[3].split(";")[0].strip().split(",")
        color = (int(color[0].strip()),int(color[1].strip()),int(color[2].strip()))
        desc = lines[4].split(";")[0].strip()
        capital = int(lines[5].split(";")[0].strip())
        ideology = int(lines[6].split(";")[0].strip())

        nationClassDict[name] = nation(regions2,shortName,longName,color,capital,desc,ideology)

def writeRandRegions():
    print("Doing the thing...")
    adjKeys = list(adjacencies.keys())
    addedToARegion = []

    inverted = {}
    for lol in list(adjNumbers.keys()):
        if not adjNumbers[lol] in inverted:
            inverted[adjNumbers[lol]] = []
        inverted[adjNumbers[lol]].append(lol)
    priority = []
    for l in inverted.keys():
        things = inverted[l]
        random.shuffle(things)
        for thing in things:
            priority.append(thing)

    FIRST = ['A', 'Ag', 'Ar', 'Ara', 'Anu', 'Bal', 'Bil', 'Boro', 'Bern', 'Bra', 'Cas', 'Cere', 'Co', 'Con',
    'Cor', 'Dag', 'Doo', 'Elen', 'El', 'En', 'Eo', 'Faf', 'Fan', 'Fara', 'Fre', 'Fro', 'Ga', 'Gala', 'Has', 
    'He', 'Heim', 'Ho', 'Isil', 'In', 'Ini', 'Is', 'Ka', 'Kuo', 'Lance', 'Lo', 'Ma', 'Mag', 'Mi', 'Mo', 
    'Moon', 'Mor', 'Mora', 'Nin', 'O', 'Obi', 'Og', 'Pelli', 'Por', 'Ran', 'Rud', 'Sam',  'She', 'Sheel', 
    'Shin', 'Shog', 'Son', 'Sur', 'Theo', 'Tho', 'Tris', 'U', 'Uh', 'Ul', 'Vap', 'Vish', 'Ya', 'Yo', 'Yyr']
    random.shuffle(FIRST)
 
    SECOND = ['ba', 'bis', 'bo', 'bus', 'da', 'dal', 'dagz', 'den', 'di', 'dil', 'din', 'do', 'dor', 'dra', 
        'dur', 'gi', 'gauble', 'gen', 'glum', 'go', 'gorn', 'goth', 'had', 'hard', 'is', 'ki', 'koon', 'ku', 
        'lad', 'ler', 'li', 'lot', 'ma', 'man', 'mir', 'mus', 'nan', 'ni', 'nor', 'nu', 'pian', 'ra', 'rak', 
        'ric', 'rin', 'rum', 'rus', 'rut', 'sek', 'sha', 'thos', 'thur', 'toa', 'tu', 'tur', 'tred', 'varl',
        'wain', 'wan', 'win', 'wise', 'ya']
    random.shuffle(SECOND)

    names = []
    for f in FIRST:
        for l in SECOND:
            names.append(f + l)
    
    count = 0
    for x in range(len(priority)):
        maxSize = random.randrange(20,90)
        spookyProv = priority[x]
        doLoop = True
        toAdd = []
        if spookyProv not in addedToARegion:
            toAdd.append(spookyProv)
            name = names[count]
            print("Prov:", spookyProv, "Count:", count)
            while doLoop:
                doLoop = False
                for thingy in toAdd:
                    adjs = adjacencies[thingy]
                    for adj in adjs:
                        if (adj not in toAdd) and (adj not in addedToARegion) and (len(toAdd) < maxSize):
                            toAdd.append(adj)
                            doLoop = True
            provString = ""
            for l in toAdd:
                addedToARegion.append(l)
                provString += str(l) + ", "
            provString = provString[:-2] + " ; provinces\n"
            lines = []
            lines.append(name + " ; name\n")
            lines.append(provString)
            lines.append("-1 ; capital\n")
            lines.append("5 ; capital\n")
            lines.append("A region! ; desc\n")
            lines.append("False ; dmz")
            file = open("./common/regions/" + name.lower() + ".txt", "w")
            file.writelines(lines)
            file.close()
            count += 1
    print("DONE!")


def calculateArea(pixels):
    provinceMap = Image.open("./map/provinces.bmp")
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

def getProvinceName(province):
    line = defLines[province]
    try:
        name = line.split(";")[4].strip()
    except:
        name = "unknown"
    return name

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
        line = (open("./common/regions/" + regions[i] + ".txt", "r").readlines())[1]
        line = line.split(";")[0].strip()
        p = line.split(",")
        for i in p:
            provinces.append(int(i))
    
    return provinces

def getRegionProvinces(region):
    provinces = []

    line = (open("./common/regions/" + region + ".txt", "r").readlines())[1]
    line = line.split(";")[0].strip()
    p = line.split(",")
    for i in p:
        provinces.append(int(i))
    
    return provinces

def getProvinceFromPixel(pixel):
    try:
        return pixelDictProvs[pixel]
    except:
        return -1
def getRegionFromPixel(pixel):
    try:
        return pxlDictRegions[pixel]
    except:
        return "undef"