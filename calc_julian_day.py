#! /usr/bin/env python

# Takes a date and converts it to the Julian Day
import datetime
import pytz

default_Y = 1957
default_M = 10
default_D = 4.81
default_JD = 2436116.31

def julian_day(Y=default_Y, M=default_M, D=default_D):
    # Calculations taking from Chapter 7 of Astronomy Algorithms
    
    # assume that the transition to the gegorian calendar happend in Oct 1582
    if Y < 1582:
        gegorian = False
    elif Y > 1582:
        gegorian = True
    elif M < 10:
        gegorian = False
    elif M > 10:
        gegorian = True
    elif D <= 4:
        gegorian = False
    elif D >= 15:
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

def main():
    pass

if __name__ == '__main__':
    main()