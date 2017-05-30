import discord
import asyncio
import random
import json
import re
import dice
import shlex
from functions import parse_args_3
from functions import list_get
from discord.ext import commands

class DowntimeForaging():
    def __init__(self,  bot):
        self.bot = bot
        with open('AlchemyTables.json', encoding="utf8") as json_data:
            self.AlchemyTableMaster = json.load(json_data)
        with open('Alchemy.json', encoding="utf8") as json_data:
            self.AlchemyMaterialsMaster = json.load(json_data)
    
    def getCommonRollProcs(self, table):
        commonRollProc = []
        i = 2
        for entry in table:
            if entry == "Common Ingredient":
                commonRollProc.append(i)
            i += 1
        return commonRollProc

    def getTable(self, name):
        print("entered function")
        i = 0
        for o in (range(len(self.AlchemyTableMaster))):
            match = re.search(name, self.AlchemyTableMaster[o]['name'], re.IGNORECASE)

            if match:
                i = o
                print("matched")
                break
        print("set")
        return self.AlchemyTableMaster[i]
    
    def table_rolls(self, args):
        found = False
        table = self.getTable(args.get('biome'))
        print(table)
        commonRollProcc = self.getCommonRollProcs(table.get('ingredients'))
        tableRolls = {}
        tableRolls['table'] = []
        tableRolls['common'] = []
        for a in range(int(args.get('successes'))):
            roll = random.randint(1, 6) + random.randint(1, 6)
            for common in commonRollProcc:
                if roll == common:
                    roll = random.randint(1, 6) + random.randint(1, 6)
                    tableRolls['common'].append(roll)
                    found = True
                    break
            if found == False:
                tableRolls['table'].append(roll)
            found = False
        print(tableRolls['table'])
        print(tableRolls['common'])
        return tableRolls

    '''def roll_materials(self, args, biome):
        i = 0
        tableRolls = self.getTable(biome)
        elementaled = False
        results = {}
        for rollTable in range(int(args.get('table'))):
            if (rollTable >=2 and rollTable <=4) or (rollTable >=10 and rollTable <=12):
                elementalProc = random.randint(1,100)
                if elementalProc >= 75:
                    results.setdefault('elemental', 0)
                    results['elemental'] += 1
                    elementaled = True
            if elementaled != True:'''




    def roll_herbalism(self, args):
        herbalismSuccesses = 0
        for a in range(int(args.get('rolls'))):
            result = dice.roll(args.get('rollstring'))
            if  result.total >= 15:
                herbalismSuccesses += 1
        return herbalismSuccesses

    def construct_embed(self, args):
        em = discord.Embed(title="FORAGING IN THE {biome} BIOME".format(biome=args.get('biome')), description="desc.")
        em.add_field(name="**Days: **", value="some of these properties have certain limits...")
        return em

    def total_forage_rolls(self, args):
        days = 0
        rolls = 0

        if args.get('days'):
            days = args.get('days')[0]
            print(days)
        else:
            days = 1

        if args.get('natural')[0]:
            for a in range(int(days)):
                rolls += random.randint(1, 4)
            return rolls
        else:
            return days    

    @commands.command(pass_context=True)
    async def forage(self, ctx, biome: str, rollstring: str, *, args):
        author = ctx.message.author
        print(args)
        splitArgs = shlex.split(args)
        argArray = parse_args_3(splitArgs)
        print (argArray)
        argArray['biome'] = biome
        argArray["rolls"] = self.total_forage_rolls(argArray)
        argArray["rollstring"] = rollstring
        print(argArray.get('rollstring'))
        argArray['successes'] = self.roll_herbalism(argArray)
        tableRollsResults = self.table_rolls(argArray)
        roll_materials(tableRollsResults, argArray['biome'])
        em = self.construct_embed(argArray)
        em.set_footer(text="requested by {user}".format(user=author.name), icon_url=author.avatar_url)
        await self.bot.say(embed=em)

   

def setup(bot):
    bot.add_cog(DowntimeForaging(bot))