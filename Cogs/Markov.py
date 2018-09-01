import discord
import asyncio
import markovify
import re
import util_functions
from discord.ext import commands

class Markov():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def load_chan(self, ctx, chan: discord.Channel):
        existing_data = [m.id for m in self.bot.training_data]
        print("Loading ALL data for channel " + str(chan))
        if chan.type is discord.ChannelType.text:
            try:
                oldest_timestamp = chan.created_at
                all_loaded = 0
                while True:
                    loaded = 0
                    loglen = 0
                    async for m in self.bot.logs_from(chan, 10000, after=oldest_timestamp):
                        loglen += 1
                        if m.timestamp > oldest_timestamp:
                            oldest_timestamp = m.timestamp
                        if m.id not in existing_data:
                            self.bot.training_data.append(m)
                            loaded += 1
                            all_loaded += 1
                    await asyncio.sleep(0.5)  # @UndefinedVariable
                    print("... loaded {} messages.".format(str(loaded)))
                    if loglen == 0: break
            except:
                pass
        print("Done! Loaded {} messages total.".format(str(all_loaded)))
        await self.bot.say("Done! Loaded {} messages total.".format(str(all_loaded)))

    @commands.command(pass_context=True)
    async def load_server(self, ctx):
        existing_data = [m.id for m in self.bot.training_data]
        print("Loading ALL data for server " + str(ctx.message.server))
        all_loaded = 0
        for chan in ctx.message.server.channels:
            print("Loading ALL data for channel " + str(chan))
            chan_loaded = 0
            if chan.type is discord.ChannelType.text:
                try:
                    oldest_timestamp = chan.created_at
                    while True:
                        loaded = 0
                        loglen = 0
                        async for m in self.bot.logs_from(chan, 10000, after=oldest_timestamp):
                            loglen += 1
                            if m.timestamp > oldest_timestamp:
                                oldest_timestamp = m.timestamp
                            if m.id not in existing_data:
                                self.bot.training_data.append(m)
                                loaded += 1
                                all_loaded += 1
                                chan_loaded += 1
                        await asyncio.sleep(0.5)  # @UndefinedVariable
                        print("... loaded {} messages.".format(str(loaded)))
                        if loglen == 0: break
                except:
                    pass
            print("Done for channel {}! Loaded {} messages total.".format(str(chan), str(chan_loaded)))
            #await self.bot.say("Done for channel {}! Loaded {} messages total.".format(str(chan), str(chan_loaded)))
        print("Done! Loaded {} messages total.".format(str(all_loaded)))
        await self.bot.say("Done! Loaded {} messages total.".format(str(all_loaded)))

    async def load():
        await self.bot.wait_until_ready()
        existing_data = [m.id for m in self.bot.training_data]
        for s in self.bot.servers:
            print("Loading data for server " + str(s))
            for c in s.channels:
                print("Loading data for channel " + str(c))
                if c.type is discord.ChannelType.text:
                    try:
                        loaded = 0
                        async for m in self.bot.logs_from(c, 1000):
                            if m.id not in existing_data:
                                self.bot.training_data.append(m)
                                loaded += 1
                    except:
                        pass
                    print("... loaded {} messages.".format(str(loaded)))
                # await asyncio.sleep(0.5)  # @UndefinedVariable
        print("Loaded!")
        
    @commands.command(pass_context=True)
    async def chanMarkov(self, ctx, channel: discord.Channel = None, num: int = 1):
        text = ''
        if channel is None:
            channel = ctx.message.channel
        for m in self.bot.training_data:
            if m.channel.id == channel.id:
                text += m.content + '\n'
        markov = markovify.NewlineText(text, state_size=self.bot.STATE_SIZE)
        out = ''
        for i in range(num):
            try:
                out += markov.make_sentence(tries=1000) + '\n\n'
            except:
                pass
        out = util_functions.fix_mentions(self.bot, out)
        await self.bot.say(out)  # @UndefinedVariable 

    @commands.command(pass_context=True)
    async def servMarkov(self, ctx, num: int = 1):
        loading = await self.bot.say("Generating, this might take a while...")
        def _():
            text = ''
            for m in self.bot.training_data:
                if m.server is not None:
                    if m.server.id == ctx.message.server.id:
                        text += m.content + '\n'
            markov = markovify.NewlineText(text, state_size=self.bot.STATE_SIZE)
            out = ''
            for i in range(num):
                try:
                    out += markov.make_sentence(tries=1000) + '\n\n'
                except:
                    pass
            out = util_functions.fix_mentions(self.bot, out)
            return out
        out = await asyncio.get_event_loop().run_in_executor(None, _)
        await self.bot.edit_message(loading, out)  # @UndefinedVariable

    @commands.command(pass_context=True)
    async def membMarkov(self, ctx, member: discord.Member, num: int = 1):
        text = ''
        for m in self.bot.training_data:
            if m.server is not None:
                if m.author.id == member.id and m.server.id == ctx.message.server.id:
                    text += m.content + '\n'
        markov = markovify.NewlineText(text, state_size=self.bot.STATE_SIZE)
        out = ''
        for i in range(num):
            try:
                out += markov.make_sentence(tries=1000) + '\n\n'
            except:
                pass
        out = util_functions.fix_mentions(self.bot, out)
        await self.bot.say(out)  # @UndefinedVariable

    @commands.command(pass_context=True)
    async def userMarkov(self, ctx, member: str, num: int = 1):
        text = ''
        for m in self.bot.training_data:
            if m.author.id == member:
                text += m.content + '\n'
        markov = markovify.NewlineText(text, state_size=self.bot.STATE_SIZE)
        out = ''
        for i in range(num):
            try:
                out += markov.make_sentence(tries=1000) + '\n\n'
            except:
                pass
        out = util_functions.fix_mentions(self.bot, out)
        await self.bot.say(out)  # @UndefinedVariable

    @commands.command(pass_context=True)
    async def globMarkov(self, ctx, num: int = 1):
        print("Starting global markov...")
        text = ''
        for m in self.bot.training_data:
            text += m.content + '\n'
        markov = markovify.NewlineText(text, state_size=self.bot.STATE_SIZE)
        out = ''
        for i in range(num):
            try:
                out += markov.make_sentence(tries=1000) + '\n\n'
            except:
                pass
        out = util_function.fix_mentions(self.bot, out)
        await self.bot.say(out)  # @UndefinedVariable


    @commands.command()
    async def state_size(self, size: int = 2):
        self.bot.STATE_SIZE = size
        await self.bot.say("State size set to " + str(size))

def setup(bot):
    bot.add_cog(Markov(bot))
