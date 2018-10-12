import discord
import redisInterface
import datetime
import re
from discord.ext import commands
from PIL import Image
from mcstatus import MinecraftServer

class Misc():
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def minecraft(self, ctx):
        server = MinecraftServer("142.44.191.72:28176")
        status = server.status()
        server.port = 25565
        query = server.query()
        embed = discord.Embed(title="Ey's Server",description="Minecraft server information and status.")
        
        embed.add_field(name="IP Address", value="142.44.191.72:28176")
        embed.add_field(name="Modpack", value="Enigmatica 2")
        playerList = ""
        for player in query.players.names:
            playerList += "{}\n".format(player)

        embed.add_field(name="Players: {} / {}".format(query.players.online, query.players.max), 
                        value=playerList)
    
        
        self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def banana(self, ctx):
        bananaStash = int(self.bot.db.get_val('bananaStash', 0))
        
        if bananaStash == 68:
            bananaStash = 0
            await self.bot.say('!69')
                
        if bananaStash == 0:
            await self.bot.say('Why thank you {}! This banana is the first in my latest stash! I shall store it carefully.'.format(ctx.message.author.mention))
            self.bot.db.set_val('bananaStash', '1')
        else:
            bananaStash += 1
            self.bot.db.set_val('bananaStash', str(bananaStash))
            await self.bot.say('Why thank you {}! I do so enjoy bananas, however I am not hungry at the moment, so I shall save this for later! My stash has {} bananas in it, can you believe it?'
            .format(ctx.message.author.mention, bananaStash))
        return await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True, hidden=True)
    async def chanSay(self, ctx, channel: str, *, message: str):
        if ctx.message.author.id == '227168575469780992':
            await self.bot.send_message(self.bot.get_channel(channel), message)
    
    async def on_message(self, message):
        match = re.fullmatch('c(a+)t', message.content.lower())
        if match:
            segments = len(match.group(1))
            images = []
            images.append(Image.open('images/tail.jpg'))
            for x in range(0,segments+1):
                images.append(Image.open('images/body.jpg'))
            images.append(Image.open('images/head.jpg'))
            widths,heights = zip(*(i.size for i in images))

            total_widths = sum(widths)
            max_height = max(height)

            out_im = Image.new('RGB', (total_width, max_height))

            x_offset = 0
            for image in images:
                out_im.paste(image, (x_offset,0))
                x_offset += image.size[0]
            out_image.save('images/out.jpg')
            self.bot.send_file(message.channel, 'images/out.jpg')

def setup(bot):
    bot.add_cog(Misc(bot))
