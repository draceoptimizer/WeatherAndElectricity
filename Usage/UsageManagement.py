#!/usr/bin/env python3
from Helpers.Config import Config
from copy import deepcopy
from pprint import pformat,pprint
import collections
import pandas as pd
import os
import shutil
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
        self.data["usage_out_names"] = ["day","hm","usage"]
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
    #  Perform Basic Conversions
    def basic_conversions(self):
        """This provides basic format changes for the usage data to match up with the 
        Dark Sky format so that joins are possible.

        (1)  Changes the - in the date to /
        (2)  Enhances the start time so that it identifies just the hour start (this is the way the Dark Sky Works)

        """
        work_pd = self["usage_panda"]
        #Change the date format
        work_pd["USAGE_DATE"] = work_pd["USAGE_DATE"].str.replace("-","/")
        if self["cfg"]["verbose"]:
            print("Changing the USAGE DATE format.")
            pprint(self["usage_panda"].head())
            pprint(self["usage_panda"].tail())
        #Enhance start time so it always has 00 min
        work_pd["hm"] = work_pd["USAGE_START_TIME"].map(lambda v: v.split(":")[0] + ":00")
        if self["cfg"]["verbose"]:
            print("Changing the USAGE DATE format.")
            pprint(self["usage_panda"].head())
            pprint(self["usage_panda"].tail())
    #  Usage Sum By Hour
    def sum_kwh(self):
        """This provides basic format changes for the usage data to match up with the 
        Dark Sky format so that joins are possible.

        (1)  Changes the - in the date to /
        (2)  Enhances the start time so that it identifies just the hour start (this is the way the Dark Sky Works)

        """
        work_pd = self["usage_panda"]
        #Change the date format

        temp_pd = pd.DataFrame()
        temp_pd["usage"] = work_pd.groupby(["USAGE_DATE","hm"])["USAGE_KWH"].sum()
        temp_pd.reset_index(level=0,inplace=True)
        temp_pd.reset_index(inplace=True)
        temp_pd["day"] = temp_pd["USAGE_DATE"]
        self["usage_processed"] = temp_pd[["day","hm","usage"]]
        if self["cfg"]["verbose"]:
            print("Changing the USAGE DATE format.")
            pprint(self["usage_processed"].head())
            pprint(self["usage_processed"].tail())
        unique_day_hr = self.__check_unique__(self["usage_processed"])
        assert unique_day_hr, "The hour and day values must be unique: {} during processing.  There is an error someplace.".format(unique_day_hr)
    #Check unique values in day and hm
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
    #  Save the usage data
    def save_usage(self):
        """This saves the updated usage information with the following steps:
        (1)  moves the input file to Processed
        (2)  reads in any existing usage file into a panda
        (3)  appends the data to the existing usage data
        (4)  writes the usage data back out

        """
        processed_dir = self["cfg"]["usage_in_processed_directory"]
        input_file = self["cfg"]["usage_in_file"]
        output_file = self["cfg"]["usage_out_file"]
        #Move the input file
        if self["cfg"]["verbose"]:
            print("Processed Directory: {}".format(processed_dir))
            print("Original Input File: {}".format(input_file))
        base_input_file = os.path.basename(input_file)
        processed_file = os.path.join(processed_dir,base_input_file)
        if self["cfg"]["verbose"]:
            print("Base Input File: {}".format(base_input_file))
            print("Processed File: {}".format(processed_file))
        shutil.move(input_file,processed_file)

        # Read in the existing file
        work_pd = None
        try:
            work_pd = pd.read_csv(output_file)
        except:
            work_pd = pd.DataFrame(columns=self["usage_out_names"])
        #Append the usage panda
        work_pd = work_pd.append(self["usage_processed"],ignore_index=True,sort=False)
        w_columns = work_pd.columns
        while not (w_columns[0] in self["usage_out_names"]):
            work_pd = work_pd.drop(w_columns[0],axis=1)
            w_columns = work_pd.columns
            if self["cfg"]["verbose"]:
                pprint(work_pd.shape)
        work_pd = work_pd.sort_values(["day","hm"])
        pprint(work_pd.head())
        pprint(work_pd.dtypes)
        unique_day_hr = self.__check_unique__(work_pd)
        assert unique_day_hr, "The hour and day values must be unique: {} before writing.  There is an error someplace.".format(unique_day_hr)
        #Write the file
        if self["cfg"]["verbose"]:
            print("The output file name is {}.".format(output_file))
        work_pd.to_csv(output_file,na_rep="0")
        #TODO:  I need to process the hr and day values if they are not unique, then log the differences