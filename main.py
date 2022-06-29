import common
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
async def regions(ctx, *args):
    regions = list(common.regionClassDict.keys())
    if len(args) < 1:
        await ctx.channel.send("List regions of a nation. .regions (nation)")
    else:
        text = ""
        for arg in args:
            text += arg + " "
        nation = text.lower().strip()
        try:
            nation = common.nationClassDict[nation]
            regions = nation.regions
            string = ""
            for region in regions:
                thing = region.name
                string += "> " + thing + "\n"
            await ctx.channel.send(string)
        except Exception as e:
            await ctx.channel.send("Failed to run.")
            print(e)
@bot.command()
async def nations(ctx):
    nations = list(common.nationClassDict.keys())
    tempNationDict = {}
    string = ""
    for r in range(len(nations)):
        tempNationDict[nations[r]] = common.nationClassDict[nations[r]].area
    thing = {key: val for key, val in sorted(tempNationDict.items(), key=lambda ele: ele[1], reverse = True)}
    for gah in thing.keys():
        string += "> " + gah + " - " + str(int(thing[gah])) + " km²\n"
    await ctx.channel.send(string)

@bot.command()
async def nation(ctx, *args):
    if len(args) == 0:
        await ctx.channel.send("> Read a nation.")
    else:
        text = ""
        for arg in args:
            text += arg.strip() + " "
        try:
            await ctx.channel.send(embed=common.nationClassDict[text.lower().strip()].embed())
        except:
            await ctx.channel.send("Failed to run command.")

@bot.command()
async def region(ctx, *args):
    if len(args) == 0:
        await ctx.channel.send("> Read region info.")
    else:
        try:
            await ctx.channel.send(embed=common.regionClassDict[args[0].lower().strip()].embed())
        except:
            await ctx.channel.send("Failed to run command.")

@bot.command()
async def area(ctx, *args):
    if len(args) == 0:
        await ctx.channel.send("> Get the area of a region or nation. .area [region (nation/region)]/[nation (nation)]")
    elif len(args) == 1:
        await ctx.channel.send(str(int(common.nationClassDict[args[0].strip().lower()].area)) + " km²")
    elif len(args) == 2:
        if args[0].lower() == "region":
            await ctx.channel.send(str(int(common.regionClassDict[args[1].strip().lower()].area)) + " km²")
        elif args[0].lower() == "nation":
            await ctx.channel.send(str(int(common.nationClassDict[args[1].strip().lower()].area)) + " km²")
        else:
            await ctx.channel.send("Invalid syntax. area [region/nation] (name)")

@bot.command()
async def find_adjacencies(ctx):
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
async def generatepolmap(ctx, *args):
    addNames = False
    if (len(args) > 0):
        if args[0] == "names":
            addNames = True
    global mappingThread
    if str(ctx.message.author.id) == "742193269655601272":
        if mappingThread != None:
            if not mappingThread.is_alive():
                await ctx.channel.send("> Generating. Please note this may take a while. Additional \'heavy\' commands should not be run in the mean time.")
                mappingThread = Thread(target=mapping.drawPolitical, args=(addNames,))
                mappingThread.start()
            else:
                await ctx.channel.send("> There is an active thread. Please try again later!")
        else:
            await ctx.channel.send("> Generating. Please note this may take a while. Additional \'heavy\' commands should not be run in the mean time.")
            mappingThread = Thread(target=mapping.drawPolitical, args=(addNames,))
            mappingThread.start()
    else:
        await ctx.channel.send("> You are not our godly administrator! SHAME!")

@bot.command()
async def reinitialize(ctx):
    if str(ctx.message.author.id) == "742193269655601272":
        await ctx.channel.send("Reinitializing. The bot will not function in the mean time.")
        timez.saveTime()
        common.initialize()
    else:
        await ctx.channel.send("You can't do that. NO.")

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

@bot.command()
async def random_nation(ctx):
    nations = list(common.nationClassDict.keys())
    nation = random.choice(nations)
    await ctx.channel.send(nation)

bot.run(TOKEN)
timez.saveTime()
timez.breakLoop()