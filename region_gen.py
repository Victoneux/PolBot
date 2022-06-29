import os

colors = []
import random

if not os.path.exists("common/regions/new_regions"):
    os.makedirs("common/regions/new_regions")
directories = os.listdir("./common/regions/")
for directory in directories:
    things = os.listdir("./common/regions/" + directory)
    for thing in things:
        lines = open(f"common/regions/{directory}/{thing}").readlines()
        color = lines[0].split(";")[0].strip().split(",")
        color = (int(color[0].strip()),int(color[1].strip()),int(color[2].strip()))
        colors.append(color)

notIn = False

while not notIn:
    toGive = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    if toGive not in colors and toGive != (0,0,0) and toGive != (255,255,255):
        notIn = True

print(toGive)

name = input("Enter a name for the new region:").strip()

lines = []
lines.append(f"{str(toGive[0])},{str(toGive[1])},{str(toGive[2])} ; color\n")
lines.append(f"{name} ; name\n")
lines.append("-1 ; capital\n")
lines.append("5 ; autonomy\n")
lines.append("A region! ; description")

color = '%02x%02x%02x' % toGive

print(f"#{color}")

g = open(f"common/regions/new_regions/{name.lower()}.txt", "w")
g.writelines(lines)
g.close()

os.system(f"echo '{color}' | xclip -select clipboard")
