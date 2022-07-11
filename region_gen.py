# import os

# colors = []
# import random

# if not os.path.exists("common/regions/new_regions"):
#     os.makedirs("common/regions/new_regions")
# directories = os.listdir("./common/regions/")
# for directory in directories:
#     things = os.listdir("./common/regions/" + directory)
#     for thing in things:
#         lines = open(f"common/regions/{directory}/{thing}").readlines()
#         color = lines[0].split(";")[0].strip().split(",")
#         color = (int(color[0].strip()),int(color[1].strip()),int(color[2].strip()))
#         colors.append(color)

# notIn = False

# while not notIn:
#     toGive = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
#     if toGive not in colors and toGive != (0,0,0) and toGive != (255,255,255):
#         notIn = True

# print(toGive)

# name = input("Enter a name for the new region:").strip()

# lines = []
# lines.append(f"{str(toGive[0])},{str(toGive[1])},{str(toGive[2])} ; color\n")
# lines.append(f"{name} ; name\n")
# lines.append("-1 ; capital\n")
# lines.append("5 ; autonomy\n")
# lines.append("A region! ; description")

# color = '%02x%02x%02x' % toGive

# print(f"#{color}")

# g = open(f"common/regions/new_regions/{name.lower()}.txt", "w")
# g.writelines(lines)
# g.close()

# os.system(f"wl-copy {color}")

import os, json, random

nation_to_add_to = input("Nation to add region to: ").strip()
region_to_add = input("Name of region to add: ").strip()

nation_exists = False

if os.path.exists(f"./common/nations/{nation_to_add_to.lower()}"):
    nation_exists = True

if not nation_exists:
    os.mkdir(f"./common/nations/{nation_to_add_to.lower()}")
    dic = {
        "short name": f"{nation_to_add_to}",
        "long name": f"{nation_to_add_to}",
        "description": "a cool nation",
        "color": [random.randint(50,150),random.randint(50,150),random.randint(50,150)]
    }
    json_obj = json.dumps(dic, indent = 4)
    with open(f"./common/nations/{nation_to_add_to.lower()}/info.json", "w") as outfile:
        outfile.write(json_obj)
        outfile.close()
    with open(f"./common/nations/{nation_to_add_to.lower()}/regions.json", "w") as outfile:
        outfile.write(json.dumps({}))
        outfile.close()

region_colors = []
region_names = []

for nation in os.listdir("./common/nations/"):
    nation_regions = json.load(open(f"./common/nations/{nation}/regions.json"))
    regions = list(nation_regions.keys())
    for region in regions:
        region_color = nation_regions[region]["color"]
        region_colors.append(region_color)
        region_names.append(region)

not_in = False

while not not_in:
    to_give = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
    if to_give not in region_colors and to_give != (0,0,0) and to_give != (255,255,255):
        not_in = True

current_regions = json.load(open(f"./common/nations/{nation_to_add_to.lower()}/regions.json"))

do = True

if region_to_add.lower() in region_names:
    do = False
    thing = input("Region name already exists. Do anyways?").strip().lower()
    if thing == "y":
        do = True

if do:
    to_add =  {
        "short name": region_to_add,
        "long name": region_to_add,
        "color": to_give
    }

    current_regions[region_to_add.lower()] = to_add

    with open(f"./common/nations/{nation_to_add_to.lower()}/regions.json", "w") as to_edit:
        to_edit.write(json.dumps(current_regions, indent = 4))
        to_edit.close()

    color = '%02x%02x%02x' % tuple(to_give)

    print(f"#{color}")

    os.system(f"wl-copy {color}")

