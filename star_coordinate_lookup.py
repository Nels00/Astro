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
    breakout_text(txt)

def breakout_text(txt):
    # example output: "Coordinates:18h36m56.3364s, +38 47 01.291"
    # perform the crazy regex, this does NOT work if there are no decimals..
    p = re.compile(r'Coordinates:(?P<hr>\d+)h(?P<mn>\d+)m(?P<sec>\d+).(?P<secdec>\d+)s,\s(?P<sgn>\S)(?P<deg>\d+)\D+(?P<degmn>\d+)\D+(?P<degsec>\d+)\D+(?P<degsecdec>\d+)')
    m = p.search(txt)
    # this function needs to be written
    rtstr = float(m.group('sec') + '.' + m.group('secdec'))
    rt_asc = hms2decdeg(float(m.group('hr')), float(m.group('mn')), rtstr)
    # this function also needs to be written
    sng = 1
    if m.group('sgn') == '-':
        sgn = -1
    decstr = float(m.group('degsec') + '.' + m.group('degsecdec'))
    dec = dms2decdeg(float(m.group('deg')), float(m.group('degmn')), decstr)

    # print out the interesting stuff
    print txt
    print 'Right Ascension: '+m.group('hr')+'h'+m.group('mn')+'m'+m.group('sec')+'.'+m.group('secdec')+'s'
    print 'Declination: '+m.group('deg')+'D '+m.group('degmn')+"' "+m.group('degsec')+'.'+m.group('degsecdec')+'"'

def hms2decdeg(x,y,z):
    # just a fake function for now
    return x

def dms2decdeg(x,y,z):
    # just a fake function for now
    return x

def main():
    # for some reason this doesn't work with Arcturus
    lookup_star_coordinates('Vega')

if __name__ == '__main__':
    main()