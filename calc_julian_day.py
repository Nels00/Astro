#! /usr/bin/env python

# Takes a date and converts it to the Julian Day
# Assumes that longitude West is positive
import datetime
import pytz

# some defaults
default_Y = 1957
default_M = 10
default_D = 4.81
default_JD = 2436116.31
default_t = datetime.datetime.strptime('00:00:00', '%H:%M:%S')
sf_lat = 38.3047
sf_longitude = 122.2989


def julian_day(Y=default_Y, M=default_M, D=default_D, t=default_t):
    # Calculations taking from Chapter 7 of Astronomy Algorithms

    # add the time part of the date to the day integer
    D = add_day_frac(D,t)
    
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
    return [year, month, day]

def sidereal_time_greenwich(Y=default_Y, M=default_M, D=default_D, t=default_t):
    # Cacls from Chapter 12 Astronomy Alogrithms

    # add the fractional day from the time object to D
    D = add_day_frac(D,t)
    # Find the Julian Day at 0h UT
    JD_0 = julian_day(Y, M, int(D))
    JD = julian_day(Y, M, D)
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


def decdeg2time(decdeg):
    # Convert decimal degrees into time
    conv_hrs = decdeg / 15
    hrs = int(conv_hrs)
    conv_mnt = (conv_hrs - hrs) * 60
    mnt = int(conv_mnt)
    sec = (conv_mnt - mnt) * 60
    # datetime is terrible, for now i have to round seconds until i figure out a better way
    t = datetime.datetime(1900,1,1, hrs, mnt, int(sec))
    return t

def decdeg2dms(decdeg):
    # Convert decimal degrees into degrees minutes seconds
    mnt,sec = divmod(decdeg*3600,60)
    deg,mnt = divmod(mnt,60)
    return deg,mnt,sec

def add_day_frac(D, t):
    # Take an int, assumed to be a day, and add a time to it as a day frac
    # (has to be a better way to do this)
    zero_time = datetime.datetime.strptime('00:00:00', '%H:%M:%S')
    tdelta = t - zero_time
    day_frac = tdelta.total_seconds() / (24 * 3600)
    return D + day_frac

def showoff():
    # Run some calcs on 7 Oct 1985 7:21PM and print them to the screen
    year = 1985
    month = 10
    day = 7
    t = datetime.datetime(1900,1,1, 19, 21)
    JD = julian_day(year, month, day, t)
    sid_gt = sidereal_time_greenwich(year, month, day, t)
    sid_local = sidereal_time_local(sid_gt)
    print 'The Julian Day of 1985 October 7 at 19:21 UTC is: %s' % JD
    print 'You can verify at this URL: http://www.onlineconversion.com/julian_date.htm'
    print ''
    print 'Mean Sidereal Time in Greenwich at that time was: %s' % decdeg2time(sid_gt).time().isoformat()
    print 'Local Sidereal Time in SF at that time was: %s' % decdeg2time(sid_local).time().isoformat()
    print 'You can verify here: http://www.csgnetwork.com/siderealjuliantimecalc.html'
    print ''
    # show current local sidereal time
    n = datetime.datetime.utcnow()
    y = n.year
    m = n.month
    d = n.day
    t = datetime.datetime.combine(datetime.date(1900,1,1), n.time())
    current_sid_local = sidereal_time_local( sidereal_time_greenwich(y, m, d, t))
    print 'Local Sidereal Time in SF right now is: %s' % decdeg2time(current_sid_local).time().isoformat()
    print 'Can verify here: http://tycho.usno.navy.mil/sidereal.html'


def main():
    showoff()

if __name__ == '__main__':
    main()