import discord
from discord.ext import commands

class PingAlerts():
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def PingAlerts(self, ctx, minlevel : int, maxlevel : int):
        output = ''
        for x in range(minlevel, maxlevel+1):
            output += '@lvl {}'.format(x)           
        await bot.say('{} has requested a notification be sent out to all players possessing the following roles for a posted quest!: {}'
        .format(ctx.message.author.mention, output))

def setup(bot):
    bot.add_cog(PingAlerts(bot))