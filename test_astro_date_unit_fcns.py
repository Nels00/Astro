#! /usr/bin/env python

from astro_date_unit_fcns import *
from star_calc_rise_set import *
import unittest
import datetime

class TestAstroDateUnitFcns(unittest.TestCase):
    def test_julian_day_default(self):
        dt_example = datetime.datetime(1985, 10, 7, 19, 21)
        self.assertEquals(2446346.30625, julian_day(dt_example))

    def test_calendar_day_default(self):
        dt_example = datetime.datetime(1985, 10, 7, 19, 21)
        JD_example = 2446346.30625
        self.assertEquals(dt_example, calendar_date(JD_example))

    def test_star_rise_set(self):
        # test the default transit, rise and set times
        default_dt = datetime.datetime(1988, 3, 20, 0, 0)
        sf_lat = 38.3047
        sf_longitude = 122.2989
        rt_asc_arctarus = 213.9167
        dec_arctarus = 19.1822
        transit, rise, setting = star_rise_set(default_dt, rt_asc_arctarus, dec_arctarus, sf_lat, sf_longitude)
        # transit compare
        dt_compare = datetime.datetime(1988,3,20,10,33,54)
        self.assertEquals(transit, dt_compare)
        # rise compare
        dt_compare = datetime.datetime(1988,3,20,3,26,55)
        self.assertEquals(rise, dt_compare)
        # set compare
        dt_compare = datetime.datetime(1988,3,20,17,40,53)
        self.assertEquals(setting, dt_compare)



if __name__ == '__main__':
    unittest.main()