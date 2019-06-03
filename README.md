# Weather And Electricity

Repository for obtaining, collecting and saving weather and electricity usage data

This repository is designed to hold the code for building electricity usage models based upon the combination of weather data and electricity usage history.  This is designed to provide both weather and electricity data on 15 minute intervals so that models of usage can be created to approximate cost for different costing models, specifically flat rate models vs demand cost models.  This is particularily useful in Texas since there is a market for the electric rates and there is a website, ![Texas Smart Meter](https://texassmartmeter.com), to obtain historical electric usage information.

As always this code comes with no warranties for correctness or appropriateness.  Furthermore, since this particular code uses a Neural Net to compute usage, it can be considered custom for each house or establishment that uses the code.  _Sorry:-\(_

## Modes of Operation

These are the separate tasks that are performed by this application,

* Gather Weather Data
* Process Usage Data to a format compatible with Weather Data
* Create a randomized weather model
* Set up data for Deep Neural Net Modeling of Usage based upon Weather Data
* Optimize a Deep Neural Net Model for Usage based upon Weather Data

The last task, is performed using a _Colaboratory_ notebook so that we can take advantage of GPU processing.

All of the processing starts with two external sets of data:

*  Dark Sky Weather Data
*  Usage Data available from Smart Meter Texas

## External Data Basics

The basic information for the external data is summarized in the following paragraphs.

### Dark Sky Weather Data

This code uses the Dark Sky API from ![Dark Sky](https://darksky.net/dev/img/attribution/poweredby.png).  Any user is required to obtain their own API Key.  This service is a pay-as-you-go service; therefore, a user of this code is responsible for their own costs.  The Dark Sky API gives you 1000 free historical data accesses per day.

This particular code is set up so that it only downloads 30 days each hour; therefore, the we trade off free access to the data against the initial time to populate the historical data.

The data that is input has the following fields _(Some processing is done during retrieval.)_:

>   'lat'   -   The latitude of the location
>   'long'  -   The longitude of the location
>   'time'  -   The UTC for the data - not used much
>   'day'   -   The local day of the data in the form yyyy/mm/dd
>   'hm'    -   The hour and minute for the data in the form "hh:00".  This is always "00" minutes since it is for the entire hour.
>   'tz'    -   The local time zone.  _This is used to convert the time to day and hm
>   'dewPoint'   - _Self Defined_
>   'humidity'   - _Self Defined_
>   'precipIntensity'   - _Self Defined_
>   'pressure'   - _Self Defined_
>   'temperature'   - _Self Defined_
>   'uvIndex'   - _Self Defined_
>   'visibility'   - _Self Defined_
>   'windBearing'   - _Self Defined_
>   'windGust'   - _Self Defined_
>   'windSpeed'   - _Self Defined_

>_I really don't know which of these will be important, so I will keep them all._

I am planning to use the month and hour for the first NN Model; therefore, I will need to synch up the usage data with the exact format for day and hm for input into the NN Model.

###  Smart Meter Texas Data

Smart Meter Texas currently only allows the last two years of data, so we will start with two years of data and slow improve the NN Model as we add data.  The Smart Meter Texas data come in with usage in 15 minute intervals; however, we will sum the usage for the entire hour.  The output will be of the form

>   'day'   -   The local day of the data in the form yyyy/mm/dd.
>   'hm'    -   The hour and minute for the data in the form "hh:00".  _This is after the sum of the hours, and always has "00" minutes since it is for the entire hour.  This matches the weather data._
>   'usage  -   This is in KiloWattHours.  This is the basic charging unit in Texas.

### Conclusion

These two data sources should provide a reasonable set of input for modeling.

##  Individual Processes

The individual processing steps are documented in their respective mark down documents.  These are:

*   [Gather Weather Data](./GatherWeatherData.md)
