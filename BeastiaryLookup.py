import discord
import asyncio
import json
import re
import random
from discord.ext import commands

class BeastiaryLookup():
    def __init__(self,  bot):
        self.bot = bot
        with open('Beastiary.json', encoding="utf8") as json_data:
            self.BeastiaryMaster = json.load(json_data)
    
def setup(bot):
    bot.add_cog(BeastiaryLookup(bot))