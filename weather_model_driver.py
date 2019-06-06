#!/usr/bin/env python3
import argparse
import os, sys
from pprint import pprint
from Helpers.Config import Config
from Preprocess.weather_history import gather_weather, check_weather
from Preprocess.usage_processing import process_usage_input
from ProcessForNN.process_to_nn import process_data_to_nn
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
parser.add_argument("-g","--gather-weather",dest="gather_weather",
    help="Gather data from Dark Sky up to the current date.",
    action="store_true", default=False )
parser.add_argument("-u","--process-input-usage",dest="process_input_usage",
    help="Process an input file of usage data to match weather data.",
    action="store_true", default=False )
parser.add_argument("-w","--check-weather",dest="check_weather_data",
    help="Check the weather data for valid values.",
    action="store_true", default=False )
parser.add_argument("-p","--process-data-to-nn",dest="process_data_to_nn",
    help="Process the weather and usage data to files ready for nn input.",
    action="store_true", default=False)
parms = parser.parse_args()
num_processing_steps = 0

if __name__ == "__main__":
    if parms.verbose:
        print("Start weather and energy processing")
    cwd = os.getcwd()
    start_config = Config(cwd,"weather.cfg")
    start_config["verbose"] = parms.verbose

    if parms.verbose:
        pprint(start_config)

    if parms.gather_weather and num_processing_steps == 0:
        print("Starting to gather the weather.",flush=True)
        gather_weather(start_config)
        num_processing_steps += 1

    if parms.process_input_usage and num_processing_steps == 0:
        print("Starting to process a usage file",flush=True)
        process_usage_input(start_config)
        num_processing_steps += 1

    if parms.check_weather_data and num_processing_steps == 0:
        print("Starting to process a usage file",flush=True)
        check_weather(start_config)
        num_processing_steps += 1

    if parms.process_data_to_nn and num_processing_steps == 0:
        print("Starting to process a usage and weather file for neural net.",flush=True)
        process_data_to_nn(start_config)
        num_processing_steps += 1
