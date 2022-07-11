import PIL, common, os, math, random, json
from copy import deepcopy
from PIL import Image, ImageDraw, ImageFont
import numpy as np
Image.MAX_IMAGE_PIXELS = None

def get_nation_dict(): # Returns a dictionary with the region ID being the key, and a list of coordinates of every pixel in the region is returned.
    nation_dict = {}
    region_colors = []

    nations = os.listdir("./common/nations/")
    for nation in nations:
        nation_dict[nation] = {"regions": {}}
        nation_info = json.load(open(f"./common/nations/{nation}/info.json", "r"))
        for key in list(nation_info.keys()):
            nation_dict[nation][key] = nation_info[key] # Add all the info from the info file to the nation state.

        region_info = json.load(open(f"./common/nations/{nation}/regions.json", "r"))
        for region in list(region_info.keys()):
            nation_dict[nation]["regions"][region] = {}
            for key in list(region_info[region].keys()):
                nation_dict[nation]["regions"][region][key] = region_info[region][key]
            nation_dict[nation]["regions"][region]["color"] = tuple(nation_dict[nation]["regions"][region]["color"])
            region_colors.append(common.rgb_to_int(tuple(nation_dict[nation]["regions"][region]["color"])))

    color_dict = {}
    for color in region_colors:
        color_dict[color] = []

    print(len(color_dict.keys()))

    white_int = common.rgb_to_int((255,255,255))
    black_int = 0
    for y in range(len(common.np_dot)):
        for x in range(len(common.np_dot[0])):
            value = common.np_dot[y][x]
            if value != white_int and value != black_int:
                color_dict[value].append((x,y))

    for nation in list(nation_dict.keys()):
        for region in list(nation_dict[nation]["regions"].keys()):
            region_color = nation_dict[nation]["regions"][region]["color"]
            color_int = common.rgb_to_int(region_color)
            coords = color_dict[color_int]
            nation_dict[nation]["regions"][region]["pixels"] = coords

    return nation_dict

def draw_nation(nation, pixel_array):
    nation_info = common.nation_dict[nation]
    print("Drawing nation: " + nation_info["short name"])
    
    light_borders = []
    heavy_borders = []
    sea_borders = []
    nation_regions = list(nation_info["regions"].keys())
    nation_pixels = []

    for region_num in range(len(nation_regions)):
        region = nation_regions[region_num]
        region_info = nation_info["regions"][region]
        for pixel in region_info["pixels"]:
            nation_pixels.append(pixel)
            if pixel[0] > common.map_width:
                print("X greater than map width", pixel)
                exit("X greater than map width")
            if pixel[1] > common.map_height:
                print("Y greater than map height", pixel)
                exit("Y greater than map height")
            pixel_array[pixel[0]][pixel[1]] = (0,0,region_num) ## Using this method limits each nation to 255 regions.
        
        print(f"{nation}-{region_info['short name']}: {len(region_info['pixels'])} pixels")
        
        # LIGHT BORDERS GEN
        for pxl in region_info["pixels"]:
            check = True
            for j in range(-1,2):
                if check:
                    for k in range(-1,2):
                        if not (j == 0 and k == 0):
                            x = pxl[0]+j
                            y = pxl[1]+k
                            if x >= common.map_width:
                                x = 0
                            elif x < 0:
                                x = common.map_width-1

                            if not (y < 0 or y >= common.map_height):
                                if pixel_array[x][y] != (0,0,region_num):
                                    light_borders.append((pxl[0],pxl[1]))
                                    break
                else:
                    break
    print(f"{nation}: Done with region loop!")
    light_borders = list(dict.fromkeys(light_borders)) ## Remove Duplicates.

    for pxl in nation_pixels:
        pixel_array[pxl[0]][pxl[1]] = tuple(nation_info["color"]) ## Set all pixels in the nation to the national color.
    
    for pxl in nation_pixels:
        for j in range(-1,2):
            for k in range(-1,2):
                if not (j == 0 and k == 0):
                    x = pxl[0]+j
                    y = pxl[1]+k
                    if x >= common.map_width:
                        x = 0
                    elif x < 0:
                        x = common.map_width-1
                    
                    if not (y < 0 or y >= common.map_height):
                        if pixel_array[x][y] != (tuple(nation_info["color"])):
                            heavy_borders.append((pxl[0],pxl[1]))
                            if common.map_data[x,y] == (0,0,0):
                                sea_borders.append((pxl[0],pxl[1]))
    heavy_borders = list(dict.fromkeys(heavy_borders))
    sea_borders = list(dict.fromkeys(sea_borders))
    
    light_count = len(light_borders)-len(heavy_borders)
    heavy_count = len(heavy_borders)-len(sea_borders)
    sea_count = len(sea_borders)
    normal_count = len(nation_pixels)-sea_count-heavy_count-light_count
    print(str(light_count) + " light borders.")
    print(str(heavy_count) + " heavy borders.")
    print(str(sea_count) + " sea borders.")
    print(str(normal_count) + " normal pixels.")
    print("Nation " + nation_info["short name"] + ": DONE!")

    return light_borders, heavy_borders, sea_borders

def draw_political(add_background):
    print("DRAWING POLITICAL MAP!")
    if add_background:
        print("(With sea background)")
    img = Image.open("./map/inputs/map.png").convert("RGB")
    img_dat = img.load()
    pixel_array = []
    for _ in range(common.map_width):
        column = []
        for _ in range(common.map_height):
            column.append(()) 
        pixel_array.append(column)
    print("done writing empty array")

    for nation in list(common.nation_dict.keys()):
        nation_info = common.nation_dict[nation]
        pixels = []
        for region in list(nation_info["regions"].keys()):
            for px in list(nation_info["regions"][region]["pixels"]):
                pixels.append(px)

        color = tuple(nation_info["color"])
        light_color = (int(color[0]*.75),int(color[1]*.75),int(color[2]*.75))
        heavy_color = (int(color[0]*.5),int(color[1]*.5),int(color[2]*.5))
        sea_color = (int(color[0]*.2),int(color[1]*.2),int(color[2]*.2))
        light, heavy, sea = draw_nation(nation,pixel_array)
        for i in pixels:
            img_dat[i[0],i[1]] = color
        for i in light:
            img_dat[i[0],i[1]] = light_color
        for i in heavy:
            img_dat[i[0],i[1]] = heavy_color
        for i in sea:
            img_dat[i[0],i[1]] = sea_color
    
    if add_background:
        print("Adding sea background")
        sea_background = Image.open("map/inputs/sea_background.png").convert("RGB")
        sea_background_dat = sea_background.load()
        for w in range(common.map_width):
            for h in range(common.map_height):
                if img_dat[w,h] == (0,0,0):
                    img_dat[w,h] = sea_background_dat[w,h]
                elif img_dat[w,h] == (255,255,255):
                    img_dat[w,h] = (60,60,60)
    
    print("Saving...")

    img.save("./map/outputs/out.png")

    ratio = .5
    scale=(int(common.map_width*ratio),int(common.map_height*ratio))
    img = img.resize(scale)
    print("Saving scaled...")
    img.save("./map/outputs/out_scaled.png")

    print("Done drawing political map! >w<")