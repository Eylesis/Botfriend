import discord
from Cogs.GameTime import get_gametime
from discord.ext import tasks, commands
import time
from datetime import date,timedelta,date
import pytz
import util_functions

class GameClock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @tasks.loop(minutes=1.0)
    async def updateTime:
        with open('Settings/settings.json', encoding="utf8") as settings_data:
            Settings = json.load(settings_data)
        
        gametime = get_gametime()
        return await self.bot.get_channel(Settings['gametime_channel']).edit(name=gametime)
    


    @commands.group(pass_context=True)
    async def cmd(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid sub command passed...')

def setup(bot):
    bot.add_cog(GameClock(bot))
