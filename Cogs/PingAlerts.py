import discord
from discord.ext import commands

class PingAlerts():
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def PingAlerts(self, ctx, minlevel : int, maxlevel : int):
        output = ''
        for x in range(minlevel, maxlevel+1):
            new_name = "Lvl {}".format(x)
            new_role = discord.utils.get(ctx.message.server.roles, name=new_name)
            mentionString = new_role.mention
            output += '{} '.format(mentionString)           
        await self.bot.say('{} has requested a notification be sent out to all players possessing the following roles for a posted quest!: {}'
        .format(ctx.message.author.mention, output))

def setup(bot):
    bot.add_cog(PingAlerts(bot))