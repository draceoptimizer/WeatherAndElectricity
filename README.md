# WeatherAndElectricity
Repository for obtaining, collecting and saving weather and electricity usage data

This repository is designed to hold the code for building electricity usage models based upon the combination of weather data and electricity usage history.  This is designed to provide both weather and electricity data on 15 minute intervals so that models of usage can be created to approximate cost for different costing models, specifically flat rate models vs demand cost models.  This is particularily useful in Texas since there is a market for the electric rates and there is a website to obtain historical electric usage information.

As always this code comes with no warranties for correctness or appropriateness.

## Modes of Operation

There are four separate tasks that are performed by this application,

* Update outstanding data
* Preprocess the outstanding data to clean data
* Use NN to create a good model for estimating data usage by hour
* Create temperature models based upon existing weather data

The first, second and fourth of these tasks are available from the _weather\_model\_driver_ and can either be called from a command line or set up to be executed on a regular basis.

The third task, is performed using a _Colaboratory_ notebook so that we can take advantage of GPU processing.

### Update Outstanding data

There are two independent set of data that need to be updated on a regular basis, the weather data and the power usage data.  These have to be updated regularily so that the model for estimating data usage over time can be as accurate as possible.

#### Original Data Information

##### Dark Sky

This code uses the Dark Sky API from ![Dark Sky](https://darksky.net/dev/img/attribution/poweredby.png).  Any user is required to obtain their own API Key.  This service is a pay-as-you-go service; therefore, a user of this code is responsible for their own costs.

##### Smart Meter Texas

This codes assumes the electrical usage information comes from [**_Smart Meters Texas_**](https://www.smartmetertexas.com).  The user must have their own account and at this point the usage information must be downloaded from the website manually using a _csv_ file.

## Code Usage

See the driver help function for usage information

