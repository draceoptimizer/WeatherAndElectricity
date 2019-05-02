#!/usr/bin/env python3
from datetime import date, timedelta
import datetime as dz
from dateutil import tz
import time as tm
from copy import deepcopy
#
from Helpers.Config import Config
"""Routines to support date and time manipulation for weather processing

These routines have a Config object as input, then use standard date/time
functions to extract the correct information.
 
"""
def extract_date_time_str(config:Config) -> str:
    '''
    Purpose:  Simple routine to return a string from integer year, month and day

    Input:
        config - a Config object with year, month and day

    Output:
        String in the format YYYY-MM-DD
    '''
    assert isinstance(config,Config)
    return extract_date(config).isoformat()
#
def extract_date_time_zero_hr(config:Config) -> str:
    '''
    Purpose:  Simple routine to return a string from integer year, month and day

    Input:
        config - a dictionary with year, month and day

    Output:
        String in the format YYYY-MM-DD
    '''
    assert isinstance(config,Config)
    return extract_date(config).ctime()
#
def extract_date(config:Config) -> date:
    '''
    Purpose:  Simple routine to return a string from integer year, month and day

    Input:
        yr - an integer for the year
        mon - an integer for the month
        day - an integer for the day of the month

    Output:
        String in the format YYYY-MM-DD
    '''
    assert isinstance(config,Config)
    year, month, day = config.get_ymd()
    return date(year,month,day)
#
def to_local_time(in_linux_timestamp=None, in_zone=None):
    '''
    Purpose:  Return the local time information with date, hour and minute

    Input:  
    in_linux_timestamp is the linux time since the epoch in UTC
    in_zone is the local time zone in common words

    Output:
    day - A string in the form YYYY-m-d
    t - A string in the form HH:MM
    '''
    to_zone = tz.gettz(in_zone)
    local_time = dz.datetime.fromtimestamp(in_linux_timestamp,to_zone).strftime("%Y/%m/%d %H:%M")
    local_time = local_time.split()
    day = local_time[0]
    t = local_time[1]
    return day, t
#
def get_timestamp(config:Config) -> float:
    assert isinstance(config,Config)
    d = extract_date(config)
    return dz.datetime(d.year,d.month,d.day).timestamp()

#
def increment_config_by_one_day(config:Config) -> Config:
    """
    Purpose:  Increment the configuration file date by one day
    
    Keyword Arguments:
        config {dictionary} -- The configuration file to get weather data (default: {None})

    Output:
        An updated config file
    """
    assert isinstance(config,Config)
    new_config = deepcopy(config)
    w_time = extract_date(new_config)
    next_day = w_time + timedelta(days=1)
    new_config.update_ymd(next_day.year,next_day.month,next_day.day)
    return new_config

