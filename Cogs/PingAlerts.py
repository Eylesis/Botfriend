import discord
import re
from discord.ext import commands

class PingAlerts():
    def __init__(self, bot):
        self.bot = bot
    
    async def on_message(self, message):
        searchStrings = ["(l.?v.?ls?.*?\s?)(\d{1,2}).{1,3}?(\d{1,2})", "(l.?v.?ls?:.*?\s?)(\d{1,2})."]
        if message.channel.id == '404050367454773251' or message.channel.id == '404050326128164884':
            
            m = re.search(searchStrings[0], message.content)
            if m.group(0) != None:
                foundString = m
            else:
                m = re.search(searchStrings[1], message.content)
                if m.group(0) != None:
                    foundString = m

            minlevel = int(foundString.group(2))
            maxlevel = int(foundString.group(3))
            
            output = ''
            for x in range(minlevel, maxlevel+1):
                new_name = "Lvl {}".format(x)
                new_role = discord.utils.get(ctx.message.server.roles, name=new_name)
                mentionString = new_role.mention
                output += '{} '.format(mentionString)

            await self.bot.say(':arrow_up:  Quest Alert :arrow_up:\n{}'
                .format(output))
        


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
        .format(ctx.message.author.mention, roleStringGenerator(ctx, minlevel, maxlevel)))

def roleStringGenerator(ctx, _minlevel : int, _maxlevel : int):
    output = ''
    for x in range(_minlevel, _maxlevel+1):
        new_name = "Lvl {}".format(x)
        new_role = discord.utils.get(ctx.message.server.roles, name=new_name)
        mentionString = new_role.mention
        output += '{} '.format(mentionString)
    return output

def setup(bot):
    bot.add_cog(PingAlerts(bot))