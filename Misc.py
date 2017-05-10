import discord
import asyncio
from discord.ext import commands

class Misc():
    def __init__(self,  bot):
        self.bot = bot
    
    @commands.group(pass_context=True)
    async def todo(self, ctx):
        if ctx.invoked_subcommand is None:
            await bot.say('Invalid todo command.')

    @todo.command(pass_context=True)
    async def add(self, ctx, *inputVar: str):
        author = ctx.message.author
        print(author.id)
        todo = open("{0}.txt".format(author.id),"a+")
        outputString = ""
        for words in inputVar:
            outputString += words + " "         
        todo.write("{0}".format(outputString))
        todo.write("\n")
        todo.close()
        await self.bot.say("Your To-Do entry has been safely logged.")
        await self.bot.delete_message(ctx.message)
    
    @todo.command(pass_context =True)
    async def read(self, ctx):
        author = ctx.message.author
        try:
            with open("{0}.txt".format(author.id),"r") as todo:
                content = todo.readlines()
        except:
            await self.bot.say("File not found. Have you added any todo's?")
            return await self.bot.delete_message(ctx.message)
        
        content = [x.strip('\n') for x in content]
        output = ""
        i=0
        for lines in content:
            i+=1
            output += "{0}. {1}\n".format(i, lines) 
        em = discord.Embed( title="{0}'s To-Do List".format(author.name), description=output)
        em.set_footer(text="requested by {user}".format(user=author.name), icon_url=author.avatar_url)
        await self.bot.say(embed=em)
        return await self.bot.delete_message(ctx.message)

    @todo.command(pass_context=True)
    async def delete(self, ctx, index: int):
        author = ctx.message.author
        try:
            with open("{0}.txt".format(author.id),"r") as todo:
                content = todo.readlines()
        except:
            await self.bot.say("File not found. Have you added and todo's?")
            return await self.bot.delete_message(ctx.message)

        if(index < 1 or index > (len(content)+1)):
            print("hit")
            await self.bot.say("Entry not found.")
            return await self.bot.delete_message(ctx.message)

        else:
            del content[index-1]
            
        todo = open("{0}.txt".format(author.id),"w+")
        for lines in content:
            todo.write(lines)
        todo.close()
        await self.bot.say("Your To-Do list has been updated.")
        await self.bot.delete_message(ctx.message)
def setup(bot):
    bot.add_cog(Misc(bot))