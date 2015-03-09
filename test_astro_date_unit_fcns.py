#! /usr/bin/env python

from astro_date_unit_fcns import *
import unittest
import datetime

class TestAstroDateUnitFcns(unittest.TestCase):
    def test_julian_day_default(self):
        self.assertEquals(2436116.30625, julian_day())

    def test_calendar_day_default(self):
        dt_answer = datetime.datetime(1957, 10, 4, 19, 21)
        self.assertEquals(dt_answer, calendar_date())

if __name__ == '__main__':
    unittest.main()