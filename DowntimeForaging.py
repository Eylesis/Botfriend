import discord
from discord.ext import commands

class DowntimeForaging():
    def __init__(self,  bot):
        self.bot = bot
        with open('AlchemyTables.json', encoding="utf8") as json_data:
            self.AlchemyTableMaster = json.load(json_data)
        with open('Alchemy.json', encoding="utf8") as json_data:
            self.AlchemyMaterialsMaster = json.load(json_data)
    
    @commands.command()
    async def forage(self, ctx):
    


def setup(bot):
    bot.add_cog(AlchemyLookup(bot))