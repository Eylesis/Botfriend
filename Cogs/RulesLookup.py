import discord
import redisInterface
import re
from discord.ext import commands

class RulesLookup():
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def rule(self, ctx, *, ruleName : str):
        rulesDB = self.bot.db.get_val('RulesDB', {})
        ruleMatch = ""
        for key in rulesDB:
            match = re.search(name, key, re.IGNORECASE)

            if match:
                ruleMatch = match.group(0)
                break

        embed = discord.Embed(
            title="**{}**".format(ruleMatch), 
            description="{}".format(rulesDB[ruleMatch]))
        return await self.bot.say(embed=embed)
    
    @commands.command(pass_context=True)
    async def addRule(self, ctx, ruleName : str, *, ruleText : str):
        allowed = False
        for role in ctx.message.author.roles:
            if role.name == "Moderators" or role.name == "Helper":
                allowed = True
        if allowed or ctx.message.author.id == '227168575469780992':
            rulesDB = self.bot.db.get_val('RulesDB', {})
            ruleExists = False
            
            if ruleName in rulesDB:
                ruleExists = True
            
            rulesDB[ruleName] = ruleText
            self.bot.db.set_val('RulesDB', rulesDB)
            if ruleExists:
                return await self.bot.say('It would seem `{}` was outdated? Well, I have updated my records for the future!')
            return await self.bot.say('Oh my, a new rule? I have recorded `{}` for future use!') 
        return await self.bot.say('Terribly sorry {0.author.mention}, but I do not recognize you as a person of authority here!'.format(ctx.message))
        
    @commands.command(pass_context=True)
    async def removeRule(self, ctx, ruleName : str):
        allowed = False
        for role in ctx.message.author.roles:
            if role.name == "Moderators" or role.name == "Helper":
                allowed = True
        if allowed or ctx.message.author.id == '227168575469780992':
            rulesDB = self.bot.db.get_val('RulesDB', {})
            element = rulesDB.pop(ruleName, None)
            self.bot.db.set_val('RulesDB', rulesDB)
            if element:
                return await self.bot.say('I am sad to see the `{}` rule go! I shall purge it from my records so it will not come up in the future.'.format(ruleName))
            return await self.bot.say("Apologies, but I am unable to find the rule `{}`. Perhaps you spelled it incorrectly?".format(ruleName))
        return await self.bot.say('Terribly sorry {0.author.mention}, but I do not recognize you as a person of authority here!'.format(ctx.message))
def setup(bot):
    bot.add_cog(RulesLookup(bot))
