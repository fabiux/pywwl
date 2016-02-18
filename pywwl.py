#!/usr/bin/python
"""
pywwl - Compute distance and azimuth between two Maidenhead squares.

This program is derived from wwl by Diane Bruce (VA3DB).
See wwl source code for complete credits.

Usage:
pywwl home_locator [dx_locator]
If only home_locator is specified, this program returns the coordinates
of the center of the specified square.

According to original software, this program is distributed under a BSD License.

@license: BSD
@author: Fabio Pani (IZ2UQF)
@version: 0.2_beta
"""
import sys
import wwl

__version__ = "0.2_beta"


def main():
    if len(sys.argv) < 2:
        print "Usage: pywwl home_locator [dx_locator]"
        return False

    my_wwl = sys.argv[1].upper()
    if not wwl.is_valid_locator(my_wwl):
        print sys.argv[1], "is not a valid locator"
        return False

    my_location = wwl.convert_locator(my_wwl)

    if len(sys.argv) == 2:
        print "Locator    :", sys.argv[1]
        print "Coordinates: Long:", wwl.get_longitude(my_location), "- Lat:", wwl.get_latitude(my_location)
        return True

    dx_wwl = sys.argv[2].upper()
    dx_location = wwl.convert_locator(dx_wwl)
    if not wwl.is_valid_locator(dx_wwl):
        print sys.argv[2], "is not a valid locator"
        return False

    wwl.bearing_distance(my_location, dx_location)
    print "qrb:", int(round(wwl.distance, 0)), "kilometers, azimuth:", int(round(wwl.bearing, 0)), "degrees"
    return True

if __name__ == '__main__':
    main()
