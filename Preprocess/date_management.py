#!/usr/bin/env python3
from datetime import date, timedelta
import datetime as dz
from dateutil import du
import time as tm
from copy import deepcopy

def to_date_time_str(config=None):
    '''
    Purpose:  Simple routine to return a string from integer year, month and day

    Input:
        config - a dictionary with year, month and day

    Output:
        String in the format YYYY-MM-DD
    '''
    assert config is not None
    return date(config["year"],config["month"],config["day"]).isoformat()
#
def to_date_time_zero_hr(config):
    '''
    Purpose:  Simple routine to return a string from integer year, month and day

    Input:
        config - a dictionary with year, month and day

    Output:
        String in the format YYYY-MM-DD
    '''
    assert config is not None
    return to_date_time(config).ctime()
#
def to_date_time(config=None):
    '''
    Purpose:  Simple routine to return a string from integer year, month and day

    Input:
        yr - an integer for the year
        mon - an integer for the month
        day - an integer for the day of the month

    Output:
        String in the format YYYY-MM-DD
    '''
    assert config is not None
    return date(config["year"],config["month"],config["day"])
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
    to_zone = du.gettz(in_zone)
    local_time = dz.datetime.fromtimestamp(in_linux_timestamp,to_zone).strftime("%Y/%m/%d %H:%M")
    local_time = local_time.split()
    day = local_time[0]
    t = local_time[1]
    return day, t
#
def get_date_from_config(config=None):
    assert config is not None
    year = config["year"]
    month = config["month"]
    day = config["day"]
    return date(year,month,day)
#
def get_timestamp_from_config(config=None):
    assert config is not None
    d = get_date_from_config(config)
    return dz.datetime(d.year,d.month,d.day).timestamp()

#
def increment_config_by_one_day(config=None):
    """
    Purpose:  Increment the configuration file date by one day
    
    Keyword Arguments:
        config {dictionary} -- The configuration file to get weather data (default: {None})

    Output:
        An updated config file
    """
    assert config is not None
    new_config = deepcopy(config)
    w_time = get_date_from_config(new_config)
    next_day = w_time + timedelta(days=1)
    new_config["year"]=next_day.year
    new_config["month"]=next_day.month
    new_config["day"] = next_day.day
    return new_config

