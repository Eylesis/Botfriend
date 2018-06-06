import discord
from discord.ext import commands

import aiohttp
import asyncio
import os
import re

API_KEY = os.environ.get('API_KEY')


class AutoRole():
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if message.content.startswith('!update'):
            await asyncio.sleep(10)  # give avrae some time to update
            async with aiohttp.ClientSession() as session:
                async with session.get('https://avrae.io/api/activecharacter',
                                       params={"user": message.author.id},
                                       headers={"Authorization": API_KEY}
                                       ) as resp:
                    data = await resp.json()
                if data is None:
                    return  # what did you even do?
                async with session.get('https://avrae.io/api/character',
                                       params={"user": message.author.id,
                                               "id": data},
                                       headers={"Authorization": API_KEY}
                                       ) as resp:
                    character = await resp.json()
            if character is None:
                return
            level = character['levels']['level']
            roleStrs = [r.name for r in message.author.roles]
            # only if user already has a level role
            if any(re.match(r"Lvl \d+(?:-\d+)?", r) for r in roleStrs):
                new_name = "Lvl {}".format(level)
                new_role = discord.utils.get(
                    message.server.roles, name=new_name)
                to_remove = [r for r in message.author.roles if re.match(
                    r"Lvl \d+(?:-\d+)?", r.name)]
                if new_name in [r.name for r in to_remove]:
                    return  # you already have this role, go away
                if new_role:
                    await self.bot.remove_roles(message.author, *to_remove)
                    await self.bot.add_roles(message.author, new_role)
                    await self.bot.send_message(message.channel,
                                                "I see you have changed, {}! As such, I have assigned you the much more fitting role of {}.".format(message.author.mention, new_role.name))


def setup(bot):
    bot.add_cog(AutoRole(bot))
