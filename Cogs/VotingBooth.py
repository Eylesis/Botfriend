import discord
from discord.ext import commands

class VotingBooth(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.nominees = ['Vanagandr', 'UberAffe', 'Eylesis', 'LightningNevan', 'TheEmeraldOtter', 'Etheldread', 'vareek', 'Whiteherrin1584']

    @commands.command(pass_context=True)
    async def vote(self, ctx, candidateName1: str, candidateName2: str):
        if isinstance(ctx.channel, discord.TextChannel):
            return await ctx.send('Apologies {0.mention}, but this appears to be a public channel! voting must be conducted in a private channel. Please feel free to step into my office, I just cleaned it!'.format(ctx.author))
        
        nominees = ['Vanagandr', 'UberAffe', 'Eylesis', 'LightningNevan', 'TheEmeraldOtter', 'Etheldread', 'vareek', 'Whiteherrin1584']
        
        votingDB = self.bot.db.get_val('votingDB', {})
        if str(ctx.author.id) not in votingDB:
            await ctx.send('Greetings {0.mention}! I checked my database records and have not found an entry for you. Allow me to enter your information into my database and get your vote squared away!'.format(ctx.author))
            votingDB[str(ctx.author.id)] = []

            if candidateName1 in self.nominees and candidateName2 in self.nominees:
                votingDB[str(ctx.author.id)].append(candidateName1)
                votingDB[str(ctx.author.id)].append(candidateName2)

                if 'tallies' not in votingDB:
                    votingDB['tallies'] = {}
                if candidateName1 not in votingDB['tallies']:
                    votingDB['tallies'][candidateName1] = []
                if candidateName2 not in votingDB['tallies']:
                    votingDB['tallies'][candidateName2] = []
                votingDB['tallies'][candidateName1].append(str(ctx.author.id))
                votingDB['tallies'][candidateName2].append(str(ctx.author.id))

                self.bot.db.set_val('votingDB', votingDB)
                return await ctx.send('It appears your ballot is in order, {0.mention}. I have gone ahead and submitted it to my database for processing. If you change your mind about your vote, please use the `{1}clearvote` command, then resubmit a new ballot. Have a great day!'.format(ctx.author, ctx.prefix))

            else:
                return await ctx.send('Apologies {0.mention}, but I am having a hard time reading the writing on this ballot. One or both of these names does not appear to be a valid candidate. Please correct your ballot before resubmitting it to me. If you are having trouble spelling a candidate\'s name, feel free to use the `{1}candidates` command to view them.\n\n If you feel my assessment of your ballot is an error, please speak with Eylesis#0001 at your earliest convenience!'.format(ctx.author, ctx.prefix))
            votindDB[str(ctx.author.id)] = [candidateName1, candidateName2]
        else:
            return await ctx.send('Apologies {0.mention}, but I found a ballot already entered for you. If you want to change your vote, please run the `{2}clearvotes` command before submitting a new vote.\n\n Your current vote: `{1[0]}` and `{1[1]}`'.format(ctx.author, votingDB[str(ctx.author.id)], ctx.prefix))
            
    @commands.command(pass_context=True)
    async def clearvotes(self, ctx):
        votingDB = self.bot.db.get_val('votingDB', {})
        if str(ctx.author.id) in votingDB:
            del votingDB[str(ctx.author.id)]
            self.bot.db.set_val('votingDB', votingDB)
            return await ctx.send('Greetings {0.mention}! I see you would like you have your ballot removed from my database? I will have this request fulfilled immediately! Please do resumbit a new ballot at your earliest convenience!'.format(ctx.author)) 
        else:
            return await ctx.send('Apologies {0.mention}, but I do not seem to have a ballot for your in my database. Please submit one with the `{1}vote candidateName1 candidateName2` command!'.format(ctx.author, ctx.prefix))

    @commands.command(pass_context=True)
    async def candidates(self, ctx):
        return await ctx.send('Greetings {0.mention}! You wish to view the candidates list? Right away, here is the list!\n\n```css\n[Candidates]\n\n#1) Vanagandr\n#2) UberAffe\n#3) Eylesis\n#4) LightningNevan\n#5) TheEmeraldOtter\n#6) Etheldread\n#7) vareek\n#8) Whiteherrin1584```'.format(ctx.author))

    @commands.command(pass_context=True)
    async def ballotcount(self, ctx):
        if ctx.author.id == 227168575469780992:
            votingDB = self.bot.db.get_val('votingDB', {})
            total = 0
            for userID in votingDB:
                if userID != 'tallies':
                    total += 1 
            percentage = (total / 148) * 100
            return await ctx.send('There have been `{}` ballots cast for this vote. `{}%` of the server has voted so far.'.format(total, round(percentage)))
        else:
            return await ctx.send('Apologies {0.mention}, but you are not permitted to run data display commands at this time! If you feel this is an error, please speak with Eylesis#0001 at your earliest convenience!'.format(ctx.author))
    
    @commands.command(pass_context=True)
    async def tally(self, ctx):
        if ctx.author.id == 227168575469780992:
            votingDB = self.bot.db.get_val('votingDB', {})
            payload = '```css\n[Votes Per Candidate]\n\n'
            candidateNames = []
            candidateTallies = []
            #candidateList = list(votingDB['tallies'].items())
            candidateList = []

            for candidate,value in votingDB['tallies'].items():
                candidateList.append((candidate,len(value)))

            for mx in range(len(candidateList)-1, -1, -1):
                swapped = False
                for i in range(mx):
                    if candidateList[i][1] < candidateList[i+1][1]:
                        candidateList[i], candidateList[i+1] = candidateList[i+1], candidateList[i]
                        swapped = True
                if not swapped:
                    break
            counter = 1
            for candidate in candidateList:
                payload += '#{}) {}: {}\n'.format(counter, candidate[0], candidate[1])
                counter += 1
            payload+= '```'
            await ctx.send(payload)
        else:
            return await ctx.send('Apologies {0.mention}, but you are not permitted to run data display commands at this time! If you feel this is an error, please speak with Eylesis#0001 at your earliest convenience!'.format(ctx.author))
    
def setup(bot):
    bot.add_cog(VotingBooth(bot))
