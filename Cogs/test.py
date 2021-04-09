import time
from datetime import date, datetime, timedelta
import pytz

# aDate = datetime(2020, 10, 18)
# bDate = datetime.now()
# delta = bDate - aDate

# new_date = datetime(2020, 10, 18, bDate.hour, bDate.minute, bDate.second) + timedelta(days=delta.days*3) + (timedelta(days=(bDate.hour//8-2)))
# print(bDate.hour//8)
# print(new_date)

def suffix(d):
        return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

months = [
    "Hammer",
    "Alturiak",
    "Ches",
    "Tarsakh",
    "Mirtul",
    "Kythorn",
    "Flamerule",
    "Eleasis",
    "Eleint",
    "Marpenoth",
    "Uktar",
    "Nightal"]
    
aDate = datetime(2020, 10, 18, tzinfo=pytz.timezone('UTC'))
bDate = datetime.now(pytz.timezone('UTC'))
delta = bDate - aDate

gametime = datetime(2020, 10, 18, bDate.hour, bDate.minute, bDate.second) + timedelta(days=delta.days*3) + (timedelta(days=(bDate.hour//8-2)))

if gametime.hour == 0:
    gametime_hour = 12
    time_decor = "AM"
else:
    gametime_hour = gametime.hour-12 if gametime.hour > 12 else gametime.hour
    time_decor = "PM" if gametime.hour > 12 else "AM"
gametime_minute = "0{}".format(gametime.minute) if gametime.minute < 10 else gametime.minute

print("{}:{} {} UTC | {}{} of {}".format(gametime_hour, gametime_minute, time_decor, gametime.day, suffix(gametime.day), months[gametime.month-1]))