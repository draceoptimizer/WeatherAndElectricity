# WeatherAndElectricity
Repository for obtaining, collecting and saving weather and electricity usage data

This repository is designed to hold the code for building electricity usage models based upon the combination of weather data and electricity usage history.  This is designed to provide both weather and electricity data on 15 minute intervals so that models of usage can be created to approximate cost for different costing models, specifically flat rate models vs demand cost models.  This is particularily useful in Texas since there is a market for the electric rates and there is a website to obtain historical electric usage information.

As always this code comes with no warranties for correctness or appropriateness.

##  Original Data Information

**_Dark Sky_**

This code uses the Dark Sky API from ![Dark Sky](https://darksky.net/dev/img/attribution/poweredby.png).  Any user is required to obtain their own API Key.  This service is a pay-as-you-go service; therefore, a user of this code is responsible for their own costs.

**_Smart Meter Texas_**

This codes assumes the electrical usage information comes from [**_Smart Meters Texas_**](https://www.smartmetertexas.com).  The user must have their own account and at this point the usage information must be downloaded from the website manually using a _csv_ file.

## Code Usage

_Data Preprocessing_  All of the code is assumed to be executed from the command line for gathering and preprocessing the data.  This isn't a large amount of data, so almost any system suffices.  _(NOTE:  This code was originally run on a raspberry pi 3 B+, so even small systems suffice for the preprocessing steps.)_

