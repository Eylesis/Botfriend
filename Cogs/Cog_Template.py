import discord
from discord.ext import commands

class DEFAULT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def cmd(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid sub command passed...')

def setup(bot):
    bot.add_cog(DEFAULT(bot))
