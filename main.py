import common, get_pixel
from common import *
import mapping, random, discord, threading, os, timez
from threading import Thread
from datetime import datetime
from discord.ext import commands

common.initialize()
TOKEN = open("token.code", "r").read().strip()
mappingThread = None
timeThread = Thread(target=timez.timeTick, args=())
timeThread.start()

bot = commands.Bot(command_prefix=".")
print("Booted!")

@bot.command()
async def regions(ctx):
    regions = list(common.regionClassDict.keys())
    str = ""
    for r in range(len(regions)):
        str += regions[r]
        if r != len(regions)-1:
            str += ", "
    await ctx.channel.send("> " + str)
@bot.command()
async def nations(ctx):
    nations = list(common.nationClassDict.keys())
    str = ""
    for r in range(len(nations)):
        str += nations[r]
        if r != len(nations)-1:
            str += ", "
    await ctx.channel.send("> " + str)

@bot.command()
async def nation(ctx, *args):
    if len(args) == 0:
        await ctx.channel.send("> Read a nation.")
    else:
        try:
            await ctx.channel.send(embed=common.nationClassDict[args[0].lower().strip()].embed())
        except:
            await ctx.channel.send("Failed.")

@bot.command()
async def area(ctx, *args):
    if len(args) == 0:
        await ctx.channel.send("> Get the area of a region or nation. .area (region/nation) (name)")
    elif len(args) == 1:
        await ctx.channel.send(str(int(common.nationClassDict[args[0].strip().lower()].area)) + " km²")
    elif len(args) == 2:
        if args[0].lower() == "region":
            await ctx.channel.send(str(int(common.regionClassDict[args[1].strip().lower()].area)) + " km²")
        elif args[0].lower() == "nation":
            await ctx.channel.send(str(int(common.nationClassDict[args[1].strip().lower()].area)) + " km²")
        else:
            await ctx.channel.send("Invalid")

@bot.command()
async def findAdjacencies(ctx):
    global mappingThread
    if str(ctx.message.author.id) == "742193269655601272":
        if mappingThread != None:
            if not mappingThread.is_alive():
                mappingThread = Thread(target=common.writeAdjacencies, args=())
                mappingThread.start()
                await ctx.channel.send("Writing adjacencies! This may take a while.")
            else:
                await ctx.channel.send("The mapping thread is busy! Try again in a bit.")
        else:
            mappingThread = Thread(target=common.writeAdjacencies, args=())
            mappingThread.start()
            await ctx.channel.send("Writing adjacencies! This may take a while.")
    else:
        await ctx.channel.send("Usable by vic only.")

@bot.command()
async def generatepolmap(ctx):
    global mappingThread
    if str(ctx.message.author.id) == "742193269655601272":
        if mappingThread != None:
            if not mappingThread.is_alive():
                await ctx.channel.send("> Generating. Please note this may take a while. Additional \'heavy\' commands should not be run in the mean time.")
                mappingThread = Thread(target=mapping.drawPolitical, args=())
                mappingThread.start()
            else:
                await ctx.channel.send("> There is an active thread. Please try again later!")
        else:
            await ctx.channel.send("> Generating. Please note this may take a while. Additional \'heavy\' commands should not be run in the mean time.")
            mappingThread = Thread(target=mapping.drawPolitical, args=())
            mappingThread.start()
    else:
        await ctx.channel.send("> You are not our godly administrator! SHAME!")

@bot.command()
async def genREGIONS(ctx):
    if str(ctx.message.author.id) == "742193269655601272":
        common.writeRandRegions()
    else:
        await ctx.channel.send("no")

