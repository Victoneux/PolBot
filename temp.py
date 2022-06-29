import os, random
nations = []
directories = os.listdir("common/nations")
for directory in directories:
    files = os.listdir(f"common/nations/{directory}/")
    for file in files:
        nations.append(f"common/nations/{directory}/{file}")

for nation in nations:
    lines = open(nation).readlines()
    r = random.randint(10,200)
    g = random.randint(10,200)
    b = random.randint(10,200)
    lines[2] = f"{r},{g},{b} ; color\n"
    lines.pop(4)
    file = open(nation, 'w')
    file.writelines(lines)
    file.close()