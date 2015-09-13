#! /usr/bin/env python
"""
Runs through a few example calculations to find the time of the Sun rise/set
Compares that to Arturus rise/set times
"""

from __future__ import division # have to do this so integers divide correctly
import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
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

def calc_12_days_of_year():
    """
    Use the year_date_window function to find the details for a star and the sun
    """
    dt_vec = year_date_window()
    star_out = star_detail(dt_vec)
    sun_out = sun_detail(dt_vec)

    # grab the hours from the date vectors
    time_ify = np.vectorize(lambda x: date2dayfrac(x)*24)
    star_dayfrac = time_ify(star_out)
    sun_dayfrac = time_ify(sun_out)
    return dt_vec, star_dayfrac, sun_dayfrac

def calc_one_year():
    """
    Use the all_days_of_year function to find the details for a star and the sun
    """
    dt_vec = all_days_of_year()
    star_out = star_detail(dt_vec)
    sun_out = sun_detail(dt_vec)

    # grab the day frac in hours from the rise time
    time_ify = np.vectorize(lambda x: date2dayfrac(x)*24)
    star_dayfrac = time_ify(star_out)
    sun_dayfrac = time_ify(sun_out)
    return dt_vec, star_dayfrac, sun_dayfrac

def plot_star_sun(dt_vec, star, sun):
    """
    take date, sun and star data and plot the information
    """
    # plot the data
    plt.interactive(1)
    plt.plot(dt_vec, star[:,1])
    plt.plot(dt_vec, star[:,2])
    plt.plot(dt_vec, sun[:,1])
    plt.plot(dt_vec, sun[:,2])
    plt.legend(['Star Rise', 'Star Set', 'Sunrise', 'Sunset'])
    plt.gca().invert_yaxis()

def write_to_CSV(dt_vec, star, sun):
    """
    Write data to a CSV
    """
    filename = 'testing.csv'

    # create pandas dataframe
    cols = ['date', 'Star Rise', 'Star Set', 'Sunrise', 'Sunset']
    output_data = pd.DataFrame(columns=cols)
    output_data['date'] = dt_vec
    output_data['Star Rise'] = star[:,1]
    output_data['Star Set'] = star[:,2]
    output_data['Sunrise'] = sun[:,1]
    output_data['Sunset'] = sun[:,2]

    # write the file out to CSV
    output_data.to_csv(filename, index=False)

def identify_month():
    """
    this code will be useful somewhere else... it uses vectorization to find where dt_vec equal a specific month
    """
    # how to find just the dates in october from this list
    oct_month = np.vectorize(lambda x: x.month == 10)
    tf = oct_month(dt_vec)
    idx = np.where(tf)
    dt_oct = map(lambda i: dt_vec[i], idx[0])
    time_of_starrise_oct = map(lambda i: time_of_starrise[i], idx[0])
    time_of_starset_oct = map(lambda i: time_of_starset[i], idx[0])
    time_of_sunrise_oct = map(lambda i: time_of_sunrise[i], idx[0])
    time_of_sunset_oct = map(lambda i: time_of_sunset[i], idx[0])

def main():
    dt_vec, star, sun = calc_one_year()
    plot_star_sun(dt_vec, star, sun)

if __name__ == '__main__':
    main()