import os
import urllib.parse
import json
import redis
import discord
from discord.ext import commands

class Database:

    def __init__(self):
        url = urllib.parse.urlparse("redis://rediscloud:9wZPefL0xSWreZPP@redis-11724.c14.us-east-1-3.ec2.cloud.redislabs.com:11724")
        #url = urllib.parse.urlparse(os.environ.get('REDISCLOUD_URL'))
        self.r = redis.Redis(host=url.hostname, port=url.port, password=url.password)
    
    def get_val(self, key):
        if self.r.get(key) is not None:
            return self.r.get(key).decode('utf-8')
        else:
            return ''
    
    def set_val(self, key, value):
        return self.r.set(key, value.encode('utf-8'))
    #def exists(self, key):

    def delete(self, key):
        return self.r.delete(key)

    def to_json(self, value):
        return json.dumps(value)

    def from_json(self, json_string : str):
        return json.loads(json_string)