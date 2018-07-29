import os
import urllib.parse
import json
import redis
import discord
from discord.ext import commands

class Database:

    def get_val(self, key, default=None):
        path = f"{self.path}{key}.json"
        if not os.path.exists(path):
            return default
        else:
            with open(path) as f:
                data = json.load(f)
            return data

    def set_val(self, key, value):
        path = f"{self.path}{key}.json"
        with open(path, 'w') as f:
            json.dump(value, f)

    def ensure_path_exists(path):
        if not os.path.exists(path):
            os.makedirs(path)
            
    def __init__(self, path='data/'):
        self.path = path
        ensure_path_exists(path)