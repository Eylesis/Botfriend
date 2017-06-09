import discord
import asyncio
import random
import json
import re
import dice
import shlex
import math
from functions import parse_args_3
from functions import list_get
from discord.ext import commands

class DowntimeForaging():
    def __init__(self,  bot):
        self.bot = bot
        with open('AlchemyTables.json', encoding="utf8") as json_data:
            self.AlchemyTableMaster = json.load(json_data)
    
    def roundup(self, x):
        return int(math.ceil(x / 10.0)) * 10

    def Get_Table(self, name):
        i = 0
        usingTable = []
        for o in (range(len(self.AlchemyTableMaster))):
            match = re.search(name, self.AlchemyTableMaster[o]['name'], re.IGNORECASE)

            if match:
                i = o
                break
        for materials in self.AlchemyTableMaster[i]['ingredients']: 
            usingTable.append(materials)
        return usingTable        
    
    def Get_Common_List(self, table):
        commonList = []
        i = 0
        for material in table:
            if material == "Common Ingredient":
                commonList.append(i)
            i += 1
        return commonList

    def Roll_Herbalism(self, args, outCol):
        herbalism = dice.roll(args.get('rollstring'))
        args['herbalismRolls'].append(re.sub(r"\s+", " ", "{0}: {1}".format(herbalism.rolled, herbalism.total)))
        if herbalism.total >= 15:
            self.Roll_Entry(args, outCol)
        else:
            return

    def Roll_Entry(self, args, outCol):
        entryQuantity = dice.roll('1d4').total
        if args.get('natural'):
            entryQuantity *= 2
        tableRoll = dice.roll('2d6').total
        table = args['usingTable']
        if ((tableRoll >= 2 and tableRoll <= 4) or (tableRoll >= 10 and tableRoll <= 12)):
            if (dice.roll('1d100').total >= 75):
                args['quantities'].append(entryQuantity)
                args['materials'].append('Elemental Water')
                if 'Elemental Water' in outCol:
                    outCol['Elemental Water'] += entryQuantity
                else:
                    outCol['Elemental Water'] = entryQuantity
                return
        foundCommon = False
        for commons in args['commonList']:
            if (tableRoll-2 == commons):
                foundCommon = True
                break
        if (foundCommon):
            tableRoll = dice.roll('2d6rr7').total
            while tableRoll == 7:
                tableRoll = dice.roll('2d6rr7').total
            selectedMat = self.Get_Table('common')[tableRoll-2]
            args['quantities'].append(entryQuantity)
            args['materials'].append(selectedMat)
            if selectedMat in outCol:
                outCol[selectedMat] += entryQuantity
            else:
                outCol[selectedMat] = entryQuantity
            return
        else:
            selectedMat = args['usingTable'][tableRoll-2]
            args['quantities'].append(entryQuantity)
            args['materials'].append(selectedMat)
            if selectedMat in outCol:
                outCol[selectedMat] += entryQuantity
            else:
                outCol[selectedMat] = entryQuantity
            return

    def Construct_Failure(self, args, author):
        outRoll = ''
        for entries in args['herbalismRolls']:
            outRoll += "{0}\n".format(entries)
        embed=discord.Embed(title="Foraging Results", description="{character} has foraged in the {biome}! Unfortunately, they didn't find anything...".format(**args))
        embed.add_field(name="Roll", value=outRoll, inline=True)
        embed.set_footer(text="requested by {user}".format(user=author.name), icon_url=author.avatar_url) 
        return embed

    def Construct_Log(self, args, outCol, author):
        logOutput = "```{0} ({1}):".format(author.mention, author.display_name)
        for key, value in outCol.items():
            logOutput += " +{0} {1},".format(value, key)
        logOutput = logOutput[:-1]
        logOutput += ' (Foraging)```'
        args['logOutput'] = logOutput[3:-3]
        embed=discord.Embed(title="Log Output", description=logOutput)
        return embed
    
    def Construct_Output(self, args, author, startRange, endRange):
        
        outQuantity = ''
        outMaterial = ''
        outRoll = ''
        for entries in args['quantities'][startRange:endRange]:
            outQuantity += "{0}\n".format(entries)
        for entries in args['materials'][startRange:endRange]:
            outMaterial += "{0}\n".format(entries)
        for entries in args['herbalismRolls'][startRange:endRange]:
            outRoll += "{0}\n".format(entries)

        embed=discord.Embed(title="Foraging Results", description="{character} has foraged in the {biome} for {days} days! They managed to find the following:".format(**args))
        embed.add_field(name="Quantity", value=outQuantity, inline=True)
        embed.add_field(name="Material", value=outMaterial, inline=True)
        embed.add_field(name="Roll", value=outRoll, inline=True)
        
        embed.set_footer(text="requested by {user}".format(user=author.name), icon_url=author.avatar_url)
        return embed

    async def reaction_menu(self, args, author, message, logMessage):
        toggle = False
        page = 0
        pgEnd = 0
        maxPage = self.roundup(len(args['quantities'])) / 10
        print(maxPage)
        await self.bot.add_reaction(message, '\U000025c0')
        await self.bot.add_reaction(message, '\U000025b6')
        await self.bot.add_reaction(message, '\U0001f4cb')
        await self.bot.add_reaction(message, '\U0001f6ab')
        while toggle==False:
            res = await self.bot.wait_for_reaction(message=message, user=author)
            print('start: {0}'.format(page))
            if res.reaction.emoji == '\U0001f4cb':
                print ('clipboard')
                logChannel = self.bot.get_channel('123208456650883072')
                await self.bot.send_message(logChannel, args['logOutput'])
                await self.bot.clear_reactions(message)
                toggle = True
            elif res.reaction.emoji == '\U0001f6ab':
                print ('cancel')
                await self.bot.clear_reactions(message)
                toggle = True
            elif res.reaction.emoji == '\U000025c0' and page > 0:
                print ('leftArrow')
                page -= 1
                pgEnd = int(page*10)+10
                logMessage = await self.bot.edit_message(logMessage, embed=self.Construct_Output(args, author, (page*10), pgEnd))
                await self.bot.remove_reaction(message, '\U000025c0', author)
            elif res.reaction.emoji == '\U000025b6' and page <= maxPage:
                print ('rightArrow')
                page += 1
                pgEnd = int(page*10)+10
                logMessage = await self.bot.edit_message(logMessage, embed=self.Construct_Output(args, author, (page*10), pgEnd))
                await self.bot.remove_reaction(message, '\U000025b6', author)
            else:
                print ('nope')
            print('end: {0}'.format(page))
        print ('exited')
        return

    @commands.command(pass_context=True)
    async def forage(self, ctx, biome: str, rollstring: str, *, args=None):
        author = ctx.message.author
        argArray = {}
        if args != None:
            splitArgs = shlex.split(args)
            argArray = parse_args_3(splitArgs)
        print (argArray)
        argArray['quantities'] = []
        argArray['materials'] = []
        argArray['herbalismRolls'] = []

        argArray['biome'] = biome
        argArray['character'] = author.display_name
        argArray['usingTable'] = []
        templist = self.Get_Table(biome)
        for entry in (templist):
            argArray['usingTable'].append(entry)
        templist.clear()

        argArray['commonList'] = []
        templist = self.Get_Common_List(argArray['usingTable'])
        for entry in (templist):
            argArray['commonList'].append(entry)
        templist.clear()

        argArray["rollstring"] = rollstring
        print(argArray.get('days')[0])
        collectionOutput = {}
        rollToDo = 0
        argArray['days'] = int(argArray.get('days', [1])[0])
        if argArray.get('commune'):
            for val in range(0, argArray['days']):
                rollToDo += dice.roll('1d4').total
        else:
            rollToDo = int(argArray.get('days', [1])[0])
        for val in range(0, rollToDo):
            self.Roll_Herbalism(argArray, collectionOutput)
        if not argArray['quantities']:
            await self.bot.say(embed=self.Construct_Failure(argArray, author))
        else:
            logMsg = await self.bot.say(embed=self.Construct_Output(argArray, author, 0, 10))
            msg = await self.bot.send_message(ctx.message.channel, embed=self.Construct_Log(argArray, collectionOutput, author))
            await self.reaction_menu(argArray, author, msg, logMsg)

def setup(bot):
    bot.add_cog(DowntimeForaging(bot))