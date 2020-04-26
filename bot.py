# -*- coding: utf-8 -*-
import discord

from discord.ext.commands import Bot
from discord.ext import commands
from discord.utils import get

from datetime import datetime

import asyncio
import os

Tskxekengsiyu = discord.Client()  # Initialize Client
tskxekengsiyu = commands.Bot(command_prefix="!")  # Initialize client bot

versionnumber = "1.2.0"
modRoleNames = ["Olo'eyktan","Eyktan","frapo"]
activeRoleNames = ["Koaktu","Tsamsiyu","Tsamsiyutsyìp","Eykyu","Ikran Makto","Taronyu","Taronyutsyìp","Numeyu","Hapxìtu","Zìma'uyu","Ketuwong"]
activeRoleThresholds = [16384, 8192, 4096, 2048, 1024, 512, 256, 128, 64, 32, 16]

naviVocab = [
    # 0 1 2 3 4 5 6 7 actual
    ["", "'aw", "mune", "pxey", "tsìng", "mrr", "pukap", "kinä"],
    # 0 1 2 3 4 5 6 7 last digit
    ["", "aw", "mun", "pey", "sìng", "mrr", "fu", "hin"],
    # 0 1 2 3 4 5 6 7 first or middle digit
    ["", "", "me", "pxe", "tsì", "mrr", "pu", "ki"],
    # 0 1 2 3 4 powers of 8
    ["", "vo", "zam", "vozam", "zazam"],
    # 0 1 2 3 4 powers of 8 last digit
    ["", "l", "", "", ""],
]

send_time = '08:00'
message_channel_id = 516003512316854295

## Updates roles.
async def roleUpdate(count, check, message, user):
        i = 0
        activeRoles = message.guild.roles            
        for roles in activeRoleNames:
                if count >= activeRoleThresholds[i] and check.name != roles:
                        newRole = get(activeRoles, name=activeRoleNames[i])
                        await user.add_roles(newRole)
                        print('Tìmìng txintìnit alu ' + newRole.name + ' tuteru alu ' + user.display_name + '.')
                        if message.author.dm_channel is None:
                                await message.author.create_dm()
                        await message.author.send('**Seykxel sì nitram!** Set lu ngaru txintìn alu ' + newRole.name + '.')
                        if check.name != "@everyone":
                                await user.remove_roles(check)
                                print("'olaku txintìnit alu " + check.name + " ta " + user.display_name + ".")
                        break
                elif count >= activeRoleThresholds[i]:
                        break
                i += 1

async def time_check():
        await tskxekengsiyu.wait_until_ready()
        
        message_channel = tskxekengsiyu.get_channel(message_channel_id)
        bot_ready = tskxekengsiyu.is_closed()
        
        while not bot_ready:
                now = datetime.strftime(datetime.now(),'%H:%M')
                if now == send_time:
                        dateTimeObj = datetime.now()
                        timestampStr = dateTimeObj.strftime("%d-%m-%Y")
                        fileName = 'qotd/' + timestampStr + '.tsk'
                        if os.path.exists(fileName):
                                fh = open(fileName, 'r')
                                fileContents = fh.readlines(1)
                                strippedContents = fileContents[0].strip("['")
                                strippedContents = fileContents[0].strip("']")
                                fh.close()
                                os.remove(fileName)
                                await message_channel.send(strippedContents)
                                time = 90
                        else:
                                time = 1
                else:
                        time = 1
                await asyncio.sleep(time)

def reverse(s): 
    if len(s) == 0: 
        return s 
    else: 
        return reverse(s[1:]) + s[0] 

def wordify(input):
        rev = reverse(input)
        output = ""
        if len(input) == 1:
                if input == "0":
                    return "kewa"
        for i, d in enumerate(rev):
                if i == 0:  # 7777[7]
                        output = naviVocab[1][int(d)] + output
                        if int(d) == 1 and rev[1] != '0':
                                output = naviVocab[4][1] + output
                elif i == 1:  # 777[7]7
                        if int((d)) > 0:
                                output = naviVocab[2][int(d)] + naviVocab[3][1] + output
                elif i == 2:  # 77[7]77
                        if int(d) > 0:
                                output = naviVocab[2][int(d)] + naviVocab[3][2] + output
                elif i == 3:  # 7[7]777
                        if int(d) > 0:
                                output = naviVocab[2][int(d)] + naviVocab[3][3] + output
                elif i == 4:  # [7]7777
                        if int(d) > 0:
                                output = naviVocab[2][int(d)] + naviVocab[3][4] + output
        for d in ["01", "02", "03", "04", "05", "06", "07"]:
                if rev[0:2] == d:
                        output = output + naviVocab[4][1]
                output = output.replace("mm", "m")
                output += "a"
                return output

