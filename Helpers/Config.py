#!/usr/bin/env python3
import json
import os, sys
from pprint import pprint, pformat
from copy import deepcopy
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
        self.conf = {}
        #Set some defaults
        self.conf["max_number_requests"] = 2
        self.conf["weather_file"] = "weather.txt"
        self.conf["verbose"] = False
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
        self.conf["weather_file"] = self.__check_value__(cfg,"weather_file","The weather file name must be provided.")
        full_data_directory = os.path.join(work_dir,self.conf["data_directory"])
        abs_data_directory = os.path.abspath(full_data_directory)
        assert os.path.exists(abs_data_directory), "The data path must exist: {}.  This does not create it programmatically.".format(abs_data_directory)
        self.conf["data_directory"] = abs_data_directory
        self.conf["weather_file"] = os.path.join(abs_data_directory,self.conf["weather_file"])
    #
    def __check_value__(self,cfg=None,dict_key=None,msg=None):
        assert cfg is not None
        assert dict_key is not None
        assert msg is not None
        try:
            return cfg[dict_key]
        except KeyError:
            if dict_key in self.conf:
                return self.conf[dict_key]
            else:
                self.__stop_input_processing(msg)
    #
    def __stop_input_processing(self, msg=None):
        assert msg is not None
        pprint(msg)
        sys.exit(1)
    #
    def state(self):
        cfg = deepcopy(self.conf)
        return cfg
    #
    def __repr__(self):
        return pformat(self.state())