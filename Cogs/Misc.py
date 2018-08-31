import discord
import redisInterface
import datetime
import re
from discord.ext import commands

class Misc():
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def banana(self, ctx):
        bananaStash = int(self.bot.db.get_val('bananaStash', 0))
        
        if bananaStash == 68:
            bananaStash = 0
            await self.bot.say('!69')
                
        if bananaStash == 0:
            await self.bot.say('Why thank you {}! This banana is the first in my latest stash! I shall store it carefully.'.format(ctx.message.author.mention))
            self.bot.db.set_val('bananaStash', '1')
        else:
            bananaStash += 1
            self.bot.db.set_val('bananaStash', str(bananaStash))
            await self.bot.say('Why thank you {}! I do so enjoy bananas, however I am not hungry at the moment, so I shall save this for later! My stash has {} bananas in it, can you believe it?'
            .format(ctx.message.author.mention, bananaStash))
        return await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True, hidden=True)
    async def chanSay(self, ctx, channel: str, *, message: str):
        if ctx.message.author.id == '227168575469780992':
            await self.bot.send_message(self.bot.get_channel(channel), message)

    @commands.command(pass_context=True)
    async def ustime(self, ctx, datestring : str, timestring : str):
        date_data = re.match('(\d{1,2})\D(\d{1,2})\D.*', datestring)        
        if date_data == None:
            return await self.bot.say("I couldn't make sense of your requested date, {}. I am terribly sorry but could you try to format it as such: '1/01'.".format(ctx.message.author.mention))
        
        return await self.bot.say(date_data[1])

def setup(bot):
    bot.add_cog(Misc(bot))
