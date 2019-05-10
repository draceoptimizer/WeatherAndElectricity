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
from Usage.UsageManagement import UsageManagement
"""
Purpose:  Process input usage data into data that is in a format consistent with weather data
"""
def process_usage_input(config: Config):
        print("Starting to process usage data.")
        print("================{}==============".format(datetime.today()))
        print(config["verbose"])
        sys.stdout.flush()
        ud = UsageManagement(config)
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
        