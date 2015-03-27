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
def year_date_window():
    """
    Returns a 12 datetime objects in a vector
    Each datetime object is separated by one month
    """
    dt_input = datetime.datetime.utcnow()
    month_vec = np.arange(dt_input.month-6, dt_input.month+6) % 12 +1
    dt_vec = []
    for x in month_vec:
        dt_vec.append(dt_input.replace(month=x))
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

    # for right now i'm just leaving this code in here to show how to pull out the hours
    
    out_hour = hour_ify(out)

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

def main():
    showoff()

if __name__ == '__main__':
    main()