import json
import re

from discord.ext import commands
import markovify
import random
from util_functions import discord_trim
from parse import parse_data_entry


class SpellText(markovify.Text):
    def sentence_split(self, text):
        return re.split(r"\s*\n\n\n\n\s*", text)

class Markov:
    
    def __init__(self, bot):
        self.bot = bot
       
        with open('Settings/spells.json', mode='r') as f:
            spells = json.load(f)
            spells = [s for s in spells if not s.get('source') == "UAMystic"]
        for i, s in enumerate(spells):
            if isinstance(s['text'], list):
                spells[i]['text'] = '\n'.join(s['text'])
        
                
        
        self.spell_title = []
        self.spell_text = SpellText('\n\n\n\n'.join(s['text'] for s in spells))
        for s in spells:
            self.spell_title += s['name'].split(' ')
        self.spell_meta = {'time': [s['time'] for s in spells],
                           'range': [s['range'] for s in spells],
                           'duration': [s['duration'] for s in spells]}
        
        with open('Settings/items.json', 'r') as f:    
            _items = json.load(f)
            items = [i for i in _items if i.get('type') is not '$']
        self.item_name = []
        for s in items:
            self.item_name += s['name'].split(' ')
        print("I MADE IT HERE :D!")
        for i, s in enumerate(items):
            if isinstance(s['text'], list):
                items[i]['text'] = '\n'.join(str(t) for t in s['text'] if t and 'Source:' not in t)
        print("I ALSO MADE IT HERE :D!")
        self.item_text = SpellText('\n\n\n\n'.join(s['text'] for s in items))
        
        
    @commands.group(aliases=['mkv'])
    async def markov(self):
        pass
    
    @markov.command()
    async def spell(self):
        """Generates a random spell."""
        spell = {}
        spell['name'] = ' '.join(random.choice(self.spell_title) for _ in range(random.randint(1, 4)))
        spell['text'] = self.spell_text.make_short_sentence(200)
        spell['level'] = random.choice(['cantrip', '1st level', '2nd level', '3rd level',
                                        '4th level', '5th level', '6th level',
                                        '7th level', '8th level', '9th level'])
        spell['school'] = random.choice(["abjuration", "evocation", "enchantment",
                                         "illusion", "divination", "necromancy",
                                         "transmutation", "conjuration"])
        spell['time'] = random.choice(self.spell_meta['time'])
        spell['range'] = random.choice(self.spell_meta['range'])
        spell['duration'] = random.choice(self.spell_meta['duration'])
        
        a = "{name}, {level} {school}.\n**Casting Time:** {time}\n**Range:** {range}\n**Duration:** {duration}\n{text}".format(**spell)
        for m in discord_trim(a):
            await self.bot.say(m)
            
    @markov.command()
    async def item(self):
        """Generates a random item."""
        item = {}
        item['name'] = ' '.join(random.choice(self.item_name) for _ in range(random.randint(1, 4)))
        item['text'] = self.item_text.make_short_sentence(200)

        a = "**{name}**\n{text}".format(**item)
        for m in discord_trim(a):
            await self.bot.say(m)

def setup(bot):
    bot.add_cog(Markov(bot))