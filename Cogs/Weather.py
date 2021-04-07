import discord
import asyncio
from discord.ext import commands
import urllib.request
import json
from Cogs.GameTime import get_gametime
from Cogs.GameTime import get_rawtime

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def weather(self, ctx, location=""):
        """Prints the town's weather."""
        await self.ctx.send(embed=get_weather(location))
        await self.ctx.message.delete()

def get_raw_weather_data(location=""):
    with open('Settings/weather_settings.json', encoding="utf8") as weather_settings_data:
        weather_settings = json.load(weather_settings_data)   
    if location == "":
        url = "http://forecast.weather.gov/MapClick.php?" + weather_settings['location'] + "&FcstType=json"
    else:
        url = "http://forecast.weather.gov/MapClick.php?" + location + "&FcstType=json"
        

    with urllib.request.urlopen(url) as response:
        raw_weather_data = json.load(response)
    return raw_weather_data['currentobservation']

def get_precipitation_stage(weather: str):
    precipitation_stage = 1
    if weather == "clear skies":
        precipitation_stage = 1
    if weather == "partly cloudy skies":
        precipitation_stage = 2
    if weather=="foggy" or weather=="fog" or weather=="haze" or weather=="overcast skies" or weather == "mostly cloudy skies":
        precipitation_stage = 3
    if weather == "light snow" or weather == "light rain" or weather == "light snow, fog" or weather == "light rain" or weather == "light rain, fog" or weather == "moderate rain, fog":
        precipitation_stage = 4
    return precipitation_stage

def get_temperature_stage(temp : int):
    temp_data = {}
    if temp <= 0:
        temp_data['qual_temperature'] = "dangerously cold"
        temp_data['temperature_stage'] = 6
    elif temp < 40:
        temp_data['qual_temperature'] = "cold"
        temp_data['temperature_stage'] = 5
    elif temp < 50:
        temp_data['qual_temperature'] = "cool"
        temp_data['temperature_stage'] = 4
    elif temp < 80:
        temp_data['qual_temperature'] = "warm"
        temp_data['temperature_stage'] = 3
    elif temp < 100:
        temp_data['qual_temperature'] = "hot"
        temp_data['temperature_stage'] = 2
    else:
        temp_data['qual_temperature'] = "unbearably hot"
        temp_data['temperature_stage'] = 1
    return temp_data

def get_wind_stage(wind_speed : str):
    wind_data = {}
    if wind_speed == "NA":
        wind_speed = 0
    else:
        wind_speed = int(wind_speed)
    wind_stage = 0
       
    if wind_speed < 1:
        wind_data['wind_speed'] = "calm winds"
        wind_data['wind_stage'] = 1
    elif wind_speed < 7:
        wind_data['wind_speed'] = "light breeze"
        wind_data['wind_stage'] = 1
    elif wind_speed < 24:
        wind_data['wind_speed'] = "moderate breeze"
        wind_data['wind_stage'] = 2
    elif wind_speed < 31:
        wind_data['wind_speed'] = "strong breeze"
        wind_data['wind_stage'] = 2
    elif wind_speed < 38:
        wind_data['wind_speed'] = "strong wind"
        wind_data['wind_stage'] = 3
    elif wind_speed < 46:
        wind_data['wind_speed'] = "gale"
        wind_data['wind_stage'] = 4
    elif wind_speed < 54:
        wind_data['wind_speed'] = "severe gale"
        wind_data['wind_stage'] = 5
    else:
        wind_data['wind_speed'] = "hurricane force winds"
        wind_data['wind_stage'] = 5
    return wind_data

def get_weather(location=""):
    with open('Settings/weather_settings.json', encoding="utf8") as weather_settings_data:
        weather_settings = json.load(weather_settings_data)

    raw_weather_data = get_raw_weather_data(location)
    
    if location != "":
        weather_settings['town'] = raw_weather_data['name']

    weather = raw_weather_data['Weather'].lower()
    try:
        weather = weather_settings['friendly_weather'][weather]
    except Exception as e:
        print("No matching friendly weather found for "+weather+". Using given value.") 
    precipitation_stage = get_precipitation_stage(weather)
    
    temp = (round(int(raw_weather_data['Temp'])/5)*5)
    temp_data = get_temperature_stage(temp)

    wind_speed = raw_weather_data['Winds']
    wind_data = get_wind_stage(wind_speed)   
   
       
    wind_gusts = raw_weather_data['Gust']
    wind_val = raw_weather_data['Windd']
    if wind_val == "NA":
        wind_val = "0"
    else:
        wind_val = int((int(wind_val)/22.5)+.5)
    wind_direction = weather_settings['friendly_wind_direction'][wind_val%16]

    weather_string = "The weather in {} is currently {}, with {}, and a temperature of around {} degrees.".format(
                                                                                                                weather_settings['town'], 
                                                                                                                temp_data['qual_temperature'], 
                                                                                                                weather, 
                                                                                                                temp)
    if wind_data['wind_speed']=="calm winds":
         weather_string+=" The wind is currently calm."
    else:
        weather_string += " There is a {} out of the {}.".format(wind_data['wind_speed'], wind_direction)
    if temp < 70:    
        weather_string += "\n\nOutside the city walls, the temperature is around {} degrees.".format(str(temp-10))

    embed = discord.Embed(title="Weather", 
                      description=weather_string)
    embed.set_thumbnail(url="http://forecast.weather.gov/newimages/medium/{}".format(raw_weather_data['Weatherimage']))
    embed.add_field(name="Weather Stages", value="{} Wind, {} Temperature, {} Precipitation".format(wind_data['wind_stage'], temp_data['temperature_stage'], precipitation_stage))
    embed.set_footer(text=get_gametime())
    
    if wind_data['wind_stage'] >= 3:
           embed.add_field(name="Strong Wind", value=weather_settings['strong_wind'])
    if temp_data['temperature_stage'] == 6:
            embed.add_field(name="Extreme Cold", value=weather_settings['extreme_cold'])
    if temp < 10:
            embed.add_field(name="Extreme Cold: Outside Neverwinter", value=weather_settings['extreme_cold'])
    if temp_data['temperature_stage'] == 1:
            embed.add_field(name="Extreme Heat", value=weather_settings['extreme_heat'])
    if precipitation_stage >= 5:
            embed.add_field(name="Heavy Precipition", value=weather_settings['heavy_precipitation'])
    
    return embed

    

def metric(d):
    return int((int(d)-32)*(5/9))

def setup(bot):
    bot.add_cog(Weather(bot))
    