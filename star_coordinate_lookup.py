#! /usr/bin/env python

# Create a function to look up coordinates for a star or constellation

import BeautifulSoup as bs
import requests
import re
from astro_date_unit_fcns import *

def lookup_star_coordinates(star_name='Arcturus'):
    # just some scratch work that might turn into something
    url = "http://en.wikipedia.org/wiki/" + star_name
    response = requests.get(url)
    soup = bs.BeautifulSoup(response.text)
    txt = soup.find(id="coordinates").text
    # this may work too: soup.find(title='Right ascension').next.next.next
    breakout_text(txt)

def breakout_text(txt):
    # example output: "Coordinates:18h36m56.3364s, +38 47 01.291"
    # first found out if there are 1, 2 or 3 periods
    # right now we assume that the periods only occur in the seconds place but in some cases, e.g. Ursa_Major, the period occurs at the hour & degree level
    # also sometimes the declination is not signed and this will cause problems
    idx = txt.find('.')
    if idx == -1:
        # no periods
        p = re.compile(r'Coordinates:(?P<hr>\d+)h(?P<mn>\d+)m(?P<sec>\d+)s,\s(?P<sgn>\S)(?P<deg>\d+)\D+(?P<degmn>\d+)\D+(?P<degsec>\d+)')
    elif txt[idx+1:].find('.') == -1:
        # only one period but it could be in the Right Asc or the Declination
        # if there's an 's' after the period then it's in the Right Asc, otherwise it's the Declination
        if txt[idx+1:].find('s') > 0:
            # the period is in the right ascension
            p = re.compile(r'Coordinates:(?P<hr>\d+)h(?P<mn>\d+)m(?P<sec>\d+).(?P<secdec>\d+)s,\s(?P<sgn>\S)(?P<deg>\d+)\D+(?P<degmn>\d+)\D+(?P<degsec>\d+)')
        else:
            # period must be in the declination
            p = re.compile(r'Coordinates:(?P<hr>\d+)h(?P<mn>\d+)m(?P<sec>\d+)s,\s(?P<sgn>\S)(?P<deg>\d+)\D+(?P<degmn>\d+)\D+(?P<degsec>\d+).(?P<degsecdec>\d+)')
    else:
        # two periods is the only other option
        p = re.compile(r'Coordinates:(?P<hr>\d+)h(?P<mn>\d+)m(?P<sec>\d+).(?P<secdec>\d+)s,\s(?P<sgn>\S)(?P<deg>\d+)\D+(?P<degmn>\d+)\D+(?P<degsec>\d+).(?P<degsecdec>\d+)')

    # do the crazy regex matching on 'txt'
    m = p.search(txt)
    # make sure to handle the decimals correctly
    if 'secdec' in m.groupdict():
        rtstr = float(m.group('sec') + '.' + m.group('secdec'))
    else:
        rtstr = float(m.group('sec'))
    if 'degsecdec' in m.groupdict():
        decstr = float(m.group('degsec') + '.' + m.group('degsecdec'))
    else:
        decstr = float(m.group('degsec'))

    # breakout the right ascension    
    rt_asc = hms2decdeg(float(m.group('hr')), float(m.group('mn')), rtstr)
    # breakout the declination, handling the signs appropriately
    sgn = 1
    if m.group('sgn') == '-':
        sgn = -1    
    dec = dms2decdeg(sgn * float(m.group('deg')), float(m.group('degmn')), decstr)

    # print out the original text
    print txt
    print 'Right Ascension: %f' %rt_asc
    print 'Declination: %f' %dec

def main():
    # show off some default functionality
    lookup_star_coordinates()

if __name__ == '__main__':
    main()