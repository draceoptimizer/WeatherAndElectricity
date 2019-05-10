#!/usr/bin/env python3
from Helpers.Config import Config
from copy import deepcopy
from pprint import pformat,pprint
import collections
import pandas as pd
#
class UsageManagement(collections.MutableMapping):
    """
    Purpose:  This class manages the usage calculations from existing 
    smart meter data.
    """
    def __init__(self,cfg:Config):
        self.data = dict()
        self.data["cfg"] = deepcopy(cfg)  # notice the deep copy for this item
        self.data["usage_in_names"] = ['ESIID','USAGE_DATE','USAGE_START_TIME',
        'USAGE_END_TIME','USAGE_KWH']
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
    def get_all_names(self):
        return self["usage_in_names"]
        #  Initialize the pandas
    def set_usage_in_panda(self):
        """Sets up a pandas for processing usage

            If a usage file doesn't exist, it builds an empty panda with the correct column names
        """
        work_usage = None
        try:
            work_usage = pd.read_csv(self["cfg"]["usage_in_file"])
        except FileNotFoundError:
            if self["cfg"]["verbose"]:
                print("No usage in file found")
            work_usage = None
        if work_usage is not None:
            work_usage.sort_values(["USAGE_DATE",'USAGE_START_TIME'])
            self["usage_panda"] = work_usage[self.data["usage_in_names"]]
            print("Set Usage Panda {}".format(self["usage_panda"].shape[0]))
            if self["cfg"]["verbose"]:
                print("Using in shape: {}x{}".format(self["usage_panda"].shape[0],self["usage_panda"].shape[1]))
                pprint(self["usage_panda"].head())
                pprint(self["usage_panda"].tail())
        else:
            print("No Usage Panda set!")