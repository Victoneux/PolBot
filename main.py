import common
from common import *
import mapping, random, discord, threading, os, timez
from threading import Thread
from datetime import datetime
from discord.ext import commands

common.initialize()
TOKEN = open("token.code", "r").read().strip()
mapping_thread = None
timeThread = Thread(target=timez.timeTick, args=())
timeThread.start()

bot = commands.Bot(command_prefix=".")
print("Booted!")

@bot.command()
async def regions(ctx, *args):
    if len(args) < 1:
        await ctx.channel.send("List regions of a nation. .regions (nation)")
    else:
        text = ""
        for arg in args:
            text += arg + " "
        nation = text.lower().strip()
        try:
            nation_info = common.nation_dict[nation]
            regions = nation_info["regions"]
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
    nations = list(common.nation_dict.keys())
    nation_count = len(nations)
    do_loop = True
    done_once = False
    while do_loop:
        if not done_once:
            string = "***[code] Nation - Area ***\n"
            done_once = True
        else:
            string = ""
        while len(string) < 1900 and len(nations) > 0:
            nation = nations.pop(0)
            string += f"> [{nation}] **{common.nation_dict[nation]['short name']}** - {str(int(common.get_nation_area(nation)))} km²\n"
        if len(nations) == 0:
            string += f"***{nation_count} total nations.***"
            do_loop = False
        await ctx.channel.send(string)

@bot.command()
async def planets(ctx):
    main_planet = common.system_info['main planet']
    planets = list(common.planet_dict.keys())
    planet_count = len(planets)
    do_loop = True
    while do_loop:
        string = ""
        while len(string) < 1900 and len(planets) > 0:
            planet = planets.pop(0)
            if planet == main_planet:
                string += f"> __**{common.planet_dict[planet]['name']}**__ - {common.planet_dict[planet]['short description']}\n"
            else:
                string += f"> **{common.planet_dict[planet]['name']}** - {common.planet_dict[planet]['short description']}\n"
        if len(planets) == 0:
            do_loop = False
        await ctx.channel.send(string)


@bot.command()
async def nation(ctx, *args):
    if len(args) == 0:
        await ctx.channel.send("> Read a nation.")
    else:
        text = ""
        for arg in args:
            text += arg.strip() + " "
        text = text.strip()
        try:
            the_embed = common.generate_nation_embed(text)
            if common.nation_dict[text]["has flag"] == True:
                flag = discord.File(f"./common/nations/{text}/flag.png", filename="flag.png")
                the_embed.set_thumbnail(url="attachment://flag.png")
                await ctx.channel.send(file=flag, embed=the_embed)
            else:
                await ctx.channel.send(embed=the_embed)
        except Exception as e:
            await ctx.channel.send(f"Failed to run command. {e}")

# @bot.command()
# async def region(ctx, *args):
#     if len(args) == 0:
#         await ctx.channel.send("> Read region info.")
#     else:
#         try:
#             await ctx.channel.send(embed=common.regionClassDict[args[0].lower().strip()].embed())
#         except:
#             await ctx.channel.send("Failed to run command.")

# @bot.command()
# async def area(ctx, *args):
#     if len(args) == 0:
#         await ctx.channel.send("> Get the area of a region or nation. .area [region (nation/region)]/[nation (nation)]")
#     elif len(args) == 1:
#         await ctx.channel.send(str(int(common.nationClassDict[args[0].strip().lower()].area)) + " km²")
#     elif len(args) == 2:
#         if args[0].lower() == "region":
#             await ctx.channel.send(str(int(common.regionClassDict[args[1].strip().lower()].area)) + " km²")
#         elif args[0].lower() == "nation":
#             await ctx.channel.send(str(int(common.nationClassDict[args[1].strip().lower()].area)) + " km²")
#         else:
#             await ctx.channel.send("Invalid syntax. area [region/nation] (name)")

@bot.command()
async def generatepolmap(ctx, *args):
    add_background = False
    if (len(args) > 0):
        if args[0] == "background":
            add_background = True
    global mapping_thread
    if str(ctx.message.author.id) == "742193269655601272":
        if mapping_thread != None:
            if not mapping_thread.is_alive():
                await ctx.channel.send("> Generating. Please note this may take a while. Additional \'heavy\' commands should not be run in the mean time.")
                mapping_thread = Thread(target=mapping.draw_political, args=(add_background,))
                mapping_thread.start()
            else:
                await ctx.channel.send("> There is an active thread. Please try again later!")
        else:
            await ctx.channel.send("> Generating. Please note this may take a while. Additional \'heavy\' commands should not be run in the mean time.")
            mapping_thread = Thread(target=mapping.draw_political, args=(add_background,))
            mapping_thread.start()
    else:
        await ctx.channel.send("> You are not our godly administrator! SHAME!")

# @bot.command()
# async def reinitialize(ctx):
#     if str(ctx.message.author.id) == "742193269655601272":
#         await ctx.channel.send("Reinitializing. The bot will not function in the mean time.")
#         timez.saveTime()
#         common.initialize()
#     else:
#         await ctx.channel.send("You can't do that. NO.")

# @bot.command()
# async def area(ctx, *args):
#     if len(args) < 2:
#         await ctx.channel.send("> Calculate the area of something. Syntax: .area (nation) (region)")
#     else:
#         action = args[0].strip().lower()
#         place = args[1].strip().lower()
#         if action == "nation":
#             await ctx.channel.send("Nation " + place + " has area " + str(int(mapping.calculateNationArea(place, common.provinceDict))) + " km²")
#         elif action == "region":
#             await ctx.channel.send("Region " + place + " has area " + str(int(mapping.calculateRegionArea(place, common.provinceDict))) + " km²")

# @bot.command()
# async def dice(ctx, *args):
#     if len(args) <= 0:
#         await ctx.channel.send("> Rolling a 20 siced dice. Result: " + str(random.randrange(1,21)))
#     if len(args) == 1:
#         try:
#             sides = int(args[0].strip())
#             await ctx.channel.send("> Rolling a " + str(sides) + " sided dice. Result: " + str(random.randrange(1,sides+1)))
#         except:
#             await ctx.channel.send("> Failed. Did you input a number?")

@bot.command()
async def ping(ctx, *args):
    space = ""
    to_send = ""
    if len(args) > 0:
        for i in range(len(args)):
            if args[i].strip().lower() == "ping":
                if i == len(args)-1:
                    to_send += "pong"
                    space = " "
                else:
                    to_send += "pong "
                    space = " "
    else:
        to_send = ""
    await ctx.channel.send("pong" + space + to_send + "!")

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

# @bot.command()
# async def random_nation(ctx):
#     nations = list(common.nationClassDict.keys())
#     nation = random.choice(nations)
#     await ctx.channel.send(nation)

bot.run(TOKEN)
timez.saveTime()
timez.breakLoop()