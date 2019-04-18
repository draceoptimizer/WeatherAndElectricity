#!/usr/bin/env python3
import requests
from pprint import pprint
import datetime as dt
from dateutil import tz

start_month = 5
start_day = 1
start_year = 2017
end_month = 5
end_day = 1
end_year = 2017
user_key = "e0c47993d5f64a030a76b8208ae2ab56"
user_lat = "32.842685"
user_long = "-96.653671"
website = "https://api.darksky.net/forecast"
cur_date = "{}-{:02d}-{:02d}T00:00:00".format(start_year,start_month,start_day)
from_zone = tz.tzutc()
to_zone = tz.gettz("America/Chicago")

full_command = website + "/" + user_key + "/" + user_lat + "," + user_long + "," + cur_date + "?exclude=currently,daily,flags"
print(full_command)
r = requests.get(full_command)
forecast = r.json()
pprint(forecast)
for i in range(24):
    cur_time = forecast["hourly"]["data"][i]["time"]
    time_zone = forecast['timezone']
    to_zone = tz.gettz(time_zone)
    local_time = dt.datetime.fromtimestamp(cur_time,to_zone).strftime("%Y/%m/%d %H:%M")
    print(local_time)
