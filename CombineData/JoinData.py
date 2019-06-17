#!/usr/bin/env python3
from Helpers.Config import Config
from copy import deepcopy
from pprint import pformat,pprint
import collections
import pandas as pd
import os, sys
import shutil
from pathlib import Path
#
class JoinData(collections.MutableMapping):
    """
    Purpose:  This class manages the usage calculations from existing 
    smart meter data.
    """
    def __init__(self,cfg:Config):
        self.data = dict()
        self.data["cfg"] = deepcopy(cfg)  # notice the deep copy for this item

    #  Overloads so that it acts kinda like a dictionary
    def __getitem__(self,key:str) -> str:
        try:
            return self.data[self.__keytransform__(key)]
        except KeyError as e:
            print("Key error {} : {}".format(e,self.__keytransform__(key)))
    def __setitem__(self,key:str,value):
        self.data[self.__keytransform__(key)] = value
    def __delitem__(self,key:str):
        del self.data[self.__keytransform__(key)]
    def __len__(self):
        return len(self.data)
    def __keytransform__(self, key:str) -> str:
        return key.lower()
    def __iter__(self):
        return iter(self.data)
    def __repr__(self):
        return pformat(self.state())
    #  General functions
    def state(self):
        return {"keys":self.data.keys(), "configuration":self["cfg"]}
    #  Initialize the pandas
    def __set_pp_usage_data_panda__(self):
        """Sets up a pandas for processing usage

            The processing can not proceed without this file.
        """
        work_usage = None
        try:
            work_usage = pd.read_csv(self["cfg"]["usage_out_file"])
        except FileNotFoundError:
            FileNotFoundError("The preprocessed usage file must exist to process further: {}".format(self["cfg"]["usage_out_file"]))
        if work_usage is not None:
            work_usage.sort_values(["day",'hm'])
            self["cfg"]["pp_usage_data"] = work_usage
            if self["cfg"]["verbose"]:
                print("Using preprocess usage shape: {}x{}".
                format(self["cfg"]["pp_usage_data"].shape[0],self["cfg"]["pp_usage_data"].shape[1]))
                pprint(self["cfg"]["pp_usage_data"].head())
                pprint(self["cfg"]["pp_usage_data"].tail())
                print("",flush=True)
        else:
            print("No Preprocessed Usage Data set!",flush=True)
            sys.exit()
    def __set_pp_weather_data_panda__(self):
        """Sets up a pandas for processing weather 

            Processing cannot proceed without this file
        """
        work_weather = None
        try:
            work_weather = pd.read_csv(self["cfg"]["weather_file"])
        except FileNotFoundError:
            FileNotFoundError("The preprocessed weather file must exist to process further: {}".
            format(self["cfg"]["weather_file"]))
        if work_weather is not None:
            work_weather.sort_values(["day",'hm'])
            self["cfg"]["pp_weather_data"] = work_weather
            if self["cfg"]["verbose"]:
                print("Using preprocess usage shape: {}x{}".
                format(self["cfg"]["pp_weather_data"].shape[0],self["cfg"]["pp_weather_data"].shape[1]))
                pprint(self["cfg"]["pp_weather_data"].head())
                pprint(self["cfg"]["pp_weather_data"].tail())
                print("",flush=True)
        else:
            print("No Preprocessed Weather Data set!",flush=True)
            sys.exit()
    #Gather the usage and weather data
    def gather_preprocessed_usage_weather(self):
        self.__set_pp_usage_data_panda__()
        self.__set_pp_weather_data_panda__()

    #  Perform Basic Conversions
    def join_usage_weather_data(self):
        """Joins the usage and weather data into a single panda
        """
        usage_data = self["cfg"]["pp_usage_data"]
        #Trim the hm column and day column
        usage_data['hm'] = usage_data['hm'].apply(lambda x: x.strip())
        usage_data['day'] = usage_data['day'].apply(lambda x: x.strip())
        weather_data = self["cfg"]["pp_weather_data"]
        weather_data['hm'] = weather_data['hm'].apply(lambda x: x.strip())
        weather_data['day'] = weather_data['day'].apply(lambda x: x.strip())
        self["cfg"]["joined_data"] = pd.merge(usage_data,weather_data,how='inner',on=['day','hm'],copy=True)
        if self["cfg"]["verbose"]:
            print("Joined format.")
            pprint(self["cfg"]["joined_data"].head())
            pprint(self["cfg"]["joined_data"].tail())
    #  Check for uniqueness  (not implemented yet)
    def __check_unique__(self, in_pd: pd.DataFrame) -> bool :
        temp_index = in_pd[["day","hm"]].apply(lambda v: str(v["day"]) + " " + str(v["hm"]), axis=1)
        max_count =temp_index.value_counts().max()
        if max_count > 1:
            num_entries = len(temp_index.value_counts().tolist())
            pprint("Max Count {}".format(max_count))
            pprint("Number unique entries {}".format(num_entries))
            temp_index.value_counts().sort_values(inplace=True)
            pprint(temp_index.tail())
            return False
        else:
            return True
    #  Save the combined data
    def save_combined(self):
        """This saves the updated combined information with the following steps:
        (1)  replace any existing joined data file with the latest joined data file
        (2)  reads in any existing usage file into a panda
        (3)  appends the data to the existing usage data
        (4)  writes the usage data back out

        """
        outfile = self["cfg"]["joined_usage_weather_data"]
        output_data = self["cfg"]["joined_data"]
        output_data.to_csv(outfile,index=False)

