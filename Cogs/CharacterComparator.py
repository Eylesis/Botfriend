import discord
import json
import util_functions
import os
import redisInterface
import aiohttp
from discord.ext import commands

class Comparator():
    def __init__(self, bot):
        self.bot = bot
        self.API_KEY = os.environ.get('API_KEY')
    
    @commands.command(pass_context=True)
    async def stats(self, ctx):
        UserData = self.bot.db.from_json(self.bot.db.get_val('UserData'))

        data = {}
        data['users'] = list(UserData.keys())
        data['ids'] = list(UserData.values())

        AC = {'lowName': '', 'lowAC' : 5, 'highName': '', 'highAC' : 0}
        HP = {'lowName': '', 'lowHP' : 1, 'highName': '', 'highHP' : 0}
        lowStats = {'strName' : '', 'strScore' : 3, 'dexName' : '', 'dexScore' : 3, 'conName': '', 'conScore'  : 3, 'intName': '', 'intScore'  : 3, 'wisName': '', 'wisScore'  : 3, 'chaName': '', 'chaScore'  : 3}
        totalChars = 0

        async with aiohttp.ClientSession() as session:
            async with session.post('https://avrae.io/api/bulkcharacter', 
                data=json.dumps(data), 
                headers={"Authorization": self.API_KEY, "Content-Type": "application/json"}) as resp:
                    respData = await resp.json()

        for users, characters in respData.items():
            totalChars += 1
            print(characters['stat_cvars']['name'] + " : " + characters['armor']) 
            print(characters['stat_cvars']['strength'] "," + characters['stat_cvars']['dexterity'] "," + characters['stat_cvars']['constitution'] "," + characters['stat_cvars']['intelligence'] "," + characters['stat_cvars']['wisdom'] "," + characters['stat_cvars']['charisma'])
            if characters['armor'] < AC['lowAC']:
                AC['lowAC'] = characters['armor']
                AC['lowName'] = characters['stat_cvars']['name']
            if characters['armor'] > AC['highAC']:
                AC['highAC'] = characters['armor']
                AC['highName'] = characters['stat_cvars']['name']
            if characters['stat_cvars']['hp'] < HP['lowHP']:
                HP['lowHP'] = characters['stat_cvars']['hp']
                HP['lowName'] = characters['stat_cvars']['name']
            if characters['stat_cvars']['hp'] > HP['highHP']:
                HP['highHP'] = characters['stat_cvars']['hp']
                HP['highName'] = characters['stat_cvars']['name']
            if characters['stat_cvars']['strength'] < lowStats['strScore']:
                lowStats['strScore'] = characters['stat_cvars']['strength']
                lowStats['strName'] = characters['stat_cvars']['name']
            if characters['stat_cvars']['dexterity'] < lowStats['dexScore']:
                lowStats['dexScore'] = characters['stat_cvars']['dexterity']
                lowStats['dexName'] = characters['stat_cvars']['name']
            if characters['stat_cvars']['constitution'] < lowStats['conScore']:
                lowStats['conScore'] = characters['stat_cvars']['constitution']
                lowStats['conName'] = characters['stat_cvars']['name']
            if characters['stat_cvars']['intelligence'] < lowStats['intScore']:
                lowStats['intScore'] = characters['stat_cvars']['intelligence']
                lowStats['intName'] = characters['stat_cvars']['name']
            if characters['stat_cvars']['wisdom'] < lowStats['wisScore']:
                lowStats['wisScore'] = characters['stat_cvars']['wisdom']
                lowStats['wisName'] = characters['stat_cvars']['name']
            if characters['stat_cvars']['charisma'] < lowStats['chaScore']:
                lowStats['chaScore'] = characters['stat_cvars']['charisma']
                lowStats['chaName'] = characters['stat_cvars']['name']

        embed = discord.Embed(title="Planar Marches Interesting Character Stats!", description="Here are a few interesting statistics that I can pull up from Avrae's Database for Planar Marches! If you have any other interesting statistics you'd like to see, feel free to ask!")

        embed.set_footer(text="Requested by: Eylesis", icon_url=ctx.message.author.avatar_url)
        embed.add_field(name="Total Registered Characters", value=totalChars)
        embed.add_field(name="Lowest | Highest", value="Base AC: {0[lowName]}: {0[lowAC]} | {0[highName]}: {0[highAC]} \nHP: {1[lowName]}: {1[lowHP]} | {1[highName]}: {1[highHP]}".format(AC, HP))
        embed.add_field(name="Lowest Ability Scores", value="Strength: {0[strName]}: {0[strScore]} \nDexterity: {0[dexName]}: {0[dexScore]} \nConstitution: {0[conName]}: {0[conScore]} \nIntelligence: {0[intName]}: {0[intScore]} \nWisdom: {0[wisName]}: {0[wisScore]} \nCharisma: {0[chaName]}: {0[chaScore]}".format(lowStats))

        await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(Comparator(bot))