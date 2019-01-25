import discord
import redisInterface
import datetime
import re
from discord.ext import commands
from PIL import Image
from mcstatus import MinecraftServer
import requests
from websocket import create_connection
import json
from http.client import responses 

class Misc():
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def dicecloud_status(self, ctx):
        info = ["[1xx] Informational : This should not show up. Run the status again in a moment and notify Eylesis.",
                "[2xx] Success : Everything is working fine. ",
                "[3xx] Redirection :  This should not show up. Run the status again in a moment and notify Eylesis.",
                "[4xx] Client Error : Dicecloud is down, but like kinda working. Don't update right now and don't refresh your dicecloud tab.",
                "[5xx] Server Error : Dicecloud is down. Entirely down. It is broke. Don't update right now and don't refresh your dicecloud tab."]
        queries = [
            {
                'url':'https://dicecloud.com',
                'name' : 'Webpage Status Code'
            }]

        embed = discord.Embed(title="Dicecloud Status Ping",
                            description="Botfriend's P.I. has infiltrated the Dicecloud servers and come back with this information.")
        
        for query in queries:
            response = requests.get(query['url'])
            embed.add_field(name="{}: {}".format(query['name'], str(int(response.status_code))), value=responses[int(response.status_code)])
        
        ws = create_connection("wss://dicecloud.com/websocket", timeout=10000)
        result = ws.recv()
        ws.send(json.dumps({"msg" : "connect", "version": "1", "support" : ["1", "pre2", "pre1"]}))
        result = json.loads(ws.recv())
        success = True
        if result["msg"] != "connected":
            success = False
        ws.send(json.dumps({"msg" : "ping"}))
        result = json.loads(ws.recv())
        if result["msg"] != "pong":
            success = False
        output = []
        if success:
            output = ["Connected", "The websocket returned a pong. We have no idea if this means it's functioning, but it's definitely not all the way dead."]
        else:
            output = ["Disconnected", "The websocket couldn't give us a pong. We have no idea if this means it's dead, but it's definitely not all the way working."]
        ws.close()
        
        embed.add_field(name="Socket Status: {}".format(output[0]), value=output[1])
        embed.add_field(name="HTTP Status Code Information", value=info[(int(response.status_code) / 100 ) -1])
        await self.bot.say(embed=embed)

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
        match = re.search('(\s|^)c(a+)t(\s|$)', message.content.lower())
        if match:
            segments = len(match.group(2))
            images = []
            images.append(Image.open('images/tail.png'))
            for x in range(0,segments+1):
                images.append(Image.open('images/body.png'))
            images.append(Image.open('images/head.png'))
            widths,height = zip(*(i.size for i in images))

            total_widths = sum(widths)
            max_height = max(height)

            out_im = Image.new('RGBA', (total_widths, max_height))

            x_offset = 0
            for image in images:
                out_im.paste(image, (x_offset,0))
                x_offset += image.size[0]
            out_im.save('images/out.png')
            await self.bot.send_file(message.channel, r'images/out.png', filename="cat.png")

def setup(bot):
    bot.add_cog(Misc(bot))
