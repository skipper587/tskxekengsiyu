# -*- coding: utf-8 -*-
import discord

from discord.ext.commands import Bot
from discord.ext import commands
from datetime import timedelta

import asyncio
import time

Tskxekengsiyu = discord.Client()  # Initialise Client
tskxekengsiyu = commands.Bot(command_prefix="!")  # Initialize client bot

versionnumber="0.0.1"
timezone=timedelta(hours=-8)
modRoleNames = ["Eyktan","Olo'eyktan"]
# activeRoles = {"Ketuwong":64,"Zìma'uyu":128,"Hapxìtu":256,"Numeyu":512,"Taronyunay":1024,"Taronyu":2048,"Tsamsiyunay":4096,"Tsamsiyu":8192}
activeRoleNames = ["Tsamsiyu","Tsamsiyunay","Taronyu","Taronyunay","Numeyu","Hapxìtu","Zìma'uyu","Ketuwong"]
activeRoleThresholds = [8192, 4096, 2048, 1024, 512, 256, 128, 64]

@tskxekengsiyu.event
async def on_ready():
    # This will be called when the bot connects to the server
    print("Tskxekengsiyu alaksi lu.")

@tskxekengsiyu.event
async def on_message():
    author = ctx.message.author
    currentRole = ctx.member.top_role
    userRoles = ctx.member.roles
    isMod = False
    userMesssageCount = 0
    
    ## Check if toprole is moderator.
    for role in modRoleNames:
        if role == currentRole:
            isMod = True
    
    ## Assigns correct role to currentRole if mod.
    if isMod:
        for role in activeRoleNames:
            if role not in ["everyone", "Eyktan", "Olo'eyktan"]:
                currentRole = role

    ## Functions for reading/writing our file

    ## Updates roles if applicable.
    i = 0
    for role in activeRoleNames:
        if userMessageCount >= activeRoleThresholds[i] and currentRole != role:
            remove_roles(author, currentRole)
            add_roles(author, activeRoleNames[i])
            # Can end here if triggers.
            break
        i += 1
             

## Quit command
@tskxekengsiyu.command(name='ftangnga')
async def botquit(ctx):
    await ctx.send("Herum.")
    await tseayu.close()
    await Tseayu.close()
    quit()

## Version
@tskxekengsiyu.command()
async def version(ctx):
    displayversion=["Version: ", versionnumber]
    await ctx.send(''.join(displayversion))

## Timestamp Test
@tskxekengsiyu.command()
async def time(ctx):
    shift=ctx.message.created_at+timezone
    await ctx.send("Date is %s PST" % shift.strftime("%Y-%m-%d %H:%M:%S"))

## Prints a list of all roles by category.
@tskxekengsiyu.command()
async def rolelist(ctx):
    trainingRoleNames = ["Ketuwong","Zìma'uyu","Hapxìtu","Taronyunay","Taronyu","Tsamsiyunay","Tsamsiyu"]
    modRoleNames = ["Eyktan","Olo'eyktan"]
    trainingRoles = []
    modRoles = []
    teacherRoles = []
    extraRoles = []
    allRoles=ctx.guild.roles
    for role in allRoles:
        if role.name in learningRoleNames:
            learningRoles.append(role)
        elif role.name in modRoleNames:
            modRoles.append(role)
        elif role.name in teacherRoleNames:
            teacherRoles.append(role)
        elif role.name == "'Eylan":
            eylanRole = role
        elif role.name != "@everyone":
            extraRoles.append(role)
    await ctx.send("O_O Learning Roles: ")
    for role in learningRoles:
        await ctx.send(role.name)
    await ctx.send("O_O Teaching Roles: ")
    for role in teacherRoles:
        await ctx.send(role.name)
    await ctx.send("O_O Moderation Roles: ")
    for role in modRoles:
        await ctx.send(role.name)
    await ctx.send("O_O Eylan Role: ")
    await ctx.send(eylanRole)
    await ctx.send("O_O Extra Roles: ")
    for role in extraRoles:
        await ctx.send(role.name)

# Replace token with your bots token
tskxekengsiyu.run("NTE5MTg4MTgxNDI2NTAzNzE4.Dubrug.QmdWE-cquRlkwk1BuEMGMiPKpfY")
