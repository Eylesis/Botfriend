import traceback
import json
import util_functions
import discord
from discord.ext import commands
import redisInterface
import sys
import re
import os

botToken = os.environ.get('botToken')
description = '''Botfriend Configuration: Conversational ^-^'''

#startup_extensions = []
startup_extensions = ["Cogs.Misc", "Cogs.Weather", "Cogs.GameTime"]
# "Cogs.GameAlerts", "Cogs.CharacterComparator", "Cogs.Misc"
bot = commands.Bot(command_prefix='*', description=description)
bot.remove_command('help')
bot.db = redisInterface.Database()
bot.training_data = []
bot.STATE_SIZE = 2

with open('Settings/settings.json', encoding="utf8") as settings_data:
    Settings = json.load(settings_data)

@bot.event
async def on_message(message):
    await bot.process_commands(message)

@bot.event
async def on_ready():
    print('Logged in as {}:{}'.format(bot.user.name, bot.user.id))
    print('----------')
    if "prefix" in Settings:
        bot.command_prefix = commands.when_mentioned_or(Settings["prefix"])

@bot.command(hidden=True)
async def chanSay(ctx, channel, *, message: str):
    if ctx.author.id == 227168575469780992:
        foundChannel = await bot.fetch_channel(channel)
        return await foundChannel.send(message)

def check_perm(ctx):
    if "Weavekeepers" in ctx.author.roles:
        return True
    return False


@bot.command(no_pm=True, hidden=True)
async def prefix(ctx, new_prefix: str):
    """Changes the prefix."""
    if check_perm(ctx) or ctx.author.id == 227168575469780992:
            if new_prefix != " ":
                Settings["prefix"] = new_prefix
                bot.command_prefix = commands.when_mentioned_or(
                    Settings["prefix"])
                util_functions.saveFile(Settings, 'Settings/settings.json')
            return await bot.say('Why certainly, {0.mention}. I have changed the prefix to `{1}`.'.format(ctx.author, Settings["prefix"]))
    return await bot.say('Terribly sorry {0.mention}, but I do not recognize you as a person of authority here!'.format(ctx.author))

@bot.command(no_pm=True, hidden=True)
async def gametime(ctx):
    """Sets the GameTime Default Channel."""
    if check_perm(ctx) or ctx.author.id == 227168575469780992:
        Settings["gametime_channel"] = ctx.channel.id
        util_functions.saveFile(Settings, 'Settings/settings.json')

@bot.event
async def on_command_error(ctx, error):
    traceback.print_exception(
        type(error), error, error.__traceback__, file=sys.stderr)

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{} : {}'. format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    bot.run(botToken)
