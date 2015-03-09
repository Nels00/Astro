#! /usr/bin/env python

# Calculates the rise and set times of a star and the star's position given the right ascension & declination
import datetime
import numpy as np
from astro_date_unit_fcns import *

# some defaults
default_dt = datetime.datetime(1988, 3, 20, 0, 0)
sf_lat = 38.3047
sf_longitude = 122.2989
rt_asc_arctarus = 213.9167
dec_arctarus = 19.1822

def star_rise_set(dt_input=default_dt, rt_asc=rt_asc_arctarus, dec=dec_arctarus, lat=sf_lat, longitude=sf_longitude):
    """
    RISE, TRANSIT, SET = star_rise_set(DATETIME Object, RIGHT ASCENSION, DECLINATION, LATITUDE, LONGITUDE)
    For a specific star return the rise, transit and set times
    All inputes, except the datetime object, are assumed to be in degrees

    These calculations were taken from Chapter 15 of Astronomy Algorithms
    """
    # an input needed for the math below
    h0_star = -0.5667
    # calculate sidereal time in greenwich at 0 UT
    day_only = datetime.datetime.combine(dt_input.date(), datetime.time(0))
    sidereal_time = sidereal_time_greenwich(dt_input)
    # convert inputs into radians
    conv_rad = np.pi/180
    h0_star_rad = h0_star * conv_rad
    lat_rad = lat * conv_rad
    longitude_rad = longitude * conv_rad
    rt_asc_rad = rt_asc * conv_rad
    dec_rad = dec * conv_rad
    sidereal_time_rad = sidereal_time * conv_rad

    # do the math
    cos_h0 = (np.sin(h0_star_rad)-(np.sin(lat_rad)*np.sin(dec_rad))) / (np.cos(lat_rad)*np.cos(dec_rad))
    if cos_h0 < -1 or cos_h0 > 1:
        print 'Error: this could be a circumpolar star'
    h0 = np.arccos(cos_h0)/conv_rad

    # transit, rise & set in degrees - make sure they a between 0 & 360
    transit_deg = (rt_asc + longitude - sidereal_time) / 360 % 1 * 360
    rise_deg = (transit_deg - h0) / 360 % 1 * 360
    set_deg = (transit_deg + h0) / 360 % 1 * 360
    if transit_deg > 360 or rise_deg > 360 or set_deg > 360:
        print 'Error: something is happening outside of this day'

    # this time is the sidereal time at Greenwich
    transit_time = decdeg2time(transit_deg)
    rise_time = decdeg2time(rise_deg)
    set_time = decdeg2time(set_deg)

    return transit_deg, rise_deg, set_deg

def display_arctarus_example():
    # display some example results

    # first pull in the default results, these are in degrees in Greenwich timezone
    transit, rise, setting = star_rise_set()
    # convert them to local time
    transit_local = decdeg2time(sidereal_time_local(transit))
    rise_local = decdeg2time(sidereal_time_local(rise))
    set_local = decdeg2time(sidereal_time_local(setting))

    # print out some results
    # why doesn't the local transit time equal the right ascension??
    print 'Here are the results in Local Sidereal Time, these are wrong :('
    print 'Transit time: ' + transit_local.isoformat()
    print 'Rise time: ' + rise_local.isoformat()
    print 'Set time: ' + set_local.isoformat()


def main():
    pass

if __name__ == '__main__':
    main()