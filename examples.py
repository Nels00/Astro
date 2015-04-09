#! /usr/bin/env python
"""
Runs through a few example calculations to find the time of the Sun rise/set
Compares that to Arturus rise/set times
"""

from __future__ import division # have to do this so integers divide correctly
import datetime
import numpy as np
import matplotlib.pyplot as plt
from astro_date_unit_fcns import *
from star_calc_rise_set import *
from sun_position import *

# calculate a date vector 
def all_days_of_year():
    """
    Returns all the days of the year in a datetime object
    """
    # find first day of the year
    tdy = datetime.date.today()
    first_dt = datetime.date(tdy.year, 1, 1)
    dt_input = datetime.datetime.combine(first_dt, datetime.time(0))
    dt_vec = []
    for x in np.arange(365):
        dt_vec.append(dt_input + datetime.timedelta(days=x))

    return dt_vec


def year_date_window():
    """
    Returns a 12 datetime objects in a vector
    Each datetime object is separated by one month
    """
    # create a datetime object with today's date and zero hours
    dt_input = datetime.datetime.combine(datetime.date.today(), datetime.time(0))
    month_vec = np.arange(dt_input.month-6, dt_input.month+6) % 12 +1
    dt_vec = []
    for x in month_vec:
        # a hacky way to handle the months ending on different days:
        dt_iter = dt_input
        while True:
            try:
                dt_iter = dt_iter.replace(month=x)
                dt_vec.append(dt_iter)
                break
            except:
                dt_iter = dt_iter.replace(day=dt_iter.day-1)

    return dt_vec

def star_detail(dt_vec):
    """
    Takes a vector of datetime objects and returns the TRANSIT, RISE, & SET times of Arturus for each datetime
    """
    out = np.empty([len(dt_vec),3], dtype=datetime.datetime)
    for idx, dt_instance in enumerate(dt_vec):
        transit, rise, setting = star_rise_set(dt_instance)
        out[idx,0] = timezone_change(transit)
        out[idx,1] = timezone_change(rise)
        out[idx,2] = timezone_change(setting)
    return out

def sun_detail(dt_vec):
    """
    Takes a vector of datetime objects and returns the TRANSIT, RISE, & SET times of the Sun for each datetime
    """
    out = np.empty([len(dt_vec),3], dtype=datetime.datetime)
    for idx, dt_instance in enumerate(dt_vec):
        rt_asc, dec = sun_position_calc(dt_instance)
        transit, rise, setting = star_rise_set(dt_instance, rt_asc, dec, starq=0)
        out[idx,0] = timezone_change(transit)
        out[idx,1] = timezone_change(rise)
        out[idx,2] = timezone_change(setting)
    return out

def showoff():
    dt_vec = year_date_window()
    star_out = star_detail(dt_vec)
    sun_out = sun_detail(dt_vec)

    # grab the hours from the date vectors
    hour_ify = np.vectorize(lambda x: x.hour)
    star_hour = hour_ify(star_out)
    sun_hour = hour_ify(sun_out)
    return star_out, sun_out

def sun_over_one_year():
    dt_vec = all_days_of_year()
    out = sun_detail(dt_vec)
    time_ify = np.vectorize(lambda x: x.time())
    time_of_sunrise = time_ify(out[:,1])
    return time_of_sunrise

def main():
    pass

if __name__ == '__main__':
    main()