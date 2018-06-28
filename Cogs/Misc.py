import discord
from discord.ext import commands

class Misc():
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def banana(self, ctx):
        await self.bot.delete_message(ctx.message)
        await self.bot.say('Why thank you {}! I do so enjoy bananas, however I am not hungry at the moment, so I shall save this for later!'.format(ctx.message.author.mention))

    @commands.command(pass_context=True, hidden=True)
    async def chanSay(self, ctx, channel: str, *, message: str):
        if ctx.message.author.id == '227168575469780992':
            await self.bot.send_message(self.bot.get_channel(channel), message)

def setup(bot):
    bot.add_cog(Misc(bot))
