#!/usr/bin/env python3
import json
import os, sys
from pprint import pprint, pformat
from copy import deepcopy
import collections
#  Date/Time imports
from datetime import date, timedelta
import datetime as dz
from dateutil import tz
import time as tm
import glob
"""
Purpose:  General configuration management class so the information can 
be passed around safely

This is written as a MutableMapping so that it acts like a dictionary with additional
features for location, date and time management
"""
class Config(collections.MutableMapping):
    """The class for managing the driving structure information

    This application requires a good bit of input because I prefer not
    deriving information from the current location of a computer.

    """
    #TODO:  Need to update this so it uses hierarchical configuration files:
    #TODO:  Probably these right now:
    #TODO:      general     - These are general knowledge that is shared
    #TODO:      gather      - These are items that are used for gathering weather data
    #TODO:      usage       - These are items that are used to transform raw usage data
    #TODO:      weather_model - These are items that are used to build weather models
    #TODO:      nn          - These are items that are used to transform data suitable for nn modeling of usage
    #TODO:  Probably do this using a v2 capability of the configuration

    #TODO:  Need to replace the use of asserts with checks and logging capabilities, asserts are a little brutal

    def __init__(self,work_dir=None,config_file=None):
        assert work_dir is not None, "The working directory must be provided."
        assert config_file is not None, "The name of the config file must be provided."
        assert os.path.exists(work_dir), "The directory for the config file must exist: {}".format(work_dir)
        cfg_file = os.path.join(work_dir, config_file)
        assert os.path.exists(cfg_file), "The config file must exist: {}".format(cfg_file)
        with open(cfg_file) as json_data_file:
            cfg = json.load(json_data_file)
        #check for required fields
        self.conf = dict()
        #Set some defaults
        self.conf["max_number_requests"] = 2
        self.conf["weather_file"] = "weather.txt"
        self.conf["verbose"] = False
        self.conf["usage_in_file"] = None
        #This is the working year, month day used to control processing
        self.conf["year"] = None
        self.conf["month"] = None
        self.conf["day"] = None
        #Process the input config file
        self.conf["website"] = self.__check_value__(cfg,"website","The website for Dark Sky must be provided.")
        self.conf["key"] = self.__check_value__(cfg,"key","The user key must be provided.")
        self.conf["latitude"] = self.__check_value__(cfg,"latitude","The latitude must be provided.")
        self.conf["longitude"] = self.__check_value__(cfg,"longitude","The longitude must be provided.")
        self.conf["start_month"] = self.__check_value__(cfg,"start_month","The start month must be provided.")
        self.conf["start_day"] = self.__check_value__(cfg,"start_day","The start day must be provided.")
        self.conf["start_year"] = self.__check_value__(cfg,"start_year","The start year must be provided.")
        self.conf["max_number_requests"] = self.__check_value__(cfg,"max_number_requests","The maximum number of requests from Dark Sky must be provided.")
        self.conf["data_directory"] = self.__check_value__(cfg,"data_directory","The data directory must be provided.")
        self.conf["usage_in_directory"] = self.__check_value__(cfg,"usage_in_directory","The input usage directory must be provided.")
        self.conf["processed_directory"] = self.__check_value__(cfg,"processed_directory","The generic processed directory")
        self.conf["weather_file"] = self.__check_value__(cfg,"weather_file","The weather file name must be provided.")
        self.conf["usage_in_file"]=self.__check_value(cfg,"usage_in_file","The usage_in_file was set to default.")
        self.conf["usage_out_file"] = "usage.csv"
        full_data_directory = os.path.join(work_dir,self.conf["data_directory"])
        abs_data_directory = os.path.abspath(full_data_directory)
        assert os.path.exists(abs_data_directory), "The data path must exist: {}.  This does not create it programmatically.".format(abs_data_directory)
        self.conf["data_directory"] = abs_data_directory
        self.conf["weather_file"] = os.path.join(abs_data_directory,self.conf["weather_file"])
        self.conf["usage_out_file"] = os.path.join(abs_data_directory,self.conf["usage_out_file"])
        #Additional processing beyond just the first level default values
        # usage_in_file processing
        if self.conf["usage_in_file"] is None:
            full_usage_in_directory = os.path.join(work_dir,self.conf["usage_in_directory"])
            assert os.path.exists(full_usage_in_directory),"The usage in directory must exist: {}.  This is not created programmatically.".format(full_usage_in_directory)
            full_usage_processed_directory = os.path.join(full_usage_in_directory,self.conf["processed_directory"])
            assert os.path.exists(full_usage_processed_directory), "The usage in processed directory must exist: {}. This is not created programatically.".format(full_usage_processed_directory)
            self.conf["usage_in_processed_directory"] = full_usage_processed_directory
            match_file_name = os.path.join(full_usage_in_directory,"*.csv")
            glob_list = glob.glob(match_file_name)
            self.conf["usage_in_file"] = glob_list[0] if len(glob_list) > 0 else None
            try:
                self.conf["verbose"] = cfg["verbose"]
            except:
                pass

    #
    def __check_value__(self,cfg=None,dict_key=None,msg=None):
        """Checks the values for inputs.
        The logic within this routine requires all of the key/value pairs to be defined otherwise the
        program aborts with the input message.
        
        Keyword Arguments:
            cfg {dict} -- A dictionary of the default values from reading in the config file (default: {None})
            dict_key {str} -- The key to search for in the cfg (default: {None})
            msg {str} -- A message to output upon failure (default: {None})
        
        Returns:
            [type] -- [description]
        """
        assert cfg is not None
        assert dict_key is not None
        assert msg is not None
        #  This first step tries to return the value from the input config file
        try:
            return cfg[dict_key]
        except KeyError:
            #This step returns the value from the default definitions or aborts.  
            #This forces all config key/value pairs to be defined.
            if dict_key in self.conf:
                return self.conf[dict_key]
            else:
                self.__stop_input_processing__(msg)
    #
    def __stop_input_processing__(self, msg=None):
        assert msg is not None
        pprint(msg)
        sys.exit(1)
    #
    def state(self):
        cfg = deepcopy(self.conf)
        return cfg
    #  Overloads so that it acts kinda like a dictionary
    def __getitem__(self,key:str) -> str:
        try:
            return self.conf[self.__keytransform__(key)]
        except KeyError as e:
            print("Key error {} : {}".format(e,self.__keytransform__(key)))
    def __setitem__(self,key:str,value):
        self.conf[self.__keytransform__(key)] = value
    def __delitem__(self,key:str):
        del self.conf[self.__keytransform__(key)]
    def __len__(self):
        return len(self.conf)
    def __keytransform__(self, key:str) -> str:
        return key.lower()
    def __iter__(self):
        return iter(self.conf)
    def __repr__(self):
        return pformat(self.state())
    #
    #  Date Management functions
    #
    def timezone(self):
        return self.conf["timezone"]
    def get_start_ymd(self):
        return self.conf["start_year"], self.conf["start_month"],self.conf["start_day"]
    def get_ymd(self):
        return self.conf["year"], self.conf["month"],self.conf["day"]
    def update_ymd(self,yr=None, mon=None, day=None):
        assert yr is not None, "In update_ymd, the year must not be None."
        assert mon is not None, "In update_ymd, the month must not be None."
        assert day is not None, "In update_ymd, the day must not be None."
        self.conf["year"] = int(yr)
        self.conf["month"] = int(mon)
        self.conf["day"] = int(day)
    def extract_date(self) -> date:
        '''Simple method to return a string from current date in object

        Returns:
            A datetime.date
        '''
        year, month, day = self.get_ymd()
        return date(year,month,day)
    #
    def extract_date_time_zero_hr(self) -> str:
        '''Simple routine to return a string for the current date in object

        Returns:
            String in the defined format for python3
        '''
        return self.extract_date().ctime()
    #
    def extract_date_time_str(self) -> str:
        '''Simple routine to return a string from the current date in object

        Returns:
            String in the format YYYY-MM-DD
        '''
        return self.extract_date().isoformat()
    #
    def get_timestamp(self) -> float:
        """Simple method to return the UTC timestamp for the current date in object
        
        Returns:
            float -- UTC timestamp
        """
        d = self.extract_date()
        return dz.datetime(d.year,d.month,d.day).timestamp()
    #
    def to_local_time(self,in_linux_timestamp=None) -> (str, str):
        '''Return the local time information with date, hour and minute

        Input:  
            in_linux_timestamp is the linux time since the epoch in UTC

        Output:
            day - A string in the form YYYY-m-d
            t - A string in the form HH:MM
        '''
        to_zone = self["timezone"]
        local_time = dz.datetime.fromtimestamp(in_linux_timestamp,to_zone).strftime("%Y/%m/%d %H:%M")
        local_time = local_time.split()
        day = local_time[0]
        t = local_time[1]
        return (day, t)
    #
    def increment_config_by_one_day(self):
        """Increment the configuration date by one day

        """
        w_time = self.extract_date()
        next_day = w_time + timedelta(days=1)
        self.update_ymd(next_day.year,next_day.month,next_day.day)