@tskxekengsiyu.event
async def on_ready():
        # This will be called when the bot connects to the server.
        print("Tskxekengsiyu alaksi lu.")
        tskxekengsiyu.loop.create_task(time_check())

@tskxekengsiyu.event
async def on_member_join(member):
        # This will automatically give anyone the 'frapo' role when they join the server.
        print(member.name + " zola'u.")
        newRole = get(member.guild.roles, name="frapo")
        await member.add_roles(newRole)
        print("Tìmìng tuteru alu " + member.name + " txintìnit alu " + newRole.name + ".")
        if member.dm_channel is None:
                await member.create_dm()
        await member.send("Zola'u nìprrte' ne **Olo' Tskengwiä**! Inan säomumit mì tsyänel alu #säomum rutxe. Lu awngaru tintìn a layu ngaru tengkrr pängkxo nga fìtsengmì, ha plltxe nìNa'vi ko!")

@tskxekengsiyu.event
async def on_message(message):    
        # If message is in-server
        if message.guild:
                if not message.content.startswith("!"):
                        # If message is in guild and isn't from the bot.
                        if len(message.content) >= 5 and message.author.id != 519188181426503718:
                                user = message.author
                                currentRole = user.top_role
                                userRoles = user.roles
                                isMod = False
                                userMessageCount = 0
                                fileName = 'users/' + str(user.id) + '.tsk'
                                
                                ## Check if author.top_role is moderator.
                                if currentRole.name in modRoleNames:
                                        isMod = True
            
                                ## Assigns correct role to currentRole if mod.
                                if isMod:
                                        for role in userRoles:
                                                if role.name not in modRoleNames:
                                                        currentRole = role

                                ## Updates the user profile.
                                if not os.path.exists(fileName):
                                      fh = open(fileName, 'w')
                                      fh.write(str(userMessageCount + 1) + "\n")
                                      fh.write(user.name)
                                      fh.close()
                                else:
                                        fh = open(fileName, "r")
                                        strMessageCount = fh.readlines(1)
                                        userMessageCount = int(strMessageCount[0])
                                        fh.close()
                                        fh = open(fileName, "w")
                                        fh.write(str(userMessageCount + 1) + "\n")
                                        fh.write(user.name)
                                        fh.close()

                                await roleUpdate(userMessageCount, currentRole, message, user)
                                
        elif message.author.id != 519188181426503718:
                # If a user DMs the bot.
                if message.author.dm_channel is None:
                        await message.author.create_dm()
                await message.author.dm_channel.send("Ftang nga! Ke nerìn 'upxaret ngeyä fìtsengmì!")
       
        await tskxekengsiyu.process_commands(message)
        
## Quit command
@tskxekengsiyu.command(name='ftang')
async def botquit(ctx):
        user = ctx.message.author
        if user.top_role.name == "Olo'eyktan":
                await ctx.send("Herum. Hayalovay!")
                await tskxekengsiyu.close()
                await Tskxekengsiyu.close()
                quit()

## Version
@tskxekengsiyu.command(name='srey')
async def version(ctx):
        displayversion = ["Srey: ", versionnumber]
        await ctx.send(''.join(displayversion))

## User message count
@tskxekengsiyu.command(name='yì')
async def messages(ctx, user: discord.Member):
        fileName = 'users/' + str(user.id) + '.tsk'
        fh = open(fileName, "r")
        fileContents = fh.readlines(1)
        strippedContents = fileContents[0].strip("\n")
        fh.close()
        i = 0
        for role in activeRoleThresholds:
                if int(fileContents[0]) >= activeRoleThresholds[i]:
                        toNextLevel = activeRoleThresholds[i - 1] - int(fileContents[0])
                        break
                elif int(fileContents[0]) <= 16:
                        toNextLevel = 16 - int(fileContents[0])
                        break
                i += 1
        output1 = wordify(str(oct(int(strippedContents)))[2:])
        output2 = wordify(str(oct(toNextLevel))[2:])
        embed=discord.Embed(color=0x3154cc, title=user.name, description="Lu tsatuteru **" + output1 + " 'upxare**. Kin pol **" + output2 + " 'upxareti** fte slivu " + activeRoleNames[i - 1])
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

## Add QOTD
@tskxekengsiyu.command(name='ngop')
async def qotd(ctx, question, date):
        fileName = 'qotd/' + str(date) + '.tsk'
        #print(fileName)
        if not os.path.exists(fileName):
                print("Trying to create...")
                fh = open(fileName, "w")
                fh.write(str(question))
                fh.close()
                print("Created.")
                await ctx.send("Lu hasey.")
        else:
                await ctx.send("Fìtìpawm mi fkeytok!")

@messages.error
async def info_error(ctx, error):
        if isinstance(error, commands.CommandError):
                await ctx.send("Srake ngal tstxoti aeyawr sìmar?")

# Replace token with your bot's token
tskxekengsiyu.run("private key")
