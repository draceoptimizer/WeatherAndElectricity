#!/usr/bin/env python3
import requests
import json
import datetime
from pprint import pprint
from copy import deepcopy
from Preprocess.date_management import *
from Preprocess.dark_sky_management import *

def process_weather(weather):
    '''
    Purpose:  Process the data into a format that can add the data to
    a pandas table

    Inputs:  weather is a dictionary that contains historical weather data 
    a particular date.

    Output:
    out_array is an array of the hourly weather for a lat/long with date and time
    in local time as defined by the timezone

    '''
    interesting_data = ['dewPoint','humidity','precipIntensity',
        'pressure','temperature','uvIndex','visibility',
        'windBearing','windGust','windSpeed']
    out_array = []
    time_zone = weather['timezone']
    work_data = weather['hourly']['data']
    for w in work_data:
        c_time = w['time']
        l_day, l_time = to_local_time(c_time,time_zone)
        res = {'time': c_time,
            'day': l_day,
            'hm':l_time,
            'tz':time_zone
        }
        for n in interesting_data:
            res[n] = w[n]
        out_array.append(res)
    return out_array

config_file = "../weather.cfg"

if __name__ == "__main__":
    config_data = None
    with open(config_file) as json_data_file:
        config_data = json.load(json_data_file)
    
    work_config = deepcopy(config_data)
    work_config["year"] = work_config["start_year"]
    work_config["month"] = work_config["start_month"]
    work_config["day"] = work_config["start_day"]
    start_date_str = to_date_time_str(work_config)
    zero_time_start_date_str = to_date_time_zero_hr(work_config)
    dt = to_date_time(work_config)
    # for i in range(35):
    #     ndt = dt + datetime.timedelta(days=i)
    #     pprint(ndt)
    weather = get_historical_weather(work_config)
    time_data = process_weather(weather)
    for t in time_data:
        pprint(t)

# start_month = 5
# start_day = 1
# start_year = 2017
# end_month = 5
# end_day = 1
# end_year = 2017
# user_key = "e0c47993d5f64a030a76b8208ae2ab56"
# user_lat = "32.842685"
# user_long = "-96.653671"
# website = "https://api.darksky.net/forecast"
# cur_date = "{}-{:02d}-{:02d}T00:00:00".format(start_year,start_month,start_day)
# from_zone = tz.tzutc()
# to_zone = tz.gettz("America/Chicago")

# full_command = website + "/" + user_key + "/" + user_lat + "," + user_long + "," + cur_date + "?exclude=currently,daily,flags"
# print(full_command)
# r = requests.get(full_command)
# forecast = r.json()
# pprint(forecast)
# for i in range(24):
#     cur_time = forecast["hourly"]["data"][i]["time"]
#     time_zone = forecast['timezone']
#     to_zone = tz.gettz(time_zone)
#     local_time = dt.datetime.fromtimestamp(cur_time,to_zone).strftime("%Y/%m/%d %H:%M")
#     print(local_time)
