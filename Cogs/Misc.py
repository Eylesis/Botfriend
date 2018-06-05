import discord
from discord.ext import commands

class Misc():
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def banana(self, ctx):
        await bot.say('Why thank you {}! I do so enjoy bananas, however I am not hungry at the moment, so I shall save this for later!'.format(ctx.message.author.mention))

def setup(bot):
    bot.add_cog(Misc(bot))