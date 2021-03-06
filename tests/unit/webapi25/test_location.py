#!/usr/bin/env python

"""
Test case for location.py module
"""

import unittest
from pyowm.webapi25.location import Location, location_from_dictionary


class TestLocation(unittest.TestCase):

    __test_name = 'London'
    __test_lon = 12.3
    __test_lat = 43.7
    __test_ID = 1234
    __test_country = 'UK'
    __test_instance = Location(__test_name, __test_lon, __test_lat, __test_ID,
                               __test_country)

    def test_init_fails_when_coordinates_are_out_of_bounds(self):
        """
        Test failure when providing: lon < -180, lon > 180, lat < -90, lat > 90
        """
        self.assertRaises(ValueError, Location, 'London', -200.0, 43.7, 1234)
        self.assertRaises(ValueError, Location, 'London', 200.0, 43.7, 1234)
        self.assertRaises(ValueError, Location, 'London', 12.3, -100.0, 1234)
        self.assertRaises(ValueError, Location, 'London', 12.3, 100.0, 1234)

    def test_from_dictionary(self):
        dict1 = {"coord": {"lon": -0.12574, "lat": 51.50853}, "id": 2643743,
                 "name": "London", "cnt": 9}
        dict2 = {"city": {"coord": {"lat": 51.50853, "lon": -0.125739},
                 "country": "GB", "id": 2643743, "name": "London",
                 "population": 1000000}
                }
        result1 = location_from_dictionary(dict1)
        result2 = location_from_dictionary(dict2)
        self.assertTrue(isinstance(result1, Location))
        self.assertTrue(isinstance(result2, Location))
        self.assertFalse(result1.get_country() is not None)
        self.assertTrue(result1.get_ID() is not None)
        self.assertTrue(result1.get_lat() is not None)
        self.assertTrue(result1.get_lon() is not None)
        self.assertTrue(result1.get_name() is not None)
        self.assertTrue(result2.get_country() is not None)
        self.assertTrue(result2.get_ID() is not None)
        self.assertTrue(result2.get_lat() is not None)
        self.assertTrue(result2.get_lon() is not None)
        self.assertTrue(result2.get_name() is not None)

    def test_getters_return_expected_data(self):
        instance = Location(self.__test_name, self.__test_lon, self.__test_lat,
                            self.__test_ID, self.__test_country)
        self.assertEqual(instance.get_name(), self.__test_name)
        self.assertEqual(instance.get_lon(), self.__test_lon)
        self.assertEqual(instance.get_lat(), self.__test_lat)
        self.assertEqual(instance.get_ID(), self.__test_ID)
        self.assertEqual(instance.get_country(), self.__test_country)
