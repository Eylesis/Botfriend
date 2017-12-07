import json
import util_functions
from discord.ext import commands
import os

botToken = os.environ.get('botToken')
description = '''Botfriend Configuration: Serious >:|'''

startup_extensions = ["weather", "GameTime"]

bot = commands.Bot(command_prefix='*', description=description)

with open('settings.json', encoding="utf8") as settings_data:
    Settings = json.load(settings_data)

@bot.event
async def on_ready():
    print('Logged in as {}:{}'.format(bot.user.name, bot.user.id))
    print('----------')
    if "prefix" in Settings:
        bot.command_prefix = commands.when_mentioned_or(Settings["prefix"])
    

@bot.command()
async def prefix(new_prefix : str):
    """Changes the prefix."""
    if new_prefix != " ":
        Settings["prefix"] = new_prefix
        bot.command_prefix = commands.when_mentioned_or(Settings["prefix"])
        util_functions.saveSettings(Settings)
    await bot.say('Prefix has been set to `{}`'.format(Settings["prefix"]))

@bot.command()
async def load(extension_name : str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}:```".format(type(e).__name__, str(e)))
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
            exc = '{} : {}'. format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    bot.run(botToken)
    
