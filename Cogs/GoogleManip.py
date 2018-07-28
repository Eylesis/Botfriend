import discord
import aiohttp
import os
import asyncio
import redisInterface
import pygsheets
from discord.ext import commands
from oauth2client import crypt
from oauth2client.service_account import ServiceAccountCredentials

class GoogleManip():
    def __init__(self, bot):
        self.bot = bot
        self.API_KEY = os.environ.get('API_KEY')
        signer = crypt.Signer.from_string(PRIVATE_KEY)
        cred = ServiceAccountCredentials(CLIENT_EMAIL, signer, private_key_id=PRIVATE_KEY_ID, client_id=CLIENT_ID)
        self.gc = pygsheets.authorize(credentials=cred)
    
    @commands.command(pass_context=True)
    async def ungold(self, ctx):
        userGoldData = self.bot.db.from_json(self.bot.db.get_val('UserGoldData'))
        userGoldData.pop(ctx.message.author.id, None)
        self.bot.db.set_val('UserGoldData', self.bot.db.to_json(userGoldData))
        await self.bot.say('done.')

    @commands.command(pass_context=True)
    async def gold(self, ctx, sheetUrl : str):
        
        if self.bot.db.get_val('UserGoldData') != 0:
            userGoldData = self.bot.db.from_json(self.bot.db.get_val('UserGoldData'))
        else:
            userGoldData = {}
        if not ctx.message.author.id in userGoldData:
            
            try:
               sh = self.gc.open_by_url(sheetUrl)
            except:
                return await self.bot.say('I have run into an error attempting to access this sheet. Have you shared it to me?')
            wks = sh.sheet1
            charName = wks.cell('L8')
            startBal = wks.cell('L9')

            userGoldData[ctx.message.author.id] = {'CharName' : charName.value, "StartBal" : startBal.value, "sheetUrl" : sheetUrl}
            self.bot.db.set_val('UserGoldData', self.bot.db.to_json(userGoldData))
            return await self.bot.say('{}, it is really appreciated that you have opted to join this data collection initiative! I have gone ahead and added {} to our listings!'.format(ctx.message.author.mention, charName.value))
        else:
            return await self.bot.say("{}, it would appear I already have one of your characters registered! Submitting your data is now automated. Simply keep your Gold Tracking Sheet up to date before running Avrae's `!update` command!".format(ctx.message.author.mention))

    async def on_message(self, message):
        if message.content.startswith('!update'):
            await asyncio.sleep(12)  # give avrae some time to update
            async with aiohttp.ClientSession() as session:
                async with session.get('https://avrae.io/api/activecharacter',
                                       params={"user": message.author.id},
                                       headers={"Authorization": self.API_KEY}
                                       ) as resp:
                    data = await resp.json()
                if data is None:
                    return  # what did you even do?
                async with session.get('https://avrae.io/api/character',
                                       params={"user": message.author.id,
                                               "id": data},
                                       headers={"Authorization": self.API_KEY}
                                       ) as resp:
                    character = await resp.json()
            if character is None:
                return
            level = character['levels']['level']

            userGoldData = self.bot.db.from_json(self.bot.db.get_val('UserGoldData'))
            sheetUrl = str(userGoldData[message.author.id]['sheetUrl'])
            print('url: {}'.format(sheetUrl))
            if not message.author.id in userGoldData:
                return
            else:
                try:
                    sh = self.gc.open_by_url(sheetUrl)
                except:    
                    return await self.bot.send_message(message.channel,'It appears you are opted into the Gold Tracking Initiative, however I was unable to access your tracking sheet. Please ensure you still have the sheet shared to me so I may collect your data!')
                wks = sh.sheet1
                if character['stats']['name'] == userGoldData[message.author.id]['CharName']:
                    CurBal = wks.cell('E18')
                    Expenses = wks.cell('C23')
                    Income = wks.cell('I23')
                    Spent = wks.cell('I16')
                    Decrease = wks.cell('I14')

                    userGoldData[message.author.id][character['levels']['level']] = { "CurBal" : CurBal.value, "Expenses" : Expenses.value, "Income" : Income.value, "Spent" : Spent.value, "Decrease" : Decrease.value }
                    self.bot.db.set_val('UserGoldData', self.bot.db.to_json(userGoldData))
                else:
                    return await self.bot.send_message(message.channel,'Sorry to bother you, {}. I have you on my listing for the Gold Tracking Initiative, but you have updated a different character. If this is not a mistake, then please ignore me! Otherwise, be sure to set the correct character active before running the `!update` command again!'.format(message.author.mention))
                await self.bot.send_message(message.channel, '{}, I have gone ahead and marked down the data on your tracker sheet for this level.'.format(message.author.mention))
                print(userGoldData)
def setup(bot):
    bot.add_cog(GoogleManip(bot))