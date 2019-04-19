#!/usr/bin/env python3
from Preprocess.date_management import *
from copy import deepcopy
import pandas as pd
from pprint import pprint
"""Functions to provide weather processing

"""
weather_time_names = ['time','day','hm','tz']
#
def get_weather_data_names():
    """Returns the weather data names
    The names are defined in this function to keep the list private

    Input:  None

    Output: the array of weather data names
    """
    return ['dewPoint','humidity','precipIntensity',
        'pressure','temperature','uvIndex','visibility',
        'windBearing','windGust','windSpeed']
#
def get_weather_time_names():
    """
    Purpose:  Return the weather time names

    Input:  None

    Output:  the array of weather time names
    """
    return ['time','day','hm','tz']
#
def get_all_weather_names():
    return  get_weather_time_names() + get_weather_data_names()
#
def process_weather(weather):
    """
    Purpose:  Process the data into a format that can add the data to
    a pandas table

    Inputs:  weather is a dictionary that contains historical weather data 
    a particular date.

    Output:
    out_array is an array of the hourly weather for a lat/long with date and time
    in local time as defined by the timezone

    """
    interesting_data = get_weather_data_names()
    out_array = []
    time_zone = weather['timezone']
    work_data = weather['hourly']['data']
    for w in work_data:
        c_time = w['time']
        l_day, l_time = to_local_time(c_time,time_zone)
        keep_data = True
        res = {'time': c_time,
            'day': l_day,
            'hm':l_time,
            'tz':time_zone
        }
        for n in interesting_data:
            try:
                res[n] = w[n]
            except:
                res[n] = None
                keep_data = False
        if keep_data:
            out_array.append(res)
    return out_array
#
def get_weather_panda(weather_file=None):
    """
    Purpose:  Returns the panda of the weather file
    If the file doesn't exist, it returns an empty panda with the correct column names
    
    Arguments:

        weather_file {String} -- The name of the weather file
    
    Outputs:
        weather_pd {panda DataFrame} -- the dataframe of the data
    """
    assert weather_file is not None
    work_weather = None
    try:
        work_weather = pd.read_csv(str(weather_file))
    except FileNotFoundError as e:
        print("Building a default panda DataFrame")
        all_columns = get_all_weather_names()
        work_weather = pd.DataFrame(columns=all_columns)
    work_weather.sort_values(["time"])
    return work_weather
#
def get_weather_start_config(in_pd=None, config=None):
    """
    Purpose:  obtain the starting date for getting new data from the weather file
    
    Keyword Arguments:
        in_pd {pandas} -- the pandas of the weather data (default: {None})
        config {dictionary} -- the dictionary of the processing controls (default: {None})
    """
    assert in_pd is not None
    assert config is not None
    df_shape = in_pd.shape
    num_rows = df_shape[0]
    work_config = None
    if num_rows == 0:
        work_config = deepcopy(config)
        work_config["year"] = work_config["start_year"]
        work_config["month"] = work_config["start_month"]
        work_config["day"] = work_config["start_day"]
        return work_config
    else:
        work_config = deepcopy(config)
        last_data = in_pd[-1]
        day_val = last_data["day"]
        all_vals = day_val.split("-")
        work_config["year"] = all_vals[0]
        work_config["month"] = all_vals[1]
        work_config["day"] = all_vals[2]
        return work_config
