import discord
import asyncio
from discord.ext import commands

class Misc():
    def __init__(self,  bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def todo(self, ctx, inputVar: str):
        author = ctx.message.author
        print(author.name)
        todo = open("todo.txt","a+")        
        todo.write("{0}: {1}".format(author.name, inputVar))
        todo.write("\n")
        todo.close()
        await self.bot.say("Your To-Do entry has been safely logged.")
        
def setup(bot):
    bot.add_cog(Misc(bot))