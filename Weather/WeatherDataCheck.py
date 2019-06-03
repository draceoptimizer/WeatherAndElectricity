#!/usr/bin/env python3
from Helpers.Config import Config
from copy import deepcopy
from pprint import pformat, pprint
import collections
import pandas as pd

class WeatherDataCheck(collections.MutableMapping):
    """The class for managing the working weather data structures for processing

    This application requires a good bit of input because I prefer not
    deriving information from the current location of a computer.

    """
    def __init__(self,cfg:Config):
        """Initialize the weather data management, the data can be rather large so this
        uses a dictionary for the data management
        
        Arguments:
            cfg {Config} -- The initial config object for processing
        """
        self.data = dict()
        self.data["cfg"] = deepcopy(cfg)  # notice the deep copy for this item
        self.data["weather_time_names"] = ['lat','long','time','day','hm','tz']
        self.data["weather_data_names"] = ['dewPoint','humidity','precipIntensity',
            'pressure','temperature','uvIndex','visibility',
            'windBearing','windGust','windSpeed']

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
    def get_all_weather_names(self):
        return self["weather_time_names"] + self["weather_data_names"]
    #  Initialize the pandas
    def set_weather_panda(self):
        """Sets up a pandas for processing weather

            If the weather file doesn't exist, it builds an empty panda with the correct column names
        """
        work_weather = None
        try:
            work_weather = pd.read_csv(self["cfg"]["weather_file"])
        except FileNotFoundError:
            if self["cfg"]["verbose"]:
                print("Building a default panda DataFrame")
            all_columns = self.get_all_weather_names()
            work_weather = pd.DataFrame(columns=all_columns)
        work_weather.sort_values(["time"])
        self["weather_panda"] = work_weather
        print("Set Weather Panda {}".format(self["weather_panda"].shape[0]))
    #
    def check_weather_dates(self):
        """Purpose:  check that each date has 24 hours of data
    
        """
        try:
            df_shape = self["weather_panda"].shape
            num_rows = df_shape[0]
            if num_rows == 0:
                if self["cfg"]["verbose"]:
                    print("Must have data to process.")
                raise KeyError
            else:
                day_counts = self["weather_panda"].groupby(["day"]).size().reset_index(name="counts")
                short_day_counts = day_counts[day_counts['counts'] < 24]
                pprint(short_day_counts)
        except KeyError as e:
            raise KeyError("The pandas needs to be read in to update the weather file {}".format(e))
    #
