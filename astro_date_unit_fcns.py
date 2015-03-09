#! /usr/bin/env python

# Several functions that allow for the calculation of Julian Day and Sidereal Time
# Assumes that longitude West is positive
import datetime

# some defaults
default_dt = datetime.datetime(1957, 10, 4, 19, 21)
default_JD = 2436116.30625
sf_lat = 38.3047
sf_longitude = 122.2989

def julian_day(dt_input=default_dt):
    # Takes a datetime object and returns the Julian Day
    # Calculations taken from Chapter 7 of Astronomy Algorithms

    # Breakout the datetime object
    Y, M, D = datebreakout(dt_input)
    # add the time part of the date to the day integer
    D = add_frac_day(dt_input)
    
    # assume that the transition to the gegorian calendar happend in Oct 1582
    # really it happened at different times depending on the country, e.g. in 1752 in the UK
    dt_julian = datetime.datetime(1582, 10, 4)
    dt_gegorian = datetime.datetime(1582, 10, 15)
    if dt_input <= dt_julian:
        gegorian = False
    elif dt_input >= dt_gegorian:
        gegorian = True
    else:
        print "Error: Technically this date, %s, should not exist" % dt_input.date().isoformat()
        gegorian = True
    # revise M & Y if we're in Jan or Feb
    if M == 1 or M == 2:
        Y = Y - 1
        M = M + 12
    # Calc A & B depending on the calendar
    if gegorian:
        A = int(Y/100)
        B = 2 - A + int(A/4)
    else:
        B = 0
    # calc the julian day from the inputs above
    JD = int(365.25*(Y+4716)) + int(30.6001*(M+1)) + D + B - 1524.5
    return JD

def calendar_date(JD=default_JD):
    # Takes a Julian Day and returns a datetime object
    # Calcs were taken from Chapter 7 of Astronomy Algorithms
    
    # these calcs do not work for negative julian days
    if JD < 0:
        print "Error: This will not work for negative Julian Day numbers"

    JD = JD + 0.5
    Z = int(JD)
    F = JD - int(JD)
    if Z < 2299161:
        A = Z
    else:
        alpha = int((Z - 1867216.25) / 36524.25)
        A = Z + 1 + alpha - int(alpha/4)
    B = A + 1524
    C = int((B - 122.1) / 365.25)
    D = int(365.25 * C)
    E = int((B - D) / 30.6001)

    # use the above to calculate the year, month and day
    day = B - D - int(30.6001 * E) + F
    if E < 14:
        month = E - 1
    else:
        month = E - 13
    if month > 2:
        year = C - 4716
    else:
        year = C - 4715
    # create the datetime object from the Year, Month integers and a fractional Day
    dt_day = datetime.datetime(year, month, int(day))
    dt_output = dayfrac2time(dt_day.date(), day)
    return dt_output

def sidereal_time_greenwich(dt_input=default_dt):
    """
    SIDEREAL_TIME (In Degrees) = sidereal_time_greenwich(DATETIME Object)
    Give a datetime object and the sidereal time in Greenwich is given (in degrees)
    """
    # Input a datetime object and the sidereal time is returned
    # Calcs from Chapter 12 Astronomy Alogrithms

    # Breakout the datetime object
    Y, M, D = datebreakout(dt_input)
    day_only = datetime.datetime(Y, M, D)
    
    # Find the Julian Day at 0h UT and the normal Julian Day
    JD_0 = julian_day(day_only)
    JD = julian_day(dt_input)
    # calc the mean sidereal time
    T = (JD_0 - 2451545.0) / 36525
    mean_sid_gt = 280.46061837 + 360.98564736629 * (JD - 2451545.0) + 0.000387933*(T**2) - ((T**3) / 38710000)
    mean_sid_gt = mean_sid_gt % 360
    return mean_sid_gt

