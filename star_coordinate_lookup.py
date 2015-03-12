#! /usr/bin/env python

# Create a function to look up coordinates for a star or constellation

import BeautifulSoup as bs
import requests

def lookup_star_coordinates(star_name='Arcturus'):
    # just some scratch work that might turn into something
    url = "http://en.wikipedia.org/wiki/" + star_name
    response = requests.get(url)
    soup = bs.BeautifulSoup(response.text)
    txt = soup.find(id="coordinates").text
    rs_hrs = float(txt[12:14])
    print rs_hrs

def crazy_regex_example():
    input_text = '1234567890'
    output_text = re.sub(r'\W*1?(\d{3})\W*(\d{3})\W*(\d{4}?)',r'(\1)\2-\3',input_text)

def main():
    pass

if __name__ == '__main__':
    main()