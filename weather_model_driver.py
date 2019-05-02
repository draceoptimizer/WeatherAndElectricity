#!/usr/bin/env python3
import argparse
import os
from pprint import pprint
from Helpers.Config import Config
from Preprocess.weather_history import gather_weather
"""
Purpose:  This driver allows selection of options for processing the data
for the weather and electricity usage models.

Required Files:
./weather.cfg - contains the basic configuration information for processing

"""
#  Set up the arg parsing
parser = argparse.ArgumentParser()
parser.add_argument("-v","--verbose",dest="verbose",
    help="Increase the verbosity (no effect now)",
    action="store_true", default=False )
parser.add_argument("--gather-weather",dest="gather_weather",
    help="Increase the verbosity (no effect now)",
    action="store_true", default=False )
parms = parser.parse_args()
num_processing_steps = 0

if __name__ == "__main__":
    if parms.verbose:
        print("Start weather and energy processing")
    cwd = os.getcwd()
    start_config = Config(cwd,"weather.cfg")
    start_config.verbose = parms.verbose

    if parms.verbose:
        pprint(start_config)

    if parms.gather_weather and num_processing_steps == 0:
        gather_weather(start_config)

