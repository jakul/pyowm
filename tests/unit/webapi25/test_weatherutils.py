#!/usr/bin/env python

"""
Test case for weatherutils.py module
"""

import unittest
from pyowm.webapi25.weather import Weather
from pyowm.webapi25 import weatherutils
from pyowm.webapi25.weathercoderegistry import WeatherCodeRegistry
from pyowm.exceptions.not_found_error import NotFoundError



class TestWeatherUtils(unittest.TestCase):

    __test_time_low = 1379090800
    __test_time_low_iso = "2013-09-13 16:46:40+00"
    __test_time_high = 1379361400
    __test_time_high_iso = "2013-09-16 19:56:40+00"

    __test_registry = WeatherCodeRegistry({
        "rain": [{
            "start": 1,
            "end": 100
        },
        {
            "start": 200,
            "end": 600
        }],
        "sun": [{
            "start": 750,
            "end": 850
        }]
    })

    __test_weather_rain = Weather(__test_time_low, 1378496400, 1378449600, 67,
            {"all": 30}, {"all": 0}, {"deg": 252.002, "speed": 4.100}, 57,
            {"press": 1030.119, "sea_level": 1038.589},
            {"temp": 294.199, "temp_kf": -1.899, "temp_max": 296.098,
                "temp_min": 294.199
            },
            "Rain", "Light rain", 500, "10d")
    __test_weather_sun = Weather(__test_time_high, 1378496480, 1378449510, 5,
            {"all": 0}, {"all": 0}, {"deg": 103.4, "speed": 1.2}, 12,
            {"press": 1090.119, "sea_level": 1078.589},
            {"temp": 299.199, "temp_kf": -1.899, "temp_max": 301.0,
             "temp_min": 297.6
             },
            "Clear", "Sky is clear", 800, "01d")
    __test_weathers = [__test_weather_rain, __test_weather_sun]

    def test_status_is(self):
        self.assertTrue(weatherutils.status_is(self.__test_weather_rain,
                                               "rain", self.__test_registry))
        self.assertFalse(weatherutils.status_is(self.__test_weather_sun,
                                               "rain", self.__test_registry))

    def test_any_status_is(self):
        self.assertTrue(weatherutils.any_status_is(self.__test_weathers,
                                                   "sun", self.__test_registry))
        self.assertFalse(weatherutils.any_status_is(self.__test_weathers,
                                                   "storm",
                                                   self.__test_registry))

    def test_filter_by_status(self):
        result_1 = weatherutils.filter_by_status(self.__test_weathers,
                                                 "rain",
                                                 self.__test_registry)
        self.assertEquals(1, len(result_1))
        self.assertTrue(weatherutils.status_is(result_1[0], "rain",
                                               self.__test_registry))
        
        result_2 = weatherutils.filter_by_status(self.__test_weathers,
                                                 "sun",
                                                 self.__test_registry)
        self.assertEquals(1, len(result_2))
        self.assertTrue(weatherutils.status_is(result_2[0], "sun",
                                               self.__test_registry))

    def test_find_closest_weather(self):
        self.assertEqual(self.__test_weather_rain,
                         weatherutils.find_closest_weather(self.__test_weathers,
                                                   self.__test_time_low + 200))
        self.assertEqual(self.__test_weather_sun,
                         weatherutils.find_closest_weather(self.__test_weathers,
                                                   self.__test_time_high - 200))

    def test_find_closest_weather_with_empty_list(self):
        self.assertFalse(weatherutils.find_closest_weather([],
                                                   self.__test_time_low + 200))

    def test_find_closest_fails_when_unixtime_not_in_coverage(self):
        self.assertRaises(NotFoundError, weatherutils.find_closest_weather,
                          self.__test_weathers, self.__test_time_high + 200)

    def test_is_in_coverage(self):
        self.assertTrue(weatherutils.is_in_coverage(self.__test_time_low + 200,
                                                    self.__test_weathers))
        self.assertTrue(weatherutils.is_in_coverage(self.__test_time_high - 200,
                                                    self.__test_weathers))
        self.assertTrue(weatherutils.is_in_coverage(self.__test_time_low,
                                                    self.__test_weathers))
        self.assertTrue(weatherutils.is_in_coverage(self.__test_time_high,
                                                    self.__test_weathers))
        self.assertFalse(weatherutils.is_in_coverage(self.__test_time_low - 200,
                                                    self.__test_weathers))
        self.assertFalse(weatherutils.is_in_coverage(self.__test_time_high + 200,
                                                    self.__test_weathers))

    def test_is_in_coverage_with_empty_list(self):
        self.assertFalse(weatherutils.is_in_coverage(1234567, []))
