import discord
from discord.ext import commands
import urllib.request
import json

class Weather():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def weather(self, ctx, location=""):
        """Prints the town's weather."""
        
        await self.bot.say(embed=get_weather(location))
        await self.bot.delete_message(ctx.message)

def get_weather(location=""):

    with open('weather_settings.json', encoding="utf8") as weather_settings_data:
        weather_settings = json.load(weather_settings_data)   
    if location == "":
        url = "http://forecast.weather.gov/MapClick.php?" + weather_settings['location'] + "&FcstType=json"
    else:
        url = "http://forecast.weather.gov/MapClick.php?" + location + "&FcstType=json"
        

    with urllib.request.urlopen(url) as response:
        raw_weather_data = json.load(response)
    raw_weather_data = raw_weather_data['currentobservation']
    
    if location != "":
        weather_settings['town'] = raw_weather_data['name']

    weather = raw_weather_data['Weather'].lower()
    precipitation_stage = 1
       
    try:
        weather = weather_settings['friendly_weather'][weather]
    except Exception as e:
        print("No matching friendly weather found for "+weather+". Using given value.")    

    if weather == "clear skies":
        precipitation_stage = 1
    if weather == "partly cloudy skies":
        precipitation_stage = 2
    if weather=="foggy" or weather=="overcast skies" or weather == "mostly cloudy skies":
        precipitation_stage = 3
    if weather == "light snow" or weather == "light rain" or weather == "light snow, fog" or weather == "light rain" or weather == "light rain, fog" or weather == "moderate rain, fog":
        precipitation_stage = 4

    real_temp = raw_weather_data['Temp']
    temp = (round(int(real_temp)/5)*5)
    temp_c = str(int((int(real_temp)-32)*(5/9)))
    temperature_stage=1
    qual_temperature=""
       
    if temp <= 0:
        qual_temperature = "dangerously cold"
        temperature_stage = 6
    elif temp < 40:
        qual_temperature = "cold"
        temperature_stage = 5
    elif temp < 50:
        qual_temperature = "cool"
        temperature_stage = 4
    elif temp < 80:
        qual_temperature = "warm"
        temperature_stage = 3
    elif temp < 100:
        qual_temperature = "hot"
        temperature_stage = 2
    else:
        qual_temperature = "unbearably hot"
        temperature_stage = 1
       
    temp = str(temp)

    wind_speed = raw_weather_data['Winds']

    if wind_speed == "NA":
        wind_speed = 0
    else:
        wind_speed = int(wind_speed)
       
    wind_stage = 0
    real_wind_speed = str(wind_speed)
       
    if wind_speed < 1:
        wind_speed = "calm winds"
        wind_stage = 1
    elif wind_speed < 7:
        wind_speed = "light breeze"
        wind_stage = 1
    elif wind_speed < 24:
        wind_speed = "moderate breeze"
        wind_stage = 2
    elif wind_speed < 31:
        wind_speed = "strong breeze"
        wind_stage = 2
    elif wind_speed < 38:
        wind_speed = "strong wind"
        wind_stage = 3
    elif wind_speed < 46:
        wind_speed = "gale"
        wind_stage = 4
    elif wind_speed < 54:
        wind_speed = "severe gale"
        wind_stage = 5
    else:
        wind_speed = "hurricane force winds"
        wind_stage = 5
       
    wind_gusts = raw_weather_data['Gust']
    wind_val = raw_weather_data['Windd']
    if wind_val == "NA":
        wind_val = "0"
    else:
        wind_val = int((int(wind_val)/22.5)+.5)
    wind_direction = weather_settings['friendly_wind_direction'][wind_val%16]

    weather_string = "The weather in {} is currently {}, with {}, and a temperature of around {} degrees.".format(weather_settings['town'], qual_temperature, weather, temp)
    if wind_speed=="calm winds":
         weather_string+=" The wind is currently calm."
    else:
        weather_string += " There is a {} out of the {}.".format(wind_speed, wind_direction)

    embed = discord.Embed(title="Weather", 
                      description=weather_string,)
    embed.set_thumbnail(url="http://forecast.weather.gov/newimages/medium/{}".format(raw_weather_data['Weatherimage']))
    embed.set_footer(text="Weather Stages: {} Wind, {} Temperature, {} Precipitation".format(wind_stage, temperature_stage, precipitation_stage))
    if wind_stage >= 3:
           embed.add_field(name="Strong Wind", value=weather_settings['strong_wind'])
    if temperature_stage==6:
            embed.add_field(name="Extreme Cold", value=weather_settings['extreme_cold'])
    if temperature_stage==1:
            embed.add_field(name="Extreme Heat", value=weather_settings['extreme_heat'])
    if precipitation_stage >= 5:
            embed.add_field(name="Heavy Precipition", value=weather_settings['heavy_precipitation'])
    
    return embed   


def setup(bot):
    bot.add_cog(Weather(bot))