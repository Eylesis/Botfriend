import discord
import redisInterface
from discord.ext import commands

class Misc():
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def banana(self, ctx):
        bananaStash = self.bot.db.get_val('bananaStash')
        if bananaStash = '':
            await self.bot.say('Why thank you {}! This banana is the first in my latest stash! I shall store it carefully.'.format(ctx.message.author.mention))
            self.bot.db.set_val('bananaStash', 1)
        else:
            bananaStash += 1
            self.bot.db.set_val('bananaStash', bananaStash)
            await self.bot.say('Why thank you {}! I do so enjoy bananas, however I am not hungry at the moment, so I shall save this for later! My stash has {} bananas in it, can you believe it?'
            .format(ctx.message.author.mention, bananaStash))
        return await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True, hidden=True)
    async def chanSay(self, ctx, channel: str, *, message: str):
        if ctx.message.author.id == '227168575469780992':
            await self.bot.send_message(self.bot.get_channel(channel), message)

def setup(bot):
    bot.add_cog(Misc(bot))
