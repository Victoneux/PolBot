import discord
import os, random, mapping, math, json
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

def initialize():
    global nation_dict, pixel_dict, planet_dict, system_info, map_width, map_height, the_map, map_data
    nation_dict = mapping.get_nation_dict()
    the_map = Image.open("./map/inputs/map.png").convert('RGB')
    map_data = the_map.load()
    map_width, map_height = the_map.size

    pixel_dict = {} ## Map Each Pixel (w,h) to a (nation,region). Ex: pixel_dict[(1110,500)] would return ("real_nation", "real_region_within_nation")

    for nation in list(nation_dict.keys()):
        regions = nation_dict[nation]["regions"]
        for region in list(regions.keys()):
            pixels = nation_dict[nation]["regions"][region]["pixels"]
            area = calculate_area(pixels)
            nation_dict[nation]["regions"][region]["area"] = area
            for px in pixels:
                pixel_dict[px] = (nation,region)

    system_info = json.load(open("./common/planets/info.json"))
    planet_dict = {}
    
    for planet in os.listdir("./common/planets/"):
        path = f"./common/planets/{planet}"
        if os.path.isdir(path):
            planet_dict[planet] = {}
            planet_info = json.load(open(f"{path}/info.json"))
            for key in list(planet_info.keys()):
                planet_dict[planet][key] = planet_info[key]
            planet_info["surface gravity"] = calculate_gravity(planet_info["mass base"],planet_info["mass factor"],planet_info["radius"])

    print("Successfully initiated! :)")

def calculate_area(pixels): ## Use some fancy equirectangular math to calculate the area of a set of pixels based on the area of each individual pixels.

    radius = 6378

    totArea = 0
    
    for x in range(len(pixels)):
        y = (abs((pixels[x][1])-(map_height/2))/(map_height/2))*(math.pi/2)
        decimal_area = math.cos(y)
        pixel_equator=(math.pi*radius*2)/map_width ## Length & Width of a pixel at the equator.
        totArea += pixel_equator * (pixel_equator * decimal_area)

    return totArea

def get_nation_pixels(nation): ## Get the pixels of a nation.
    nation_info = nation_dict[nation]
    pixels = []
    for region in nation_info["regions"]:
        for px in nation_info["regions"][region]["pixels"]:
            pixels.append(px)
    return pixels

def get_nation_area(nation): ## Get the area of a nation.
    nation_info = nation_dict[nation]
    area = 0
    for region in nation_info["regions"]:
        area += nation_info["regions"][region]["area"]
    return area

def calculate_gravity(mass_base, mass_factor, distance):
    mass = mass_base*pow(10,mass_factor)
    G = 6.67*pow(10,11)
    acceleration = (G*mass)/(distance*distance)
    return acceleration