#! /usr/bin/env python

# Several functions that allow for the calculation of Julian Day and Sidereal Time
# Assumes that longitude West is positive
import datetime
import pytz

# some defaults
default_dt = datetime.datetime(1957, 10, 4, 19, 21)
default_JD = 2436116.30625
sf_lat = 38.3047
sf_longitude = 122.2989

def julian_day(dt_input=default_dt):
    # Calculations taking from Chapter 7 of Astronomy Algorithms

    # Breakout the datetime object
    Y, M, D = datebreakout(dt_input)
    # add the time part of the date to the day integer
    D = add_day_frac(dt_input)
    
    # assume that the transition to the gegorian calendar happend in Oct 1582
    if Y < 1582:
        gegorian = False
    elif Y > 1582:
        gegorian = True
    elif M < 10:
        gegorian = False
    elif M > 10:
        gegorian = True
    elif int(D) <= 4:
        gegorian = False
    elif int(D) >= 15:
        gegorian = True
    else:
        print "Error: Technically this date should not exist"
        gegorian = True
    # revise M & Y if we're in Jan or Feb
    if M == 1 or M == 2:
        Y = Y - 1
        M = M + 12
    # Calc A & B depending on the calendar
    if gegorian == True:
        A = int(Y/100)
        B = 2 - A + int(A/4)
    else:
        B = 0
    # calc the julian day from the inputs above
    JD = int(365.25*(Y+4716)) + int(30.6001*(M+1)) + D + B - 1524.5
    return JD

def calendar_date(JD=default_JD):
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
    day_dt = datetime.datetime(year, month, int(day))
    time_dt = dayfrac2time(day)

    return datetime.datetime.combine(day_dt.date(), time_dt.time())

def sidereal_time_greenwich(dt_input=default_dt):
    # Cacls from Chapter 12 Astronomy Alogrithms

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
    # Take sidereal time at Greenwich and convert into Local Sidereal Time (LST)
    lst = sid_gt - longitude
    lst = lst % 360
    return lst

def datebreakout(dt_input):
    Y = dt_input.year
    M = dt_input.month
    D = dt_input.day
    return Y, M, D

def decdeg2time(decdeg):
    # Convert decimal degrees into time
    conv_hrs = decdeg / 15
    hrs = int(conv_hrs)
    conv_mnt = (conv_hrs - hrs) * 60
    mnt = int(conv_mnt)
    sec = (conv_mnt - mnt) * 60
    sec = round(sec)
    # should change this using date + timedelta(days=1)
    # for now it's a hack
    if sec > 59:
        sec = 59
    # they come out as floats so i need to convert them to type integer
    # for now i have to round seconds until i figure out a better way
    t = datetime.datetime(1900,1,1, hrs, mnt, int(sec))
    return t

def decdeg2dms(decdeg):
    # Convert decimal degrees into degrees minutes seconds
    mnt,sec = divmod(decdeg*3600,60)
    deg,mnt = divmod(mnt,60)
    return deg, mnt, sec

def dayfrac2time(day_frac):
    # Convert a fractional day into a time
    frac = day_frac - int(day_frac)
    mnt,sec = divmod(frac*24*3600, 60)
    hrs,mnt = divmod(mnt,60)
    sec = round(sec)
    # should change this using date + timedelta(days=1)
    # for now it's a hack
    if sec > 59:
        sec = 59
    # they come out as floats so i need to convert them to type integer
    t = datetime.datetime(1900,1,1, int(hrs), int(mnt), int(sec))
    return t


def add_day_frac(dt_input):
    # Take an int, assumed to be a day, and add a time to it as a day frac
    # (has to be a better way to do this)
    Y, M, D = datebreakout(dt_input)
    day_only = datetime.datetime(Y, M, D)
    tdelta = dt_input - day_only
    day_frac = tdelta.total_seconds() / (24 * 3600)
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