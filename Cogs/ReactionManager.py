import discord
from discord.ext import commands

class ReactionManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        reactDB = self.bot.db.get_val('reactDB', {})
        if str(payload.channel_id) in reactDB:
            print('passed chan')
            if str(payload.message_id) in reactDB[str(payload.channel_id)]:
                print('passed mess')
                if payload.emoji.name in reactDB[str(payload.channel_id)][str(payload.message_id)]:
                    print('passed emoji')
                    foundGuild = self.bot.get_guild(payload.guild_id)
                    foundMember = await foundGuild.fetch_member(payload.user_id)
                    await foundMember.add_roles(foundGuild.get_role(reactDB[str(payload.channel_id)][str(payload.message_id)][payload.emoji.name]))

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        reactDB = self.bot.db.get_val('reactDB', {})
        if str(payload.channel_id) in reactDB:
            print('passed chan')
            if str(payload.message_id) in reactDB[str(payload.channel_id)]:
                print('passed mess')
                if payload.emoji.name in reactDB[str(payload.channel_id)][str(payload.message_id)]:
                    print('passed emoji')
                    foundGuild = self.bot.get_guild(payload.guild_id)
                    foundMember = await foundGuild.fetch_member(payload.user_id)
                    await foundMember.remove_roles(foundGuild.get_role(reactDB[str(payload.channel_id)][str(payload.message_id)][payload.emoji.name])) 

    @commands.group(pass_context=True)
    async def react(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid sub command passed...')

    @react.command(pass_context=True)
    async def add(self, ctx, channelID : discord.TextChannel, messageID : int, reaction : str, roleName : discord.Role):
        if roleCheck(ctx.author, 'Admin'):
            reactDB = self.bot.db.get_val('reactDB', {})
            print(reactDB)
            emoji = reaction
            if ':' in reaction:
                emoji = discord.utils.get(self.bot.get_all_emojis(), name = reaction.split(':')[1])
                if not emoji:
                    return await ctx.send('Apologies {0.mention}, but this emoji will not work as a reaction! Please try to use a Discord emoji or a custom Emoji on this server.'.format(ctx.author))
            print(str(reaction))
            if not str(channelID.id) in reactDB:
                print('chan')
                reactDB[str(channelID.id)] = {}
            if not str(messageID) in reactDB[str(channelID.id)]:
                print('mess')
                reactDB[str(channelID.id)][str(messageID)] = {}
            if not reaction in reactDB[str(channelID.id)][str(messageID)]:
                print('react')
                reactDB[str(channelID.id)][str(messageID)][reaction] = roleName.id
                
                message = await channelID.fetch_message(messageID)
                await message.add_reaction(emoji)
                print(reactDB)
                self.bot.db.set_val('reactDB', reactDB)

                return await ctx.send('I have fulfilled the following request for you, {0.mention}!\n{1} added to channel {2} and linked to the {3} role for the supplied message.'.format(ctx.author, emoji, channelID.mention, roleName.mention))
            else:
                
                return await ctx.send('I was unable to complete this request for you, {0.mention}!\n{1} already has the {2} role assigned to it for the supplied message!'.format(ctx.author, emoji, ctx.guild.get_role(reactDB[str(channelID.id)][str(messageID)][reaction]).mention))
                
        else:
            return await ctx.send('Apologies {0.mention}, but you are not an Admin, therefore I cannot assist you with this request!'.format(ctx.author))

    @react.command(pass_context=True)
    async def edit(self, ctx, channelName : discord.TextChannel, messageID : int, reaction : str, newRole : discord.Role):
        reactDB = self.bot.db.get_val('reactDB', {})
        if str(payload.channel_id) in reactDB:
            print('passed chan')
            if str(payload.message_id) in reactDB[str(payload.channel_id)]:
                print('passed mess')
                if payload.emoji.name in reactDB[str(payload.channel_id)][str(payload.message_id)]:
                    print('passed emoji')
                    oldRole = ctx.guild.get_role(reactDB[str(channelID.id)][str(messageID)][reaction])
                    reactDB[str(channelID.id)][str(messageID)][reaction] = newRole.id
                    self.bot.db.set_val('reactDB', reactDB)
                    return await ctx.send('I have fulfilled the following request for you, {0.mention}!\n{1}\'s role in channel {2} has been updated from {3} to {4}.'.format(ctx.author, emoji, channelID.mention, oldRole.mention, newRole.mention))
                else:
                    
                    return await ctx.send('I was unable to complete this request for you, {0.mention}!\n{1} does not have a role assigned for the supplied message!'.format(ctx.author, emoji))
                    
            else:
                return await ctx.send('Apologies {0.mention}, but you are not an Admin, therefore I cannot assist you with this request!'.format(ctx.author))

    @react.command(pass_context=True)
    async def remove(self, ctx, messageID, reaction):
        reactDB = self.bot.db.get_val('reactDB', {})
        if str(payload.channel_id) in reactDB:
            print('passed chan')
            if str(payload.message_id) in reactDB[str(payload.channel_id)]:
                print('passed mess')
                if payload.emoji.name in reactDB[str(payload.channel_id)][str(payload.message_id)]:
                    print('passed emoji')
                    oldRole = ctx.guild.get_role(reactDB[str(channelID.id)][str(messageID)][reaction])
                    del reactDB[str(channelID.id)][str(messageID)][reaction]
                    self.bot.db.set_val('reactDB', reactDB)
                    return await ctx.send('I have fulfilled the following request for you, {0.mention}!\n{1}\'s role in channel {2} has been removed.'.format(ctx.author, emoji, channelID.mention))
                else:
                    
                    return await ctx.send('I was unable to complete this request for you, {0.mention}!\n{1} does not have a role assigned for the supplied message!'.format(ctx.author, emoji))
                    
            else:
                return await ctx.send('Apologies {0.mention}, but you are not an Admin, therefore I cannot assist you with this request!'.format(ctx.author))

    @react.command(pass_context=True)
    async def update(self, ctx, userID):
        await ctx.send('eep')

    @react.command(pass_context=True)
    async def display(self, ctx, messageID):
        await ctx.send('eep')


def roleCheck(authorInfo, roleName):
    if authorInfo.id == 227168575469780992:
        return True
    for role in authorInfo.roles:
        if role.name == roleName:
            return True
        
        

def setup(bot):
    bot.add_cog(ReactionManager(bot))


#Channel Scrapper - Search Through Whitelisted Channels for emotes

# Update Entire Server Command - Loops through member list, updating their roles based on RRLs
# 	!reaction update <username | all>
# 		Updates single user's rolls
# 		Requires follow up confirmation for update all
# Add RRL - Creates a new RRL entry in the dictionary
# 	!reaction add <emote> <role names>
# Edit RRL - Edits an RRL using the message uid as a filter, and changing a pairing
# 	!reaction edit <message uid> <emote> <new role names>
# Remove RRL - Removes an emote from a message uid's RRL list
# 	!reaction delete <message uid> <emote>
# Show Server's RRL's

# Role Page Scroller