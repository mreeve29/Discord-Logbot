import os
from os import path
import random
import sys
import json
import discord
from discord.ext import commands
import time
import requests
import datetime

TOKEN = "enter token here"
GUILD = "enter guild here"
client = commands.Bot(command_prefix = "!", intents = discord.Intents.all())

# connection to server
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

def getStrMembers(vc):
    str = "["
    for m in vc.members:
        str += m.display_name + ", "
    str = str[0:-2]
    str += "]"
    if str == "]":
        return "None"
    else:
        return str

def log(msg):
    date = datetime.datetime.now()
    time = "[" + date.strftime("%x") + " " + date.strftime("%X") + "] "


    month = date.strftime("%-m")
    year = date.strftime("%Y")
    folder = month + "-" + year

    folderExists = os.path.exists("logs/" + folder)

    if(folderExists == False):
        os.mkdir("logs/" + folder)

    day = date.strftime("%x").replace("/","-")
    dayPath = "logs/" + folder + "/" + day + ".txt"
    logs = open(dayPath,"a")
    logs.write(time + msg + "\n")
    logs.close()



@client.event
async def on_voice_state_update(member, before, after):
    if before.self_mute == False and after.self_mute == True:
        log(member.display_name + " muted in " + after.channel.name + ", current members: " + getStrMembers(after.channel))
        return
    elif before.self_mute == True and after.self_mute == False:
        log(member.display_name + " unmuted in " + after.channel.name + ", current members: " + getStrMembers(after.channel))
        return

    if before.channel == None and after.channel != None:
        log(member.display_name + " joined " + after.channel.name + ", current members: " + getStrMembers(after.channel))
        return
    elif after.channel == None and before.channel != None:
        log(member.display_name + " disconnected from " + before.channel.name + ", current members: " + getStrMembers(before.channel))
        return
    elif after.channel != None and before.channel != None:
        log(member.display_name + " moved from " + before.channel.name + " to " + after.channel.name + ", current members: " + getStrMembers(after.channel))
        return


@client.event
async def on_member_update(before,after):
    if before.activity is None and after.activity is not None:
        print(after.activity.type)
        if(str(after.activity.type) == "ActivityType.playing"):
            msg = after.display_name + " is now playing " + str(after.activity.name)
            if(str(after.activity.details) != "None"):
                msg += " - " + str(after.activity.details)
            log(msg)
        else:
            log(after.display_name + "\'s activity is now " + str(after.activity))
        return
    elif str(before.activity) != str(after.activity) and after.activity is not None:
        print(after.activity.type)
        if(str(after.activity.type) == "ActivityType.playing" and before.activity.name == after.activity.name):
            msg = after.display_name + "\'s status in " + str(after.activity.name)
            if(str(after.activity.details) != "None"):
                msg += "changed to " + str(after.activity.details)
            else:
                msg += " changed to nothing"
            log(msg)
        else:
            log(after.display_name + "\'s activity changed from " + str(before.activity) + " to " + str(after.activity))
        return
    elif before.activity is not None and after.activity is None:
        print(before.activity.type)
        if(str(before.activity.type) == "ActivityType.playing"):
            msg = after.display_name + " stopped playing " + str(before.activity.name)
            if(str(before.activity.details) != "None"):
                msg += " - " + str(before.activity.details)
            log(msg)
        else:
            log(after.display_name + "\'s activity changed from " + str(before.activity) + " to nothing ")
        return

    if statusChange(before,after):    
        if after.status != "offline":
            log(after.display_name + "'s status changed: Desktop: " + str(after.desktop_status) + ", Mobile: " + str(after.mobile_status) + ", Web: " + str(after.web_status))
        elif after.status == "offline":
            log(before.display_name + "'s status changed: Desktop: " + str(before.desktop_status) + ", Mobile: " + str(before.mobile_status) + ", Web: " + str(before.web_status))



def statusChange(before, after):
    beforeDesktop = before.desktop_status
    beforeMobile = before.mobile_status
    beforeWeb = before.web_status
    afterDesktop = after.desktop_status
    afterMobile = after.mobile_status
    afterWeb = after.web_status

    desktop = beforeDesktop == afterDesktop
    mobile = beforeMobile == afterMobile
    web = beforeWeb == afterWeb

    return not (desktop and mobile and web)

client.run(TOKEN)
