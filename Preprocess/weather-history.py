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
        if i_count %50 == 0:
            print("Number of days of weather information: {}".format(i_count))
        c_date = get_timestamp_from_config(work_config)
        if c_date < last_date:
            weather = get_historical_weather(work_config)
            weather_array = process_weather(weather)
            data_array.extend(weather_array)
        work_config = increment_config_by_one_day(work_config)
        i_count += 1
        current_time = get_timestamp_from_config(work_config)
    print("Number of days of weather information: {}".format(i_count))
    #append the new data to the current panda

    add_weather_pd = pd.DataFrame.from_dict(data_array)
    add_weather_pd = add_weather_pd[get_all_weather_names()]
    weather_pd = weather_pd.append(add_weather_pd,ignore_index=True,sort=False)
    w_columns = weather_pd.columns
    while not (w_columns[0] in get_all_weather_names()):
        weather_pd = weather_pd.drop(w_columns[0],axis=1)
        w_columns = weather_pd.columns
    weather_pd.to_csv(weather_file_name,na_rep="-1")
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

