import discord
from discord.ext import commands
import time
import datetime
import pytz

class GameTime():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def time(self, ctx):
        """Displays current game time."""
        await self.bot.say(embed=get_gametime())
        await self.bot.delete_message(ctx.message)   
    
def suffix(d):
        return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

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
    gametime = datetime.datetime.now(pytz.timezone('US/Pacific'))
        
    if gametime.hour > 12:
        timestring = "{}:{} PM on the {}{} of {}, {} DR".format(gametime.hour-12, gametime.minute, gametime.day, suffix(gametime.day),months[gametime.month-1], gametime.year - 527)
    else:
        timestring = "{}:{} AM on the {}{} of {}, {} DR".format(gametime.hour, gametime.minute, gametime.day, suffix(gametime.day),months[gametime.month-1], gametime.year - 527)
    embed = discord.Embed(title="Current time in Neverwinter",description=timestring)
    return embed


def setup(bot):
    bot.add_cog(GameTime(bot))