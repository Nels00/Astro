#! /usr/bin/env python

from astro_date_unit_fcns import *
from star_calc_rise_set import *
import unittest
import datetime

class TestAstroDateUnitFcns(unittest.TestCase):
    def test_julian_day_default(self):
        self.assertEquals(2436116.30625, julian_day())

    def test_calendar_day_default(self):
        dt_answer = datetime.datetime(1957, 10, 4, 19, 21)
        self.assertEquals(dt_answer, calendar_date())

    def test_star_rise_set(self):
        # test the default transit, rise and set times
        default_dt = datetime.datetime(1988, 3, 20, 0, 0)
        sf_lat = 38.3047
        sf_longitude = 122.2989
        rt_asc_arctarus = 213.9167
        dec_arctarus = 19.1822
        transit, rise, setting = star_rise_set(default_dt, rt_asc_arctarus, dec_arctarus, sf_lat, sf_longitude)
        # transit compare
        dt_transit = decdeg2time(transit)
        dt_compare = datetime.datetime(1900,1,1,10,33,54)
        self.assertEquals(dt_transit, dt_compare)
        # rise compare
        dt_rise = decdeg2time(rise)
        dt_compare = datetime.datetime(1900,1,1,3,26,55)
        self.assertEquals(dt_rise, dt_compare)
        # set compare
        dt_set = decdeg2time(setting)
        dt_compare = datetime.datetime(1900,1,1,17,40,53)
        self.assertEquals(dt_set, dt_compare)



if __name__ == '__main__':
    unittest.main()