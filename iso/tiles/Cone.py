"""
Create appropriately-sized isochrones for single points, modeled as
numpy array cones where value = travel time from center, in seconds.

Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
Email: mike@stamen.com; WWW: http://www.mysociety.org/

$Id: Cone.py,v 1.5 2009-05-01 00:22:41 francis Exp $

>>> import Isochrones
>>> xmin, ymin = GYM(-123, 37)
>>> xmax, ymax = GYM(-122, 38)
>>> tile = Isochrones.TileStub(1000, 1000, xmin, ymin, xmax, ymax)
>>> '%.6f' % pixels_per_kilometer(tile)
'12.312128'

>>> cone = make_cone(4)
>>> cone[3,3], cone[4,4]
(0, 0)
>>> cone[0,0] >= 2400, cone[7,7] >= 2400
(True, True)

>>> cone = make_cone(8)
>>> cone[7,7], cone[8,8]
(0, 0)
>>> cone[0,0] >= 2400, cone[15,15] >= 2400
(True, True)

>>> cone = make_cone(16)
>>> cone[15,15], cone[16,16]
(0, 0)
>>> cone[0,0] >= 2400, cone[31,31] >= 2400
(True, True)
"""
import math
import numpy
import pyproj

GYM = pyproj.Proj(proj='merc', a=6378137, b=6378137, lat_ts=0.0, lon_0=0.0, x_0=0.0, y_0=0, k=1.0, units='m', nadgrids=None, no_defs=True)

def kilometers_between(lat1, lon1, lat2, lon2):
    """ Number of kilometers between two locations on spherical globe given in degrees.
    """

    if lat1 == lat2 and lon1 == lon2:
        return 0.0

    # lat/lon in radians
    rad1 = (lat1 * math.pi/180, lon1 * math.pi/180)
    rad2 = (lat2 * math.pi/180, lon2 * math.pi/180)
    
    # vector in x, y, z
    point1 = (math.sin(rad1[1]), math.cos(rad1[1]), math.sin(rad1[0]))
    point2 = (math.sin(rad2[1]), math.cos(rad2[1]), math.sin(rad2[0]))
    
    # vector length
    norm1 = math.sqrt(math.pow(point1[0], 2) + math.pow(point1[1], 2) + math.pow(point1[2], 2))
    norm2 = math.sqrt(math.pow(point2[0], 2) + math.pow(point2[1], 2) + math.pow(point2[2], 2))
    
    # dot product
    dot = sum(map(lambda x, y: (x * y), point1, point2))
    
    # angle between them
    angle = math.acos(dot / (norm1 * norm2))
    
    # assuming earth radius in kilometers = 6378.137
    return angle * 6378.137

def pixels_per_kilometer(tile):
    """ Number of pixels per kilometer of spherical globe in current projection.
    """
    xmin, ymin, xmax, ymax = tile.bounds()
    width, height = tile.size()
    
    lon1, lat1 = GYM(xmin, ymin, inverse=True)
    lon2, lat2 = GYM(xmax, ymax, inverse=True)
    
    assert -90 <= lat1 and lat1 <= 90
    assert -90 <= lat2 and lat2 <= 90
    assert -180 <= lon1 and lon1 <= 180
    assert -180 <= lon2 and lon2 <= 180

    distance1 = kilometers_between(lat1, lon1, lat2, lon2)
    distance2 = kilometers_between(lat1, lon2, lat2, lon1)
    average_distance = (distance1 + distance2) / 2
    
    return math.hypot(width, height) / average_distance

def make_cone(radius):
    """ Floating point cone array of height = 1.0 with a given radius.
    """
    # shorter vars
    r, d = int(radius), int(radius) * 2

    # make an array, then isolate the bottom right corner
    cone = numpy.empty((d, d), dtype=numpy.int32)
    corner = cone[r:,r:]
    
    # do bottom-right quadrant of cone
    for x in range(r):
        for y in range(r):
            corner[x, y] = 2400 * math.hypot(x, y) / r

    # flip and copy to other three quadrants
    cone[:r,:r] = numpy.flipud(numpy.fliplr(corner)) # top left
    cone[:r,r:] = numpy.flipud(corner) # top right
    cone[r:,:r] = numpy.fliplr(corner) # bottom left
    
    return cone

if __name__ == '__main__':
    import doctest
    doctest.testmod()
