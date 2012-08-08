#!/usr/bin/python

#
# pywwl - Compute distance and azimuth between two Maidenhead squares.
#
# This program is derived from wwl by Diane Bruce (VA3DB).
# See wwl source code for complete credits.
#
# Usage:
# pywwl home_locator [dx_locator]
# If only home_locator is specified, this program returns the coordinates
# of the center of the specified square.
#
# According to original software, this program is distributed under a BSD License.
# Fabio Pani (IZ2UQF)
#

__version__ = "0.1_beta"

import sys
from math import radians, degrees, pi, sin, cos, atan2, sqrt, pow

WWL_LEN	= 6
EARTHRADIUS	= 6371.33

bearing = 0
distance = 0

def isValidLocator(wwl):
	if len(wwl) != WWL_LEN:
		return False
	return not(wwl[0] < 'A' or wwl[0] > 'R' or wwl[1] < 'A' or wwl[1] > 'R' or wwl[2] < '0' or wwl[2] > '9' or wwl[3] < '0' or wwl[3] > '9' or wwl[4] < 'A' or wwl[4] > 'X' or wwl[5] < 'A' or wwl[5] > 'X')

def convertLocator(wwl):
	loc = {}
	charbase = ord('A')
	numbase = ord('0')
	loc['latitude'] = radians((ord(wwl[1]) - charbase) * 10.0 - 90.0 +  (ord(wwl[3]) - numbase) + (ord(wwl[5]) - charbase) / 24.0 + (1.0 / 48.0))
	loc['longitude'] = radians((ord(wwl[0]) - charbase) * 20.0 - 180.0 + (ord(wwl[2]) - numbase) * 2.0 + (ord(wwl[4]) - charbase) / 12.0 + (1.0 / 24.0))
	return loc;

def bearingDistance(my_location, dx_location):
	global bearing
	global distance

	hn = my_location['latitude']
	he = my_location['longitude']
	n = dx_location['latitude']
	e = dx_location['longitude']

	co = cos(he - e) * cos(hn) * cos(n) + sin(hn) * sin(n)
	ca = atan2(sqrt(1 - pow(co, 2)), co)
	az = atan2(sin(e - he) * cos(n) * cos(hn), sin(n) - sin(hn) * cos(ca))
	if az < 0:
		az += 2.0 * pi

	bearing = round(degrees(az), 0)
	distance = round(EARTHRADIUS * ca, 0)
	return

def main():
	if len(sys.argv) < 2:
		print "Usage: pywwl home_locator [dx_locator]"
		return False

	my_wwl = sys.argv[1].upper()
	if not isValidLocator(my_wwl):
		print sys.argv[1], "is not a valid locator"
		return False

	my_location = convertLocator(my_wwl)

	if len(sys.argv) == 2:
		if my_location['longitude'] < 0.0:
			lon = 'W'
		else:
			lon = 'E'

		if my_location['latitude'] > 0.0:
			lat = 'N'
		else:
			lat = 'S'

		print "Locator    :", sys.argv[1]
		print "Coordinates: Long:", lon, round(degrees(my_location['longitude']), 2), "Lat :", lat, round(degrees(my_location['latitude']), 2)
		return True

	dx_wwl = sys.argv[2].upper()
	dx_location = convertLocator(dx_wwl)
	if not isValidLocator(dx_wwl):
		print sys.argv[2], "is not a valid locator"
		return False

	bearingDistance(my_location, dx_location)
	print "qrb:", int(distance), "kilometers, azimuth:", int(bearing), "degrees"
	return True

if __name__ == '__main__':
	main()