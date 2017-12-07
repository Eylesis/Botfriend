import discord
from discord.ext import commands
import urllib.request
import json
from GameTime import get_gametime
import redisInterface

class xplog():
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def redis(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid git command passed...')
    
    
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
        
    @redis.command()
    async def delkey(self, key):
         redismonkey = redisInterface.Database()
         await self.bot.say(redismonkey.delete(key))
def setup(bot):
    bot.add_cog(xplog(bot))