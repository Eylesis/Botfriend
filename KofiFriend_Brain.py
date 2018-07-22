import traceback
import json
import util_functions
from discord.ext import commands
import sys
import re
import os
import aiohttp

botToken = os.environ.get('botToken')

def run_app(self, app, *, host='0.0.0.0', port=None, shutdown_timeout=60.0, ssl_context=None, print=print, backlog=128):
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
    data = await request.json()
    print("Accepted request:\n{}".format(data))

    return await self.bot.send_message(
        self.bot.get_channel('404368678683934731'), 
        'post recieved!')
            

bot = commands.Bot(command_prefix='*', description=description)
loop = bot.loop
app = web.Application(loop=loop)
app.router.add_post('/endpoint', self.tba_handler)




if __name__ == "__main__":
    run_app(app, host=os.environ.get('HOST'), port=os.environ.get('PORT'))
    bot.run(botToken)