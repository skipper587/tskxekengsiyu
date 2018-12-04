# -*- coding: utf-8 -*-
import discord

from discord.ext.commands import Bot
from discord.ext import commands

import asyncio
import os

Tskxekengsiyu = discord.Client()  # Initialise Client
tskxekengsiyu = commands.Bot(command_prefix="!")  # Initialize client bot

versionnumber = "0.0.2"
modRoleNames = ["Eyktan","Olo'eyktan"]
activeRoleNames = ["Koaktu","Tsamsiyu","Tsamsiyunay","Taronyu","Taronyunay","Numeyu","Hapxìtu","Zìma'uyu","Ketuwong"]
activeRoleThresholds = [16384, 8192, 4096, 2048, 1024, 512, 256, 128, 64]
# localDir = os.getcwd()

@tskxekengsiyu.event
async def on_ready():
        # This will be called when the bot connects to the server
        print("Tskxekengsiyu alaksi lu.")

@tskxekengsiyu.event
async def on_message(message):
        if message.guild:
                if message.guild.id == 516003512316854287 and message.author.id != 519188181426503718:
                        user = message.author
                        currentRole = user.top_role
                        userRoles = user.roles
                        activeRoles = message.guild.roles
                        isMod = False
                        userMessageCount = 0
                        fileName = str(user.id) + '.tsk'
                        
                        ## Check if author.top_role is moderator.
                        if currentRole.name in modRoleNames:
                                isMod = True
    
                        ## Assigns correct role to currentRole if mod.
                        if isMod:
                                for role in userRoles:
                                        if role.name not in modRoleNames:
                                                currentRole = role

                        ## Functions for reading/writing the file
                        if not os.path.exists(fileName):
                              fh = open(fileName, 'w')
                              fh.write(str(userMessageCount))
                              fh.close()
                        else:
                                fh = open(fileName, "r")
                                strMessageCount = fh.read()
                                userMessageCount = int(strMessageCount)
                                print(user + ' has ' + userMessageCount + ' messages.')
                                fh.close()
                                fh = open(fileName, "w")
                                fh.write(str(userMessageCount + 1))
                                fh.close()
                                fh = open(fileName, "r")
                                print(fh.read())
                                fh.close()
        
                        ## Updates roles.
                        i = 0
                        for roles in activeRoleNames:
                                if userMessageCount >= activeRoleThresholds[i] and currentRole.name != roles:
                                        # For users with no roles.
                                        if currentRole.name == "@everyone":
                                                for role in activeRoles:
                                                        if role.name == activeRoleNames[i]:
                                                                await user.add_roles(role)
                                                                print('Added ' + role.name + ' to ' + user.display_name + '.')
                                                                await message.author.send('**Seykxel sì nitram!** Set lu ngaru txintìnit alu ' + role.name + '.')
                                                                # print('Lu hasey.')
                                                                break
                                        else:
                                                # For everyone else.
                                                await user.remove_roles(currentRole)
                                                for role in activeRoles:
                                                        if role.name == activeRoleNames[i]:
                                                                await user.add_roles(role)
                                                                print('Added ' + role.name + ' to ' + user.display_name + '.')
                                                                await message.author.send('**Seykxel sì nitram!** Set lu ngaru txintìnit alu ' + role.name + '.')
                                                                # print('Lu hasey.')
                                                                break
                                elif userMessageCount >= activeRoleThresholds[i]:
                                        print('Lu hasey.')
                                        break
                                i += 1
        else:
                # If a user DMs the bot.
                await message.author.dm_channel.send('Ftang nga! Ke nerìn \'upxaret ngeyä fìtsengmì!')
        
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
@tskxekengsiyu.command()
async def version(ctx):
        displayversion=["Version: ", versionnumber]
        await ctx.send(''.join(displayversion))

# Replace token with your bots token
tskxekengsiyu.run("NTE5MTg4MTgxNDI2NTAzNzE4.DuhCZQ.TwZGq5zzmW4yetu6MGYqBYyOdjs")
