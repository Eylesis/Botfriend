import discord
import redisInterface
import re
from discord.ext import commands

class CustomItems():
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(pass_context=True)
    async def item(self, ctx):
       if ctx.invoked_subcommand is None:
        await bot.say('Invalid item command passed...')
    
    @item.command(pass_context=True)
    async def add(self,ctx, item_info : str):
        if self.bot.db.get_val('customItems') == '':
            to_db = {}
        else:
            to_db = self.bot.db.from_json(self.bot.db.get_val('customItems'))
        
        item_data = re.match('(.*?\n)(.*?),(.*?),(.*?)\n(.*?)\s*---\s*(.*?)-\s*(.*?)', item_info)

        if item_data.group(1) not in to_db:
            to_db[item_data.group(1)] = {"type": item_data.group(2), "desc" : item_data.group(3)}
        else:
            await bot.say("That item exists already.")

        


def setup(bot):
    bot.add_cog(CustomItems(bot))