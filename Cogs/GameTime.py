import discord
from discord.ext import commands
import time
import datetime
import pytz

class GameTime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def time(self, ctx):
        """Displays current game time."""
        locationName = self.bot.db.get_val("ServerInfo", "")
        print(type(locationName))
        print(locationName['CityName'])
        embed = discord.Embed(title="Current time in {}".format(locationName['CityName']),description=get_gametime())
        await ctx.send(embed=embed)
        await ctx.message.delete_message()   
    
def suffix(d):
        return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

def get_rawtime():
        return datetime.datetime.now(pytz.timezone('UTC'))

def get_gametime():
    months = [
        "Hammer",
        "Alturiak",
        "Ches",
        "Tarsakh",
        "Mirtul",
        "Kythorn",
        "Flamerule",
        "Eleasis",
        "Eleint",
        "Marpenoth",
        "Uktar",
        "Nightal"]

    aDate = datetime(2020, 10, 18, tzinfo=pytz.timezone('UTC'))
    bDate = datetime.now(pytz.timezone('UTC'))
    delta = bDate - aDate

    gametime = datetime(2020, 10, 18, bDate.hour, bDate.minute, bDate.second) + timedelta(days=delta.days*3) + (timedelta(days=(bDate.hour//8-2)))

    if gametime.hour == 0:
        gametime_hour = 12
        time_decor = "AM"
    else:
        gametime_hour = gametime.hour-12 if gametime.hour > 12 else gametime.hour
        time_decor = "PM" if gametime.hour > 12 else "AM"
    
    gametime_minute = "0{}".format(gametime.minute) if gametime.minute < 10 else gametime.minute

    return "{}:{} {} UTC | {}{} of {}".format(gametime_hour, gametime_minute, time_decor, gametime.day, suffix(gametime.day), months[gametime.month-1])


def setup(bot):
    bot.add_cog(GameTime(bot))
