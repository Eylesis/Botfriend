import traceback
import json
import util_functions
from discord.ext import commands
import redisInterface
import sys
import re
import os
import pygsheets

botToken = os.environ.get('botToken')

description = '''Botfriend Configuration: Conversational ^-^'''

#startup_extensions = []
startup_extensions = ["Cogs.help", "Cogs.autorole", "Cogs.PingAlerts", "Cogs.Misc", "Cogs.Weather", "Cogs.CampaignTools", "Cogs.GoogleManip"]
# "Cogs.GameAlerts", "Cogs.CharacterComparator", "Cogs.Misc"
bot = commands.Bot(command_prefix='*', description=description)
bot.remove_command('help')
bot.db = redisInterface.Database()


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


@bot.command(pass_context=True, no_pm=True, hidden=True)
async def prefix(ctx, new_prefix: str):
    """Changes the prefix."""
    allowed = False
    for role in ctx.message.author.roles:
        if role.name == "Moderator":
            allowed = True
    if allowed or ctx.message.author.id == '227168575469780992':
            if new_prefix != " ":
                Settings["prefix"] = new_prefix
                bot.command_prefix = commands.when_mentioned_or(
                    Settings["prefix"])
                util_functions.saveFile(Settings, 'Settings/settings.json')
            return await bot.say('Why certainly, {0.author.mention}. I have changed the prefix to `{1}`.'.format(ctx.message, Settings["prefix"]))
    return await bot.say('Terribly sorry, but I do not recognize you as a person of authority here!')


@bot.command(pass_context=True, no_pm=True, hidden=True)
async def load(ctx, extension_name: str):
    """Loads an extension."""
    allowed = False
    for role in ctx.message.author.roles:
        if role.name == "Moderator":
            allowed = True
    if allowed or ctx.message.author.id == '227168575469780992':
        try:
            bot.load_extension(extension_name)
        except (AttributeError, ImportError) as e:
            await bot.say("Oh dear. It would appear engineering has sent up the following correspondance.```py\n{}:```".format(type(e).__name__, str(e)))
            return
        return await bot.say("Excellent choice, {0.author.mention}! `{1}` has been loaded and is ready to be ultilized.".format(ctx.message, extension_name))
    return await bot.say('Terribly sorry {0.author.mention}, but I do not recognize you as a person of authority here!'.format(ctx.message))


@bot.command(pass_context=True, no_pm=True, hidden=True)
async def unload(ctx, extension_name: str):
    """Unloads an extension."""
    for role in ctx.message.author.roles:
        if role.name == "Moderator":
            allowed = True
    if allowed or ctx.message.author.id == '227168575469780992':
        bot.unload_extension(extension_name)
        return await bot.say("Excellent choice, {0.author.mention}! `{1}` has been unloaded and stored for future use.".format(ctx.message, extension_name))
    return await bot.say('Terribly sorry {0.author.mention}, but I do not recognize you as a person of authority here!'.format(ctx.message))


@bot.event
async def on_command_error(error, ctx):
    traceback.print_exception(
        type(error), error, error.__traceback__, file=sys.stderr)

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{} : {}'. format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    print('eeeeeeeeeeeeeeeeeeeeeeeeeep')
    bot.run(botToken)
