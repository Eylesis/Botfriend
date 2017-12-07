import json
import util_functions
from discord.ext import commands
import redisInterface
import re
import os

botToken = os.environ.get('botToken')
description = '''Botfriend Configuration: Serious >:|'''

startup_extensions = ["weather", "GameTime", "xplog"]

bot = commands.Bot(command_prefix='*', description=description)
bot.db = redisInterface.Database()

with open('settings.json', encoding="utf8") as settings_data:
    Settings = json.load(settings_data)

@bot.event
async def on_ready():
    print('Logged in as {}:{}'.format(bot.user.name, bot.user.id))
    print('----------')
    if "prefix" in Settings:
        bot.command_prefix = commands.when_mentioned_or(Settings["prefix"])
    
@bot.event
async def on_message(message):
    if message.channel.id == "379420083107397643":
        players = re.findall("<@!.*?>.*?\(.*?\)", message.content)
        event = re.match(r"\).*?\(", message.content[::-1]).group(0)[::-1]
        experience = int((re.search("\d+", re.search(r"\+.*?\d+", message.content).group(0)).group(0)))
        
        if bot.db.get_val('xp_log') == '':
            to_db = {}
        else:
            to_db = bot.db.from_json(bot.db.get_val('xp_log'))
        for player in players:
            name = player[player.find('!')+1:player.find('>')]
            character = player[player.find('(')+1: player.find(')')]
            
            if name not in to_db.keys():
                to_db[name] = {}
            if character not in to_db[name].keys():
                to_db[name][character] = {}
            if 'events' not in to_db[name][character].keys():
                to_db[name][character]['events'] = {}
            if 'total' not in to_db[name][character].keys():
                to_db[name][character]['total'] = 0    
            to_db[name][character]['events'][event] = experience
            to_db[name][character]['total'] += experience    
        bot.db.set_val('xp_log', bot.db.to_json(to_db))
    await bot.process_commands(message)

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
    
