import discord
import asyncio
import json
import re
import random
import dice
import traceback
from discord.ext import commands
import os

botToken = os.environ.get('botToken')
print(botToken)
startup_extensions = ["AlchemyLookup", "BeastiaryLookup", "Misc", "DowntimeForaging"]

bot = commands.Bot(command_prefix=commands.when_mentioned_or("*"))
bot.change_status(discord.Game(name="mes"))


@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, discord.ext.commands.CommandNotFound):
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        return

@bot.event
async def on_read():
    print("Client logged in")

@bot.command()
async def prefix(newPref: str):
    if newPref != " ":
        bot.command_prefix = commands.when_mentioned_or(newPref)
        return await bot.say("New Prefix `{0}` set!".format(newPref))
    else:
        return await bot.say("New Prefix cannot be `{0}`.".format(newPref))

@bot.command()
async def hi():
    return await bot.say("Greetings! I am Botfriend!")

@bot.command(pass_context=True)
async def roll(ctx, args):
    print (args)
    return await bot.say(dice.roll(args))    

@bot.command()
async def load(extension_name : str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} loaded.".format(extension_name))

@bot.command()
async def unload(extension_name : str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await bot.say("{} unloaded.".format(extension_name))

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(botToken)
    