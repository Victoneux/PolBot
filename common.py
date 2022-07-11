import discord
import os, random, mapping, math, json
from PIL import Image
import numpy as np
Image.MAX_IMAGE_PIXELS = None

def initialize():
    global nation_dict, planet_dict, system_info, map_width, map_height, the_map, map_data, np_dot, np_array
    print("Loading . . .")
    the_map = Image.open("./map/inputs/map.png").convert('RGB')
    map_data = the_map.load()
    map_width, map_height = the_map.size
    np_array = np.array(the_map)
    np_dot = np.dot(np_array.astype(np.uint32),[1,256,65536])
    nation_dict = mapping.get_nation_dict()

    print("Done getting nation dict . . .")


    system_info = json.load(open("./common/planets/info.json"))
    planet_dict = {}
    
    for planet in os.listdir("./common/planets/"):
        path = f"./common/planets/{planet}"
        if os.path.isdir(path):
            planet_dict[planet] = {}
            if os.path.exists(f"./common/planets/{planet}/render.png"):
                planet_dict[planet]["has render"] = True
            else:
                planet_dict[planet]["has render"] = False
            planet_info = json.load(open(f"{path}/info.json"))
            for key in list(planet_info.keys()):
                planet_dict[planet][key] = planet_info[key]
            planet_dict[planet]["surface gravity"] = calculate_gravity(planet_info["mass base"],planet_info["mass factor"],planet_info["radius"])

    print("Done getting planet dict . . .")

    for nation in list(nation_dict.keys()):
        if os.path.exists(f"./common/nations/{nation}/flag.png"):
            nation_dict[nation]["has flag"] = True
        else:
            nation_dict[nation]["has flag"] = False
        regions = nation_dict[nation]["regions"]
        for region in list(regions.keys()):
            pixels = nation_dict[nation]["regions"][region]["pixels"]
            area = calculate_area(pixels)
            nation_dict[nation]["regions"][region]["area"] = area
        nation_dict[nation]["area"] = get_nation_area(nation)

    sorted_list = sorted(nation_dict.items(), key=lambda x:x[1]["area"], reverse=True)
    nation_dict = dict(sorted_list)

    print("Done with area calculations . . .")

    print("Successfully initiated! :)")

def calculate_area(pixels): ## Use some fancy equirectangular math to calculate the area of a set of pixels based on the area of each individual pixels.

    radius = get_main_planet_radius() / 1000

    for pixel_num in range(len(pixels)):
        pixels[pixel_num] = pixels[pixel_num][1]
    unique_vals = np.unique(pixels, return_counts=True)

    half_height = map_height/2
    half_pi = math.pi/2

    totArea = 0
    pixel_equator=(math.pi*radius*2)/map_width ## Length & Width of a pixel at the equator.
    
    for i in range(len(unique_vals[0])):
        y = unique_vals[0][i]
        count = unique_vals[1][i]
        y_new = ((y-half_height)/half_height)*half_pi
        decimal_area = np.cos(y_new)
        to_add = ((pixel_equator**2)* count * decimal_area)
        totArea += to_add
    
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
    G = 6.67e-11
    acceleration = (G*mass)/(distance*distance)
    return round(acceleration, 2)

def generate_nation_embed(nation):
    try:
        nation_info = nation_dict[nation]
        the_embed = discord.Embed(
            title = nation_info["long name"],
            description = nation_info["description"],
            color = rgb_to_hex(tuple(nation_info["color"]))
        )
        the_embed.add_field(name="Area", value=f"{int(get_nation_area(nation)):,d} km²", inline=True)
        return the_embed
    except Exception as e:
        print(e)
        return ""

def generate_planet_embed(planet):
    try:
        planet_info = planet_dict[planet]
        the_embed = discord.Embed(
            title = planet_info["name"],
            description = planet_info["description"],
            color = rgb_to_hex(tuple(planet_info["color"]))
        )
        the_embed.add_field(name="Surface Gravity", value=f"{planet_info['surface gravity']} m/s²", inline=True)
        return the_embed
    except Exception as e:
        print(e)
        return ""

def rgb_to_hex(rgb):
    return int('%02x%02x%02x' % rgb, 16)

def rgb_to_int(rgb):
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]
    return (b << 16) + (g << 8) + (r << 0)

def get_main_planet_radius():
    main_planet = system_info["main planet"]
    planet_radius = planet_dict[main_planet]["radius"]
    return planet_radius