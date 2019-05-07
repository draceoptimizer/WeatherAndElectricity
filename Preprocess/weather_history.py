#!/usr/bin/env python3
import sys
import time
from datetime import datetime, date, timedelta
import requests
import json
import datetime as dt
import pandas as pd
from pprint import pprint
from Helpers.date_management import *
from Preprocess.dark_sky_management import *
from Preprocess.weather_processing import *
from Helpers.Config import Config
from Weather.WeatherManagement import WeatherManagement

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

#  Default values
def gather_weather(config:Config):
    while True:
        print("Starting to gather weather data.")
        print("================{}==============".format(datetime.today()))
        sys.stdout.flush()
        gw = WeatherManagement(config)
        gw.set_weather_panda()
        gw.set_weather_gather_start_date()
        max_days = gw["cfg"]["max_number_requests"]
        weather = get_historical_weather(gw["cfg"])
        time_zone = weather["timezone"]
        gw["cfg"]["time_zone"] = time_zone
        data_array = []
        last_date = date.today() - timedelta(days=1)
        last_date = dt.datetime(last_date.year,last_date.month,last_date.day).timestamp()
        current_time = gw["cfg"].get_timestamp()
        print("Gathering additional Weather Data")
        print("\t{}".format(current_time))
        print("\t{}".format(last_date))
        icount = 0
        while current_time < last_date:
            if icount%50 == 0:
                print("Number of days added to weather information: {}".format(icount))
            c_date = gw["cfg"].get_timestamp()
            if c_date < last_date:
                weather = get_historical_weather(gw["cfg"])
                weather_array = process_weather(weather)
                data_array.extend(weather_array)
            gw["cfg"].increment_config_by_one_day()
            current_time = gw["cfg"].get_timestamp()
            icount += 1
        print("Number of days of weather information: {}".format(icount))
        print(len(data_array))
        gw.add_additional_weather(weather_array)
        gw.save_weather()
        print("Collected {} days of weather.".format(icount))
        print("--------------{}-------------".format(datetime.today()))
        print("Sleeping to not try too much per day (per Dark Sky)")
        time.sleep(60 * 60)

