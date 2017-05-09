import discord
import asyncio
import json
import re
import random
from discord.ext.commands import Bot
from discord.ext import commands
my_bot = Bot(command_prefix=commands.when_mentioned_or("*"))

with open ('Beastiary.json', encoding="utf8") as json_data:
    BeastiaryMaster = json.load(json_data)
print("There are {0} monsters indexed.".format(len(BeastiaryMaster)))


with open('Alchemy.json', encoding="utf8") as json_data:
    AlchemyMaterialsMaster = json.load(json_data)

    for i in range(len(AlchemyMaterialsMaster)):    
        print(("{0}: {1}".format(i+1, AlchemyMaterialsMaster[i]['name'])))

with open('AlchemyTables.json', encoding="utf8") as json_data:
    AlchemyTableMaster = json.load(json_data)

    for i in range(len(AlchemyTableMaster)):    
        print(("{0}: {1}".format(i+1, AlchemyTableMaster[i]['name'])))

@my_bot.event
async def on_command_error(error, ctx):
    if isinstance(error, discord.ext.commands.CommandNotFound):
        return

@my_bot.event
async def on_read():
    print("Client logged in")

@my_bot.command()
async def prefix(newPref: str):
    if newPref != " ":
        my_bot.command_prefix = commands.when_mentioned_or(newPref)
        return await my_bot.say("New Prefix `{0}` set!".format(newPref))
    else:
        return await my_bot.say("New Prefix cannot be `{0}`.".format(newPref))

@my_bot.command()
async def hi():
    return await my_bot.say("Greetings! I am Eramir Melchor!")

@my_bot.event
async def on_message(message):
    if message.content.startswith("What are we fighting today, Botfriend?"):
        randomMonster = random.randrange(0,len(BeastiaryMaster))
        await my_bot.send_message(message.channel, "Let's fight a {name}.".format(name=BeastiaryMaster[randomMonster]['name']))
    return await my_bot.process_commands(message)
    

@my_bot.command(pass_context=True)
async def table(ctx, tableName: str):
    author = ctx.message.author
    i = 0
    for o in (range(len(AlchemyTableMaster))):
        match = re.search(tableName, AlchemyTableMaster[o]['name'], re.IGNORECASE)

        if match:
            i = o
            break

    output = ""
    for n in range(2,13):
        if (AlchemyTableMaster[i]['subgroup'][n-2] == ""):
            output += "{0} {1}\n".format(n, AlchemyTableMaster[i]['ingredients'][n-2], AlchemyTableMaster[i]['subgroup'][n-2])
        else:
            output += "{0} {1} (*{2}*)\n".format(n, AlchemyTableMaster[i]['ingredients'][n-2], AlchemyTableMaster[i]['subgroup'][n-2])

    em = discord.Embed(title="{name} Ingredients".format(**AlchemyTableMaster[i]), description=output)
    em.set_footer(text="requested by {user}".format(user=author.name), icon_url=author.avatar_url)
    await my_bot.say(embed=em)
    return await my_bot.delete_message(ctx.message)
    

@my_bot.command(pass_context=True)
async def material(ctx, name: str):
    author = ctx.message.author
    i = 0
    for o in range(len(AlchemyMaterialsMaster)):
        match = re.search(name, AlchemyMaterialsMaster[o]['name'], re.IGNORECASE)

        if match:
            i = o
            
            break

    output = "**{name}**\n*{type}, ({location}) ({dc})*\n{details}\n\n{description}".format(**AlchemyMaterialsMaster[i])
    em = discord.Embed( title="{name}".format(**AlchemyMaterialsMaster[i]), description="*{type}, ({location}) ({dc})*\n{details}\n\n{description}".format(**AlchemyMaterialsMaster[i]))
    em.set_footer(text="requested by {user}".format(user=author.name), icon_url=author.avatar_url)
    await my_bot.say(embed=em)
    return await my_bot.delete_message(ctx.message)

my_bot.run("MjQzNDk0NzkwMzU5MDIzNjE2.CvwNvQ.lCk5xfkWCtFzle8IaqLz2ki6Et0")