class province():
    def __init__(self, id):
        self.id = id
        self.name = "undefined"
        self.population = 0
        self.coastal = False
        self.biome = "undefined"
        self.continent = 0
    
    def setName(self, name):
        self.name = name
    def setPopulation(self, pop):
        self.population = pop
    def setCoastal(self, bool):
        self.coastal = bool
    def setBiome(self, biome):
        self.biome = biome
    def setContinent(self, continent):
        self.continent = continent

    def getID(self):
        return self.id
    def getName(self):
        return self.name
    def getPopulation(self):
        return self.population
    
    def toString(self):
        if self.coastal == True:
            coastString = "a coastal "
        else:
            coastString = "not coastal. It is a "
        
        return self.name + " has id " + str(self.id) + " and population " + str(self.population) + ". The province is " + coastString + self.biome + " province. It is on " + readContinent(self.continent) + "."

def readContinent(id):
    provinceLine = open("continents").readlines()[id]
    provinceLine = provinceLine.split(";")
    return provinceLine[1].strip()

def readProvince(id):
    provinceLine = open("provinces").readlines()[id]
    provinceLine = provinceLine.split(";")
    p = province(id)
    p.setPopulation(int(provinceLine[4]))
    if provinceLine[5].lower() == "true":
        p.setCoastal(True)
    else:
        p.setCoastal(False)
    p.setBiome(provinceLine[6])
    p.setContinent(int(provinceLine[7]))
    nameLines = open("provinceNames").readlines()

    for l in (nameLines):
        split = l.split(";")
        if split[0] == str(id):
            p.setName(split[1].strip())
    
    return(p.toString())

    