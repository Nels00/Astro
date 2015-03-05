#! /usr/bin/env python

from astro_date_unit_fcns import *
import unittest

class TestAstroDateUnitFcns(unittest.TestCase):
    def test_julian_day_default(self):
        self.assertEquals(2436116.30625, julian_day())

    def test_calendar_day_default(self):
        actual_date = calendar_date()
        self.assertEquals(1957, actual_date.year)
        self.assertEquals(10, actual_date.month)
        self.assertEquals(4, actual_date.day)
        self.assertEquals(19, actual_date.hour)
        self.assertEquals(21, actual_date.minute)

if __name__ == '__main__':
    unittest.main()