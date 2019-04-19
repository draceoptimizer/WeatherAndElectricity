#!/usr/bin/env python3
from datetime import date
import datetime as dz
from dateutil import tz
import time as tm

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
    to_zone = tz.gettz(in_zone)
    local_time = dz.datetime.fromtimestamp(in_linux_timestamp,to_zone).strftime("%Y/%m/%d %H:%M")
    local_time = local_time.split()
    day = local_time[0]
    t = local_time[1]
    return day, t
