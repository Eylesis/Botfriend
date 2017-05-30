import discord
import asyncio
import json
import re
import random
import shlex
from functions import parse_args_3
from discord.ext import commands

class AlchemyLookup():
    def __init__(self,  bot):
        self.bot = bot
        with open('AlchemyTables.json', encoding="utf8") as json_data:
            self.AlchemyTableMaster = json.load(json_data)
        with open('Alchemy.json', encoding="utf8") as json_data:
            self.AlchemyMaterialsMaster = json.load(json_data)
    
    @commands.command(pass_context=True)
    async def material(self, ctx, name: str, *, args):
        author = ctx.message.author
        splitArgs = shlex.split(args)
        argArray = parse_args_3(splitArgs)

        print(author.name)
        i = 0
        for o in (range(len(self.AlchemyMaterialsMaster))):
            match = re.search(name, self.AlchemyMaterialsMaster[o]['name'], re.IGNORECASE)

            if match:
                i = o
                break

        output = "**{name}**\n*{type}, ({location}) ({dc})*\n{details}\n\n{description}".format(**self.AlchemyMaterialsMaster[i])
        em = discord.Embed( title="{name}".format(**self.AlchemyMaterialsMaster[i]), description="*{type}, ({location}) ({dc})*\n{details}\n\n{description}".format(**self.AlchemyMaterialsMaster[i]))
        em.set_footer(text="requested by {user}".format(user=author.name), icon_url=author.avatar_url)
        if argArray.get("raw"):
            await self.bot.say(output)
        else: 
            await self.bot.say(embed=em)
        await self.bot.delete_message(ctx.message)


    @commands.command(pass_context=True)
    async def table(self, ctx, tableName: str):
        author = ctx.message.author
        print(author.name)
        i = 0
        for o in (range(len(self.AlchemyTableMaster))):
            match = re.search(tableName, self.AlchemyTableMaster[o]['name'], re.IGNORECASE)
            if match:
                i = o
                break

        output = ""
        for n in range(2,13):
            if (self.AlchemyTableMaster[i]['subgroup'][n-2] == ""):
                output += "{0} {1}\n".format(n, self.AlchemyTableMaster[i]['ingredients'][n-2], self.AlchemyTableMaster[i]['subgroup'][n-2])
            else:
                output += "{0} {1} (*{2}*)\n".format(n, self.AlchemyTableMaster[i]['ingredients'][n-2], self.AlchemyTableMaster[i]['subgroup'][n-2])

        em = discord.Embed(title="{name} Ingredients".format(**self.AlchemyTableMaster[i]), description=output)
        em.set_footer(text="requested by {user}".format(user=author.name), icon_url=author.avatar_url)
        await self.bot.say(embed=em)
        await self.bot.delete_message(ctx.message)

def setup(bot):
    bot.add_cog(AlchemyLookup(bot))