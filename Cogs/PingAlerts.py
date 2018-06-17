import discord
from discord.ext import commands

class PingAlerts():
    def __init__(self, bot):
        self.bot = bot
    
    async def on_message(self, message):
        searchStrings = ["(l.?v.?ls?.*?\s?)(\d{1,2}).{1,3}?(\d{1,2})"]




    @commands.command(pass_context=True)
    async def alert(self, ctx, minlevel : int, maxlevel : int):
        
        if minlevel > maxlevel:
            medlevel = maxlevel
            maxlevel = minlevel
            minlevel = medlevel
        if minlevel < 3:
            minlevel = 3
        if minlevel > 20:
            minlevel = 20
        if maxlevel < 3:
            maxlevel = 3
        if maxlevel > 20:
            maxlevel = 20
        
                   
        await self.bot.say('{} has requested a notification be sent out to all players possessing the following roles for a posted quest!: {}'
        .format(ctx.message.author.mention, roleStringGenerator(minlevel, maxlevel)))

def roleStringGenerator(_minlevel : int, _maxlevel : int):
    output = ''
    for x in range(minlevel, maxlevel+1):
        new_name = "Lvl {}".format(x)
        new_role = discord.utils.get(ctx.message.server.roles, name=new_name)
        mentionString = new_role.mention
        output += '{} '.format(mentionString)
    return output

def setup(bot):
    bot.add_cog(PingAlerts(bot))