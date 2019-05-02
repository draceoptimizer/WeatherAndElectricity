#!/usr/bin/env python3
'''
    Purpose:  These routines are designed to build the Dark Sky calls
'''
import sys
import requests
import json
from pprint import pprint
from Helpers.Config import Config
# from date_management import *
#
def build_forecast_request(config:Config) -> str:
    '''
        Purpose:  This function build a Dark Sky forecast request to get current information
        It is mainly focused on a limited set of information

        Inputs:  config is a json dictionary with the website, key, lat and long information

        Outputs:  A string that contains the https request for current weather information
    '''
    excludes="minutely,hourly,daily,alerts,flags"
    try:
        url = "{}/{}/{},{}?exclude=\"{}\"".format(config["website"],
            config["key"],
            config["latitude"],config["longitude"],
            excludes)
    except TypeError as e:
        pprint("The input variable should be a dictionary")
        pprint(e)
        sys.exit()
    except AttributeError as e:
        pprint("The attributes are incorrect")
        pprint(e)
        sys.exit()
    return url
#
def build_historical_request(config):
    '''
        Purpose:  This function build a Dark Sky forecast request to get current information
        It is mainly focused on a limited set of information

        Inputs:  config is a json dictionary with the website, key, lat and long information

        Outputs:  A string that contains the https request for current weather information
    '''
    excludes="currently,daily,alerts,flags"
    try:
        cur_date = "{:04d}-{:02d}-{:02d}T00:00:00".format(config["year"],
            config["month"],config["day"])
        url = "{}/{}/{},{},{}?exclude=\"{}\"".format(config["website"],
            config["key"],
            config["latitude"],config["longitude"],cur_date,
            excludes)
    except TypeError as e:
        pprint("The input variable should be a dictionary")
        pprint(e)
        sys.exit()
    except AttributeError as e:
        pprint("The attributes are incorrect")
        pprint(e)
        sys.exit()
    return url
#
def get_location_timezone(config):
    '''
    Purpose:  Use a call to Dark Sky to get the current time zone

    Inputs:  config is a dictionary with the website, key, lat and long information

    Outputs:  A string with the canonical time zone information extracted from the current weather information
    '''
    url = build_forecast_request(config)
    result = None
    try:
        result = requests.get(url)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        pprint(e)
        sys.exit(1)
    forecast = result.json()
    return forecast['timezone']
#
def get_current_weather(config):
    '''
    Purpose:  Use a call to Dark Sky to the the current weather

    Inputs:  config is a dictionary with the website, key, lat and long information

    Outputs:  A json object with the current weather
    '''
    url = build_forecast_request(config)
    result = None
    try:
        result = requests.get(url)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        pprint(e)
        sys.exit(1)
    return result.json()
#
def get_historical_weather(config):
    url = build_historical_request(config)
    result = None
    try:
        result = requests.get(url)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        pprint(e)
        sys.exit(1)
    try:
        return result.json()
    except e:
        pprint(e)
        pprint(result)
        pprint(url)
        sys.exit(1)