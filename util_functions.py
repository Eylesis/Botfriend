import json
import re
import discord
def saveFile(Settings : dict, filename : str):
    settings_file = open(filename, "w")
    settings_file.write(json.dumps(Settings, ensure_ascii=False))
    settings_file.close()

def discord_trim(str):
    result = []
    trimLen = 0
    lastLen = 0
    while trimLen <= len(str):
        trimLen += 1999
        result.append(str[lastLen:trimLen])
        lastLen += 1999
    return result    

def fix_mentions(bot, string):
    mentions = re.findall('<[@!]+[0-9]+>', string)
    for mention in mentions:
        string = string.replace(mention, "@\u200b" + str(
            discord.utils.get(bot.get_all_members(), id=re.sub('[<>@!]', '', mention))))
    return string.replace('@', '@\u200b')