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
        self.gc = pygsheets.authorize(service_file='Botfriend-creds.json')
    
    @commands.command(pass_context=True)
    async def ungold(self, ctx, userID):
        if ctx.message.author.id == '227168575469780992':
            userGoldData = self.bot.db.get_val('UserGoldData')
            userGoldData.pop(userID, None)
            self.bot.db.set_val('UserGoldData', userGoldData)
            return await self.bot.say('I have removed this ID from the Gold Tracking Project.')
        else:
            return await self.bot.say('Terribly sorry {0.author.mention}, but I do not recognize you as a person of authority here!'.format(ctx.message))

    @commands.command(pass_context=True)
    async def gold(self, ctx, sheetUrl=None):
        if sheetUrl == None:
            embed = discord.Embed(title="Gold Tracking Project!", 
            description="So, you want to be apart of the gold tracking project? Well good on you! This project is an attempt to collect tangible data on the recent gold changes for the Planar Marches Moderation Team to analyze. So, how do you join the initiative? It's simple, allow me to walk you through the process!")
            
            embed.add_field(name="Register a Sheet", value="First, grab a copy of this [google sheet](https://docs.google.com/spreadsheets/d/1n5Mpnvrw5T-lfDtGRNnP8ePwdR9WPcJf-XAuu42Thtw/edit?usp=sharing). It is your sheet to log any and all gold income and expense. It behaves like a standard balancing sheet. If you have questions, be sure to visit the help-zone channel! To register the sheet, share the sheet with me, Botfriend! \nMy google email is `botfriend@botfriend-3393.iam.gserviceaccount.com`, just give me edit permissions to your excel sheet. Once that has been completed, all that's left is to run this command again, with your sheet url! `*gold url`")
            embed.add_field(name="How to Setup a Sheet", value="The sheet looks complex, right? Well it really is quite a complex task of handling gold. Luckily for you, there are only a few requirements to set up the sheet. You will notice two fields in the top right of the sheet. **Character Name**, and **Starting Balance**. The **Character Name** must match exactly the name of your character as seen on your Avrae sheet. We use this to make sure you're not accidentally using the level of a different character! And the **Starting Balance** is whatever gold total you have on your sheet when you first set up the sheet. These two values are static. Once you set them, don't touch them! The other section you can customize is the Income and Expense categories. You can change the names on the first page of these categories to suit your characters income types. Not a caster and don't need Spell Components? Replace it with a fancy dinners expense category!")
            embed.add_field(name="Sending your Data to Botfriend.", value="Once you have received a confirmation message from me following the **Register a Sheet** step, you're actually all set! Everytime you run the `!update` command with your registered character, I will access your transaction sheet and pull the relevant data. You don't have to do anything new!")
            return await self.bot.say(embed=embed)
        else:
            userGoldData = self.bot.db.get_val('UserGoldData', {})

            if not ctx.message.author.id in userGoldData:
                
                try:
                    sh = self.gc.open_by_url(sheetUrl)
                except:
                    return await self.bot.say('I have run into an error attempting to access this sheet. Have you shared it to me?')
                wks = sh.sheet1
                charName = wks.cell('L8')
                startBal = wks.cell('L9')

                userGoldData[ctx.message.author.id] = {'CharName' : charName.value, "StartBal" : startBal.value, "sheetUrl" : sheetUrl, "entries" : 0}
                self.bot.db.set_val('UserGoldData', userGoldData)
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

            userGoldData = self.bot.db.get_val('UserGoldData')
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

                    
                    newKey = str(character['levels']['level']) + str(userGoldData[message.author.id]['entries'])
                    print(newKey)
                    newEntry = userGoldData[message.author.id]['entries'] + 1
                    print(newEntry)
                    
                    userGoldData[message.author.id]['entries'] = newEntry
                    userGoldData[str(newKey)] = { "CurBal" : CurBal.value, "Expenses" : Expenses.value, "Income" : Income.value, "Spent" : Spent.value, "Decrease" : Decrease.value }
                    self.bot.db.set_val('UserGoldData', userGoldData)
                else:
                    return await self.bot.send_message(message.channel,'Sorry to bother you, {}. I have you on my listing for the Gold Tracking Initiative, but you have updated a different character. If this is not a mistake, then please ignore me! Otherwise, be sure to set the correct character active before running the `!update` command again!'.format(message.author.mention))
                await self.bot.send_message(message.channel, '{}, I have gone ahead and marked down the data on your tracker sheet for this level.'.format(message.author.mention))
                print(userGoldData)
def setup(bot):
    bot.add_cog(GoogleManip(bot))