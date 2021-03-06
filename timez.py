import time as t
import os, discord, threading
import datetime

saveLines = open("time.save", "r").readlines()
currentTime = datetime.datetime.strptime(saveLines[0].strip(), "%Y-%m-%d %H:%M:%S")
currentRate = int(saveLines[1])
doLoop = True

def saveTime():
    try:
        file = open("time.save", "w")
        file.write(str(currentTime) + "\n" + str(currentRate))
        print("Saved!")
    except:
        print("Failed to save!")

def breakLoop():
    global doLoop
    doLoop = False

def getTime():
    return currentTime

def getRate():
    return currentRate

def setRate(rate):
    global currentRate
    currentRate = rate

def timeTick():
    global currentTime
    time_passed = 0
    while doLoop:
        t.sleep(1)
        time_passed += currentRate
        if time_passed > 14400:
            time_passed = 0
            saveTime()
        currentTime += datetime.timedelta(seconds=currentRate)

print(getTime())

