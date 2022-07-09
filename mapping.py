import PIL, common, os, math, random, json
from copy import deepcopy
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = None

def get_nation_dict(): # Returns a dictionary with the region ID being the key, and a list of coordinates of every pixel in the region is returned.
    nation_dict = {}
    color_dict = {}

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
            color_dict[nation_dict[nation]["regions"][region]["color"]] = (nation,region)
    
    region_map = Image.open("./map/inputs/map.png").convert("RGB")
    image_dat = region_map.load()
    width, height = region_map.size

    for h in range(height):
        for w in range(width):
            pR, pG, pB = image_dat[w,h]
            if (pR,pG,pB) != (0,0,0) and (pR,pG,pB) != (255,255,255):
                if "pixels" not in list(nation_dict[color_dict[(pR,pG,pB)][0]]["regions"][color_dict[(pR,pG,pB)][1]].keys()):
                    nation_dict[color_dict[(pR,pG,pB)][0]]["regions"][color_dict[(pR,pG,pB)][1]]['pixels'] = []
                nation_dict[color_dict[(pR,pG,pB)][0]]["regions"][color_dict[(pR,pG,pB)][1]]["pixels"].append((w,h)) ## Add the pixel to the nation's region's dict's list.
    region_map.close()
    return nation_dict

def draw_nation(nation, pixel_array, do_light):
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
            pixel_array[pixel[0]][pixel[1]] = (0,0,region_num) ## Using this method limits each nation to 255 regions.
        
        print(f"{nation}-{region_info['short name']}: {len(region_info['pixels'])} pixels")
        
        # LIGHT BORDERS GEN
        if do_light:
            for px in region_info["pixels"]:
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
    print(f"{nation}-{region_info['short name']}: Done with region loop!")
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
    
    if not do_light:
        light_count = 0
    else:
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
        light, heavy, sea = draw_nation(nation,pixel_array,False)
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