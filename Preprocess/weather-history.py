#!/usr/bin/env python3
import time
from datetime import datetime, date, timedelta

"""Process the weather data up to the current date

Process:
    If weather.txt exists, it reads that into a panda dataframe and add from the last date
    Else, it start from the start date

    It processes a maximum number of days as specified in the config file

Side Effects:
    This updates the weather.txt file with any new data
    weather.txt is a cvs with the following fields
    ['time', 'day','hm','tz','dewPoint','humidity','precipIntensity',
        'pressure','temperature','uvIndex','visibility',
        'windBearing','windGust','windSpeed']
    These fields are mostly self explanatory
"""
import requests
import json
import datetime as dt
import pandas as pd
from pprint import pprint
from copy import deepcopy
from Preprocess.date_management import *
from Preprocess.dark_sky_management import *
from Preprocess.weather_processing import *
#  Default values
config_file = "../weather.cfg"
max_number_day_processes = 10
weather_file_name = "weather.txt"
if __name__ == "__main__":
    config_data = None
    with open(config_file) as json_data_file:
        config_data = json.load(json_data_file)
    max_days = config_data.get("max_number_requests" ,max_number_day_processes)
    weather_file_name = str(config_data.get("weather_file",weather_file_name))
    weather_pd = get_weather_panda(weather_file_name)
    work_config = get_weather_start_config(weather_pd, config_data)
    weather = get_historical_weather(work_config)
    time_zone = weather["timezone"]
    work_config["time_zone"] = time_zone
    data_array = []
    last_date = date.today() - timedelta(days=1)
    last_date = dt.datetime(last_date.year,last_date.month,last_date.day).timestamp()
    i_count = 0
    current_time = get_timestamp_from_config(work_config)
    print(current_time)
    print(last_date)
    while i_count < max_days and current_time < last_date:
        c_date = get_timestamp_from_config(work_config)
        if c_date < last_date:
            weather = get_historical_weather(work_config)
            weather_array = process_weather(weather)
            data_array.extend(weather_array)
        work_config = increment_config_by_one_day(work_config)
        i_count += 1
        current_time = get_timestamp_from_config(work_config)
    #append the new data to the current panda
    add_weather_pd = pd.DataFrame.from_dict(data_array)
    add_weather_pd = add_weather_pd[get_all_weather_names()]
    weather_pd = weather_pd.append(add_weather_pd,ignore_index=True,sort=False)
    w_columns = weather_pd.columns
    while w_columns[0] != 'time':
        weather_pd = weather_pd.drop(w_columns[0],axis=1)
        w_columns = weather_pd.columns
    weather_pd.to_csv(weather_file_name)
    #show the data
    #pprint(data_array)

    # work_config = deepcopy(config_data)
    # work_config["year"] = work_config["start_year"]
    # work_config["month"] = work_config["start_month"]
    # work_config["day"] = work_config["start_day"]
    # start_date_str = to_date_time_str(work_config)
    # zero_time_start_date_str = to_date_time_zero_hr(work_config)
    # dt = to_date_time(work_config)

    # weather = get_historical_weather(work_config)
    # time_data = process_weather(weather)
    # for t in time_data:
    #     pprint(t)

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
