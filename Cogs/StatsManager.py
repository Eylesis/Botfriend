import discord
from discord.ext import commands

class StatsManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
        async def cleanup(self, ctx):
        allowed = False
        for role in ctx.author.roles:
            if role.name == "Admin" or role.name == "Governor":
                allowed = True
        if allowed or ctx.author.id == 227168575469780992:
        
        async for message in channel.history():
            async for reaction in message.reactions():
                async for user in reaction.users():
       

def setup(bot):
    bot.add_cog(StatsManager(bot))
