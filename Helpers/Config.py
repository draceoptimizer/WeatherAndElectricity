#!/usr/bin/env python3
import json
import os, sys
from pprint import pprint, pformat
"""
Purpose:  General configuration management class so the information can 
be passed around safely
"""
class Config(object):
    """The class for managing the driving structure information

    This application requires a good bit of input because I prefer not
    deriving information from the current location of a computer.

    """

    def __init__(self,work_dir=None,config_file=None):
        assert work_dir is not None, "The working directory must be provided."
        assert config_file is not None, "The name of the config file must be provided."
        assert os.path.exists(work_dir), "The directory for the config file must exist: {}".format(work_dir)
        cfg_file = os.path.join(work_dir, config_file)
        assert os.path.exists(cfg_file), "The config file must exist: {}".format(cfg_file)
        with open(cfg_file) as json_data_file:
            cfg = json.load(json_data_file)
        #check for required fields
        self.website = self.__check_value__(cfg,"website","The website for Dark Sky must be provided.")
        self.key = self.__check_value__(cfg,"key","The user key must be provided.")
        self.latitude = self.__check_value__(cfg,"latitude","The latitude must be provided.")
        self.longitude = self.__check_value__(cfg,"longitude","The longitude must be provided.")
        self.start_month = self.__check_value__(cfg,"start_month","The start month must be provided.")
        self.start_day = self.__check_value__(cfg,"start_day","The start day must be provided.")
        self.start_year = self.__check_value__(cfg,"start_year","The start year must be provided.")
        self.max_number_requests = self.__check_value__(cfg,"max_number_requests","The maximum number of requests from Dark Sky must be provided.")
        self.data_directory = self.__check_value__(cfg,"data_directory","The data directory must be provided.")
        self.weather_file = self.__check_value__(cfg,"weather_file","The weather file name must be provided.")
        full_data_directory = os.path.join(work_dir,self.data_directory)
        abs_data_directory = os.path.abspath(full_data_directory)
        assert os.path.exists(abs_data_directory), "The data path must exist: {}.  This does not create it programmatically.".format(abs_data_directory)
        self.data_directory = abs_data_directory
        self.verbose = False

    def __check_value__(self,cfg=None,dict_key=None,msg=None):
        assert cfg is not None
        assert dict_key is not None
        assert msg is not None
        try:
            return cfg[dict_key]
        except KeyError as e:
            self.__stop_input_processing(msg)

    def __stop_input_processing(self, msg=None):
        assert msg is not None
        pprint(msg)
        sys.exit(1)

    def state(self):
        cfg = {}
        cfg["website"] = self.website
        cfg["key"] = self.key
        cfg["latitude"] = self.latitude
        cfg["longitude"] = self.longitude
        cfg["start_month"] = self.start_month
        cfg["start_day"] = self.start_day
        cfg["start_year"] = self.start_year
        cfg["max_number_requests"] = self.max_number_requests
        cfg["data_directory"] = self.data_directory
        cfg["weather_file"] = self.weather_file
        cfg["verbose"] = self.verbose
        return cfg

    def __repr__(self):
        return pformat(self.state())