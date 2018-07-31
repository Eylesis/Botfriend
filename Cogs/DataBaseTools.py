import discord
from discord.ext import commands

class DataBaseTools():
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True, hidden=True)
    async def getVal(self, ctx, key):
        return await self.bot.say(self.bot.db.get_val(key))

    @commands.command(pass_context=True, hidden=True)
    async def setVal(self, ctx, key, *, value):
        self.bot.db.set_val(key, value)
        return await self.bot.say(self.bot.db.get_val(key))

def setup(bot):
    bot.add_cog(DataBaseTools(bot))