def sidereal_time_local(sid_gt, lat=sf_lat, longitude=sf_longitude):
    # Takes a sidereal time at Greenwich, expressed in degrees, and returns the Local Sidereal Time (LST) for that Lat & Long
    # I think that subtracting the longitude is too simple but it's a close approximation, i think
    lst = sid_gt - longitude
    lst = lst % 360
    return lst

def datebreakout(dt_input):
    # Give a datetime object and return the Year, Month & Day
    Y = dt_input.year
    M = dt_input.month
    D = dt_input.day
    return Y, M, D

def decdeg2dms(decdeg):
    # Convert decimal degrees into degrees minutes seconds
    mnt,sec = divmod(decdeg*3600,60)
    deg,mnt = divmod(mnt,60)
    return deg, mnt, sec

def decdeg2time(decdeg):
    # Convert decimal degrees into time
    conv_hrs = decdeg / 15
    hrs = int(conv_hrs)
    conv_mnt = (conv_hrs - hrs) * 60
    mnt = int(conv_mnt)
    sec = (conv_mnt - mnt) * 60
    sec = round(sec)
    # they come out as floats so i need to convert them to type integer
    # for now i have to round seconds until i figure out a better way
    t = datetime.datetime(1900,1,1, hrs, mnt, int(sec))
    return t

def dayfrac2time(dt_input, day_frac):
    # Take a datetime.date and fractional day & the fractional day to the datetime object
    frac = day_frac - int(day_frac)
    mnt,sec = divmod(frac*24*3600, 60)
    hrs,mnt = divmod(mnt,60)
    sec = round(sec)
    # sometimes the seconds will round to 60, so we need to increment by a minute
    inc_mnt = False
    if sec == 60:
        sec = 0
        inc_mnt = True
    # they come out as floats so i need to convert them to type integer
    t = datetime.time(int(hrs), int(mnt), int(sec))
    dt_output = datetime.datetime.combine(dt_input, t)
    if inc_mnt:
        dt_output = dt_output + datetime.timedelta(minutes=1)
    return dt_output

def date2dayfrac(dt_input):
    # Take a datetime object and convert the time part to a fractional day
    day_only = datetime.datetime.combine(dt_input.date(), datetime.time(0))
    tdelta = dt_input - day_only
    day_frac = tdelta.total_seconds() / (24 * 3600)
    return day_frac

def time2decdeg(dt_input):
    # Take a datetime object and convert the time part to degrees
    day_frac = date2dayfrac(dt_input)
    return 360 * day_frac

def add_frac_day(dt_input):
    # Take an datetime object, and add the time to the Day as a fractional day
    Y, M, D = datebreakout(dt_input)
    day_frac = date2dayfrac(dt_input)
    return D + day_frac

def showoff():
    # Run some calcs on 7 Oct 1985 7:21PM and print them to the screen
    dt_ex = datetime.datetime(1987,10,7, 19, 21)
    JD = julian_day(dt_ex)
    sid_gt = sidereal_time_greenwich(dt_ex)
    sid_local = sidereal_time_local(sid_gt)
    print 'The Julian Day of 1985 October 7 at 19:21 UTC is: %s' % JD
    print 'You can verify at this URL: http://www.onlineconversion.com/julian_date.htm'
    print ''
    print 'Mean Sidereal Time in Greenwich at that time was: %s' % decdeg2time(sid_gt).time().isoformat()
    print 'Local Sidereal Time in SF at that time was: %s' % decdeg2time(sid_local).time().isoformat()
    print 'You can verify here: http://www.csgnetwork.com/siderealjuliantimecalc.html'
    print ''
    # show current local sidereal time
    utcnow = datetime.datetime.utcnow()
    current_sid_local = sidereal_time_local( sidereal_time_greenwich(utcnow))
    print 'Local Sidereal Time in SF right now is: %s' % decdeg2time(current_sid_local).time().isoformat()
    print 'Can verify here: http://tycho.usno.navy.mil/sidereal.html'


def main():
    showoff()

if __name__ == '__main__':
    main()