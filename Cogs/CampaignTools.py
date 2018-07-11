import discord
from discord.ext import commands

class DEFAULT():
    def __init__(self, bot):
        self.bot = bot
    
    async def on_member_join(self, member):
        if member.server.id = '466679011511369728':
            await self.bot.send_message(member.server.default_channel, 'Greetings {}! You are on the guest list, so allow me prepare your rooms for you! I will be with you in a moment!'.format(member.mention))
            everyone = discord.PermissionOverwrite(read_messages=False)
            mine = discord.PermissionOverwrite(read_messages=True)
            
            await client.create_channel(member.server, "{}'s IC".format, (member.server.default_role, everyone), (member, mine), (member.server.me, mine))
            await client.create_channel(member.server, "{}'s OOC".format, (member.server.default_role, everyone), (member, mine), (member.server.me, mine))


    @commands.command(pass_context=True)
    async def DEFAULT(self, ctx):
        await self.bot.say('eep')

def setup(bot):
    bot.add_cog(DEFAULT(bot))