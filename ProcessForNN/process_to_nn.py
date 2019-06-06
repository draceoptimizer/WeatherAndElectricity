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
from Helpers.Config import Config
from CombineData.JoinData import JoinData
"""
Purpose:  Process input usage data into data that is in a format consistent with weather data
"""
def process_data_to_nn(config: Config):
        print("Starting to process data for Neural Net AI.")
        print("================{}==============".format(datetime.today()))
        print(config["verbose"])
        if config["verbose"]:
            print("Preprocessed usage file name: {}".format(config["usage_out_file"]))
            print("Preprocessed weather in file name: {}".format(config["weather_file"]))
        sys.stdout.flush()
        sys.exit()
        jd = JoinData(config)
        ud.set_usage_in_panda()
        ud.basic_conversions()
        ud.sum_kwh()
        ud.save_usage()
        if config["verbose"]:
            print("Changing the USAGE DATE format.")
            pprint(ud["usage_processed"].head())
            pprint(ud["usage_processed"].tail())
            pprint(ud["cfg"]["usage_in_file"])
            pprint(ud["cfg"]["usage_out_file"])
        