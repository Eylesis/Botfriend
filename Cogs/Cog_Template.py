import discord
from discord.ext import commands

class DEFAULT():
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def DEFAULT(self, ctx):
        await bot.say('eep')

def setup(bot):
    bot.add_cog(DEFAULT(bot))