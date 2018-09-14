import discord
from discord.ext import commands
import datetime

class AutoDowntime():
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(pass_context=True, invoke_without_command=True)
    async def downtime(self, ctx):
        if get_active_character(ctx.message.author.id):
            await ctx.invoke(self.lookup, player=ctx.message.author, charName=get_active_character(ctx.message.author.id))
        else:
            return await self.bot.say("You do not appear to have an active character! Please add one with `*downtime add <character name>` or set one with `*downtime active <character name>`.")
               
    @downtime.command(pass_context=True)
    async def lookup((self, ctx, player: discord.Member, charName: str):
        if is_character(player.id, charName):
            logs = compile_logs(player.id, charName)
            downtime = get_downtime(player.id, charName)
            
            embed = discord.Embed(title="Downtime: {}".format(charName), description="This log displays the current downtime for {}. Automatic downtime is earned at a rate of 1 per day, incremented at 00:00:00 UTC.".format(charName))
            embed.set_footer(text="Downtime looked up by: {}".format(ctx.message.author.display_name), icon_url=ctx.message.author.avatar_url)
        
            embed.add_field(name="Total Downtime", value="{}".format(downtime))
            embed.add_field(name="Downtime Log", value="{}".format(logs))
     
            return await self.bot.say(embed=embed)
        else:
            return await self.bot.say("{} is not a registered character! To register, simply use `*downtime register {}`.".format(charName))

    @downtime.command(pass_context=True)
    async def register((self, ctx, charName: str):
        if add_character(ctx.message.author.id, charName):
            return await self.bot.say("{} has been successfully registered and will begin acquiring downtime starting at 12:00AM UTC.".format(charName))
        else:
            return await self.bot.say("{} has already been registered!".format(charName))

    @downtime.command(pass_context=True)
    async def active(self, ctx, charName: str):
        if set_active_character(ctx.message.author.id, charName):
            return await self.bot.say("{} has been set to your active character and will now be awarded downtime from quests.".format(charName))
        else:
            return await self.bot.say("{} is not a registered character! To register, simply use `*downtime register {}`.".format(charName))

    @downtime.command(pass_context=True)
    async def spend(self,ctx, value: int, reason: str):
        if get_active_character(ctx.message.author.id):
            change_downtime(ctx.message.author.id, get_active_character(ctx.message.author.id), value)
            add_log(ctx.message.author.id, get_active_character(ctx.message.author.id), value, reason)
            return await self.bot.say("Records updated for {}!".format(get_active_character(ctx.message.author.id)))
        else:
            return await self.bot.say("You do not appear to have an active character! Please add one with `*downtime add <character name>` or set one with `*downtime active <character name>`.")

    @downtime.command(pass_context=True)
    async def award(self,ctx, value: int, reason: str, *, rawMentions : str):
        embed = discord.Embed(title="Awarded Downtime".format(charName), description="{}: {}".format(value, reason))
        embed.set_footer(text="Downtime awarded by: {}".format(ctx.message.author.display_name), icon_url=ctx.message.author.avatar_url)
        log = ""
        for player in ctx.message.mentions:
            if get_active_character(player.id):
                change_downtime(player.id, get_active_character(player.id), value)
                add_log(player.id, get_active_character(player.id), value, reason)
                downtimeResult = str(get_downtime(player.id, get_active_character(player.id))
            else:
                downtimeResult = "ERROR"
            log += "**{}**: {}\n".format(get_active_character(player.id), value), downtimeResult)

        embed.add_field(name="Results", value="{}".format(log))
        return await self.bot.say(embed=embed)


def add_character(playerID: str, charName: str):
    if is_character(playerID, charName):
        return False
    else:
        DowntimeData = self.bot.db.get_value("DowntimeData")
        DowntimeData[playerID][charName] = {
                                    "Datestamp" : datetime.datetime.utcnow().date(), 
                                    "AwardedDowntime" : 0,
                                    "Log" : []
                                }
        self.bot.db.set_value("DowntimeData", DowntimeData)
        set_active_character(playerID, charName)

def add_log(playerID: str, charName: str, value: int, reason: str):
    if is_character(playerID, charName):
        DowntimeData = self.bot.db.get_value("DowntimeData")
        DowntimeData[playerID][charName]["Log"].insert(0,"{}: {}".format(value, reason))
        self.bot.db.set_value("DowntimeData", DowntimeData)
        return True
    else:
        return False

def change_downtime(playerID: str, charName: str, value: int):
    if is_character(playerID, charName):
        DowntimeData = self.bot.db.get_value("DowntimeData")
        DowntimeData[playerID][charName]["AwardedDowntime"] += value
        self.bot.db.set_value("DowntimeData", DowntimeData)
        return True
    else:
        return False

def compile_logs(playerID: str, charName: str):
    if is_character(playerID, charName):
        output = ""
        DowntimeData = self.bot.db.get_value("DowntimeData")
        for log in DowntimeData[playerID][charName]["Log"]:
            output += log + "\n"
        return output
    else:
        return ""        

def get_active_character():
    DowntimeData = self.bot.db.get_value("DowntimeData")
    if DowntimeData[playerID]:
        return DowntimeData[playerID]["Active"]
    else:
        return False

def get_downtime(playerID: str, charName: str):
    if is_character(playerID, charName):
        DowntimeData = self.bot.db.get_value("DowntimeData")
        DailyDowntime = datetime.datetime.utcnow().date() - DowntimeData[player.id][charName]["Datestamp"]
        return DowntimeData[player.id][charName]["AwardedDowntime"] + DailyDowntime
    else:
        return -1

def is_character(playerID: str, charName: str):
    DowntimeData = self.bot.db.get_value("DowntimeData")
    if playerID in DowntimeData and charName in DowntimeData[playerID]:
        return True
    else:
        return False

def set_active_character(playerID: str, charName: str):
    if is_character(playerID, charName):
        DowntimeData = self.bot.db.get_value("DowntimeData")
        DowntimeData[playerID]["Active"] = charName
        self.bot.db.set_value("DowntimeData", DowntimeData)
        return True
    else:
        return False

def setup(bot):
    bot.add_cog(AutoDowntime(bot))