#!/usr/bin/env python3
import pytest
from Preprocess.dark_sky_management import *

def test_non_dictionary():
    with pytest.raises(TypeError and SystemExit):
        url = build_forecast_request(1)

def test_correct_dictionary():
    data = {"website": "https://api.darksky.net/forecast",
        "key": "asdfjkl",
        "latitude": "32.7829",
        "longitude": "-96.7920",
        "start_month": 5,
        "start_day" : 1,
        "start_year" : 2017,
        "max_number_requests" : 5
    }
    url = build_forecast_request(data)
    expected_result = "https://api.darksky.net/forecast/asdfjkl/32.7829,-96.7920?exclude=\"minutely,hourly,daily,alerts,flags\""
    assert url == expected_result

def test_get_timezone():
    data = {"website": "https://api.darksky.net/forecast",
        "key": "e0c47993d5f64a030a76b8208ae2ab56",
        "latitude": "32.7829",
        "longitude": "-96.7920",
        "start_month": 5,
        "start_day" : 1,
        "start_year" : 2017,
        "max_number_requests" : 5
    }
    current_tz = get_location_timezone(data)
    expected_result = "America/Chicago"
    assert current_tz == expected_result

def test_get_current_weather():
    data = {"website": "https://api.darksky.net/forecast",
        "key": "e0c47993d5f64a030a76b8208ae2ab56",
        "latitude": "32.7829",
        "longitude": "-96.7920",
        "start_month": 5,
        "start_day" : 1,
        "start_year" : 2017,
        "max_number_requests" : 5
    }
    weather = get_current_weather(data)
    assert isinstance(weather,dict)
    assert weather is not None

def test_get_historical_weather(printout=False):
    data = {"website": "https://api.darksky.net/forecast",
        "key": "e0c47993d5f64a030a76b8208ae2ab56",
        "latitude": "32.7829",
        "longitude": "-96.7920",
        "month": 5,
        "day" : 1,
        "year" : 2017,
        "max_number_requests" : 5
    }
    weather = get_historical_weather(data)
    if(printout):
        pprint(weather)
    assert isinstance(weather,dict)
    assert weather is not None

if __name__ == "__main__":
    test_non_dictionary()

    test_correct_dictionary()

    test_get_timezone()

    test_get_historical_weather(printout=True)
