import traceback
import json
import util_functions
from discord.ext import commands
import discord
import sys
import re
import os
import asyncio
from aiohttp import web
import datetime

botToken = os.environ.get('botToken')

def run_app(app, *, host='0.0.0.0', port=None, shutdown_timeout=60.0, ssl_context=None, print=print, backlog=128):
    """Run an app"""
    if port is None:
        if not ssl_context:
            port = 8080
        else:
            port = 8443

    loop = app.loop

    handler = app.make_handler()
    server = loop.create_server(handler, host, port, ssl=ssl_context, backlog=backlog)
    srv, startup_res = loop.run_until_complete(asyncio.gather(server, app.startup(), loop=loop))

    scheme = 'https' if ssl_context else 'http'
    print("======== Running on {scheme}://{host}:{port}/ ========\n"
            "(Press CTRL+C to quit)".format(
        scheme=scheme, host=host, port=port))

async def tba_handler(request):
    data = await request.post()
    print("Accepted request:\n{}".format(data))
    print("{}".format(data))
    embed = discord.Embed(
        title="Crooq's Computer Quest Updated!", 
        url="https://ko-fi.com/eylesis", 
        description="{} has given ${} to the cause! The donation is appreciated!".format(data['from_name'], data['amount']), 
        timestamp=datetime.datetime.fromisoformat(data['timestamp']))
    embed.set_footer(text="Ko-Fi")
    embed.add_field(name="__Message__", value=data['message'])

    channelids = {'470455397912674305'} #, '404368678683934731'
    for channelid in channelids:
        await bot.send_message(bot.get_channel(channelid), embed=embed)
    return web.Response()
            

bot = commands.Bot(command_prefix='*')
loop = bot.loop
app = web.Application(loop=loop)
app.router.add_post('/endpoint', tba_handler)




if __name__ == "__main__":
    run_app(app, host=os.environ.get('HOST'), port=os.environ.get('PORT'))
    bot.run(botToken)