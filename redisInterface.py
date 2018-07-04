import os
import urllib.parse
import json
import redis
import discord
from discord.ext import commands

class Database:

    def __init__(self):
        url = urllib.parse.urlparse(os.environ.get('REDISCLOUD_URL'))
        self.r = redis.Redis(host=url.hostname, port=url.port, password=url.password)
    
    def get_val(self, key):
        if self.r.get(key) is not None:
            return self.r.get(key).decode('utf-8')
        else:
            return 0
    
    def set_val(self, key, value):
        return self.r.set(key, value.encode('utf-8'))

    def delete(self, key):
        return self.r.delete(key)

    def to_json(self, value):
        return json.dumps(value)

    def from_json(self, json_string : str):
        return json.loads(json_string)