import discord
from discord.ext import commands

class CampaignTools():
    def __init__(self, bot):
        self.bot = bot
    
    async def on_member_join(self, member):
        if member.server.id == '466679011511369728':
            await self.bot.send_message(self.bot.get_channel('466695135967707138'), 'Greetings {}! You are on the guest list, so allow me prepare your rooms for you! I will be with you in a moment!'.format(member.mention))
            everyone = discord.PermissionOverwrite(read_messages=False)
            mine = discord.PermissionOverwrite(read_messages=True)
            
            await self.bot.create_channel(member.server, "{}- IC".format(member.name), (member.server.default_role, everyone), (member, mine), (member.server.me, mine))
            await self.bot.create_channel(member.server, "{}- OOC".format(member.name), (member.server.default_role, everyone), (member, mine), (member.server.me, mine))


            await self.bot.send_message(self.bot.get_channel('466695135967707138'), 
            "Ha! A moment for me is much faster than a moment for you! Your rooms have been prepared. Now then, let me take some time to assign you your honorary title.")
            
            role = discord.utils.get(member.server.roles, name='Player')
            await self.bot.add_roles(member, role)
            await self.bot.send_message(self.bot.get_channel('466695135967707138'), 
            "Marvelous! You are now officially a Player. I bet you're still trying to figure out what your rooms are? I shall leave you awestruck, and wish you an enjoyable stay.") 

def setup(bot):
    bot.add_cog(CampaignTools(bot))