@bot.command()
async def getMap(ctx, *args):
    if len(args) <= 0:
        await ctx.channel.send("> Fetches a specific type of map, optionally from a specific date. Format: .getMap (mapType) (date y/m/d)")
    elif len(args) >= 1:
        type = args[0].strip().lower()
        if str(ctx.message.author.id) == "742193269655601272":
            if len(args) == 1:
                if type == "political":
                    dir = os.listdir("./history/maps/political")
                    dir.sort(key = lambda date: datetime.strptime(date, '%Y_%m_%d.png'))
                    latest = dir[len(dir)-1]
                    latestStr = latest.split(".")[0].split("_")
                    latestStr = latestStr[0] + "/" + latestStr[1] + "/" + latestStr[2]
                    await ctx.channel.send(file=discord.File("./history/maps/political/" + latest), content="> Political map, as of " + latestStr)
                # elif type == "population":
                #     dir = os.listdir("./history/maps/population")
                #     dir.sort(key = lambda date: datetime.strptime(date, '%Y_%m_%d.png'))
                #     latest = dir[len(dir)-1]
                #     latestStr = latest.split(".")[0].split("_")
                #     latestStr = latestStr[0] + "/" + latestStr[1] + "/" + latestStr[2]
                #     await ctx.channel.send(file=discord.File("./history/maps/population/" + latest), content="> Population density map, as of " + latestStr)
                else:
                    await ctx.channel.send("> Unable to process.")
            elif len(args) == 2:
                dateToFind = datetime.strptime(args[1].strip(), "%Y/%m/%d")
                if type == "political":
                    dir = os.listdir("./history/maps/political")
                    dir.sort(key = lambda date: datetime.strptime(date, '%Y_%m_%d.png'))
                    dates = []
                    for i in range(len(dir)):
                        date = datetime.strptime(dir[i], "%Y_%m_%d.png")
                        dates.append(date)
                    matchingDate = dates[len(dates)-1]
                    for i in range(len(dates)-1, 0, -1):
                        if dateToFind < dates[i]:
                            if i > 0:
                                matchingDate = dates[i-1]
                            else:
                                matchingDate = dates[i]
                    text = matchingDate.strftime("%Y/%m/%d")
                    fileText = matchingDate.strftime("%Y_%m_%d" + ".png")
                    await ctx.channel.send(file=discord.File("./history/maps/political/" + fileText), content="> Political map, as of " + text)
                # elif type == "population":
                #     dir = os.listdir("./history/maps/population")
                #     dir.sort(key = lambda date: datetime.strptime(date, '%Y_%m_%d.png'))
                #     dates = []
                #     for i in range(len(dir)):
                #         date = datetime.strptime(dir[i], "%Y_%m_%d.png")
                #         dates.append(date)
                #     matchingDate = dates[len(dates)-1]
                #     for i in range(len(dates)-1, 0, -1):
                #         if dateToFind < dates[i]:
                #             if i > 0:
                #                 matchingDate = dates[i-1]
                #             else:
                #                 matchingDate = dates[i]
                #     text = matchingDate.strftime("%Y/%m/%d")
                #     fileText = matchingDate.strftime("%Y_%m_%d" + ".png")
                #     await ctx.channel.send(file=discord.File("./history/maps/population/" + fileText), content="> Political map, as of " + text)
        else:
            await ctx.channel.send("> You are not the admin, and cannot fetch the image. Please check <#920476735177379901>")

@bot.command()
async def getarea(ctx, *args):
    if len(args) < 2:
        await ctx.channel.send("> Calculate the area of something. Syntax: .getarea (nation/region) (nationName/regionName)")
    else:
        action = args[0].strip().lower()
        place = args[1].strip().lower()
        if action == "nation":
            await ctx.channel.send("Nation " + place + " has area " + str(int(mapping.calculateNationArea(place, common.provinceDict))) + " km²")
        elif action == "region":
            await ctx.channel.send("Region " + place + " has area " + str(int(mapping.calculateRegionArea(place, common.provinceDict))) + " km²")

@bot.command()
async def dothing(ctx):
    if str(ctx.message.author.id) == "742193269655601272":
        get_pixel.thing("./out.png")

@bot.command()
async def dice(ctx, *args):
    if len(args) <= 0:
        await ctx.channel.send("> Rolling a 20 siced dice. Result: " + str(random.randrange(1,21)))
    if len(args) == 1:
        try:
            sides = int(args[0].strip())
            await ctx.channel.send("> Rolling a " + str(sides) + " sided dice. Result: " + str(random.randrange(1,sides+1)))
        except:
            await ctx.channel.send("> Failed. Did you input a number?")

@bot.command()
async def ping(ctx, *args):
    space = ""
    tosend = ""
    if len(args) > 0:
        for i in range(len(args)):
            if args[i].strip().lower() == "ping":
                if i == len(args)-1:
                    tosend += "pong"
                    space = " "
                else:
                    tosend += "pong "
                    space = " "
    else:
        tosend = ""
    await ctx.channel.send("pong" + space + tosend + "!")

@bot.command()
async def time(ctx):
    await ctx.channel.send(datetime.strftime(timez.getTime(), "> %Y-%m-%d \n> %H:%M UTC"))

@bot.command()
async def rate(ctx, *args):
    if len(args) == 0:
        await ctx.channel.send("Current rate: " + str(timez.getRate()))
    elif len(args) == 1:
        if str(ctx.message.author.id) == "742193269655601272":
            try:
                thing = int(args[0])
                if thing <= 86400 and thing >= 0:
                    timez.setRate(thing)
                    await ctx.channel.send("Rate set to " + str(thing))
                else:
                    await ctx.channel.send("Cannot set rate. Too high or low?")
            except:
                await ctx.channel.send("Failed to set rate.")
        else:
            await ctx.channel.send("You are not the godly admin!")

bot.run(TOKEN)
timez.saveTime()
timez.breakLoop()