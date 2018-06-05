import discord
from discord.ext import commands
import urllib.request
import json
import redisInterface

class xplog():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def logxp(self, ctx, id, character, event, experience : int):
        if "dungeon master" in [y.name.lower() for y in ctx.message.author.roles]:
            if self.bot.db.get_val('xp_log') == '':
                to_db = {}
            else:
                to_db = self.bot.db.from_json(self.bot.db.get_val('xp_log'))
                name = id[id.find('!')+1:id.find('>')]
                
                if name not in to_db.keys():
                    to_db[name] = {}
                if character not in to_db[name].keys():
                    to_db[name][character] = {}
                if 'events' not in to_db[name][character].keys():
                    to_db[name][character]['events'] = {}
                if 'total' not in to_db[name][character].keys():
                    to_db[name][character]['total'] = 0    
                to_db[name][character]['events'][event] = experience
                to_db[name][character]['total'] += experience
                self.bot.db.set_val('xp_log', self.bot.db.to_json(to_db))
                await self.bot.say("{} has been logged for {} XP to {}.".format(event, experience, character))      
        else:
            await self.bot.say("You do not have Dungeon Master permissions!")
    @commands.command(pass_context=True)
    async def delxp(self, ctx, id, character, event):
        if "dungeon master" in [y.name.lower() for y in ctx.message.author.roles]:
            if self.bot.db.get_val('xp_log') == '':
                to_db = {}
            else:
                to_db = self.bot.db.from_json(self.bot.db.get_val('xp_log'))
                name = id[id.find('!')+1:id.find('>')]
                
                if name not in to_db.keys():
                    return await self.bot.say("Player does not exist!")
                if character not in to_db[name].keys():
                    return await self.bot.say("Character does not exist!")
                if 'events' not in to_db[name][character].keys():
                    return await self.bot.say("Character has not done any events!")
                if event not in to_db[name][character]['events'].keys():
                    return await self.bot.say("Character did not attend that event!")
                to_db[name][character]['total'] -= to_db[name][character]['events'][event]
                experience = to_db[name][character]['events'][event]
                to_db[name][character]['events'].pop(event)
                self.bot.db.set_val('xp_log', self.bot.db.to_json(to_db))
                await self.bot.say("{} has been removed from {}'s memories.".format(event, experience, character))  
        else:
            await self.bot.say("You do not have Dungeon Master permissions!")

    @commands.command(pass_context=True)
    async def getxp(self, ctx, character):
        xp_log = self.bot.db.from_json(self.bot.db.get_val('xp_log'))
        if xp_log.get(ctx.message.author.id) != None:
            player = xp_log[ctx.message.author.id]
            output = ""
            if player.get(character) != None:
                for k,v in player[character]['events'].items():
                    output += f"{k}: {v}\n"
                output += "Total XP: {}".format(player[character]['total'])

                embed = discord.Embed(title=character, description=output)
                return await self.bot.say(embed=embed)
            else:
                pass
        await self.bot.say("That character does not exist!")
        
    @commands.command(pass_context=True)
    async def DMgetxp(self, ctx, id, character):
        if "dungeon master" in [y.name.lower() for y in ctx.message.author.roles]:
            xp_log = self.bot.db.from_json(self.bot.db.get_val('xp_log'))
            name = id[id.find('!')+1:id.find('>')]
            if xp_log.get(name) != None:
                
                player = xp_log[name]
                output = ""
                if player.get(character) != None:
                    for k,v in player[character]['events'].items():
                        output += f"{k}: {v}\n"
                    output += "Total XP: {}".format(player[character]['total'])

                    embed = discord.Embed(title=character, description=output)
                    return await self.bot.say(embed=embed)
                else:
                    pass
            await self.bot.say("That character does not exist!")
        else:
            await self.bot.say("You do not have Dungeon Master permissions!")

def setup(bot):
    bot.add_cog(xplog(bot))