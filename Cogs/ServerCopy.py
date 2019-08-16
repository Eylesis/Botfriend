import discord
from discord.ext import commands

class ServerCopy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def server_manifest(self, ctx, sourceID : int, serverID : int):
        await ctx.send('It seems you have put in a request for a server manifest. Allow me a moment to investigate.')
        serverChannels = self.bot.get_guild(serverID).text_channels
        serverCategories = self.bot.get_guild(serverID).categories
        sourceGuild = self.bot.get_guild(sourceID)
        categoryConversions = {}
        
        for channel in serverCategories:
            if type(channel) is discord.channel.CategoryChannel:
                
                newChannel = await sourceGuild.create_category_channel(channel.name, reason="Botfriend Channel Rehoming Service!")
                categoryConversions[channel.id] = newChannel.id

        for channel in serverChannels:
            if type(channel) is discord.channel.TextChannel:
                if channel.category_id == None:
                    await sourceGuild.create_text_channel(channel.name, position=channel.position + 1, topic=channel.topic, reason="Botfriend Channel Rehoming Service!")
                else:
                    await sourceGuild.create_text_channel(channel.name, position=channel.position + 1, topic=channel.topic, category=sourceGuild.get_channel(categoryConversions[channel.category_id]), reason="Botfriend Channel Rehoming Service!")

            if type(channel) is discord.channel.VoiceChannel:
                if channel.category_id == None:
                    await sourceGuild.create_voice_channel(channel.name, bitrate=channel.bitrate, user_limit=channel.user_limit, position=channel.position + 1, reason="Botfriend Channel Rehoming Service!")
                else:    
                    await sourceGuild.create_voice_channel(channel.name, bitrate=channel.bitrate, user_limit=channel.user_limit, position=channel.position + 1, category=sourceGuild.get_channel(categoryConversions[channel.category_id]), reason="Botfriend Channel Rehoming Service!")
            

    # @commands.command(pass_context=True)
    #     async def deepcopy(self, ctx):
            

def setup(bot):
    bot.add_cog(ServerCopy(bot))
