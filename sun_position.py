#! /usr/bin/env python

"""
This calculates the position of the Sun

The calculations are taken from Chapter 25 of Astronomy Algorithms
"""
from __future__ import division # have to do this so integers divide correctly
import datetime
import numpy as np
from astro_date_unit_fcns import *

# some defaults
default_dt = datetime.datetime(1992, 10, 13, 0, 0)

def sun_position_calc(dt_input=default_dt):
    """
    Takes the calcs from Chapter 25 of Astronomy Algorithms and finds the position of the Sun

    Returns the apparent Right_Ascension and Declination of the Sun in degrees
    """
    # find the Julian Day
    JD = julian_day(dt_input)
    # the number of julian centuries since J2000.0
    T = (JD - 2451545.0) / 36525
    # the geometric mean longitude of the sun (in degrees)
    L_0 = 280.46646 + 36000.76983*T + 0.0003032*(T**2)
    L_0 = L_0 % 360
    # the mean anomaly of the sun
    M = 357.52911 + 35999.05029*T - 0.0001537*(T**2) % 360
    M = M % 360
    # eccentricity of the Earth's orbit
    e = 0.016708634 - 0.000042037*T - 0.0000001267*(T**2)
    # The sun's equation of center
    C = (1.914602 - 0.004817*T - 0.000014*(T**2))*np.sin(np.radians(M)) \
        + (0.019993 - 0.000101*T)*np.sin(np.radians(2*M)) \
        + 0.000289 * np.sin(np.radians(3*M))
    # the sun's true longitude
    lng = L_0 + C
    # the sun's true anomaly
    v = M + C
    # the sun's radius vector, expressed in astronomical units
    R = (1.000001018*(1 - e**2)) / (1 + e*np.cos(np.radians(v)))
    # apparent longitude of the sun
    omega = 125.04 - 1934.136*T
    lam = lng - 0.00569 - 0.00478*np.sin(np.radians(omega))
    # obliquity of the ecliptic
    epsilon_0 = dms2decdeg(23,26,21.448) - (46.8150/3600)*T - (0.00059/3600)*(T**2) + (0.001813/3600)*(T**3)
    epsilon = epsilon_0 + 0.00256*np.cos(np.radians(omega))
    # right ascension and declination of the sun
    rt_asc = np.arctan2(np.cos(np.radians(epsilon))*np.sin(np.radians(lam)), np.cos(np.radians(lam)))
    dec = np.arcsin(np.sin(np.radians(epsilon)) * np.sin(np.radians(lam)))
    return np.degrees(rt_asc) % 360, np.degrees(dec)


def main():
    pass

if __name__ == '__main__':
    main()