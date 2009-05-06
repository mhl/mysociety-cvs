#
# geoconvert.py:
# Convert between coordinate systems.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: geoconvert.py,v 1.2 2009-05-06 16:53:34 francis Exp $
#

import pyproj
import math

BNG = pyproj.Proj(proj='tmerc', lat_0=49, lon_0=-2, k=0.999601, x_0=400000, y_0=-100000, ellps='airy', towgs84='446.448,-125.157,542.060,0.1502,0.2470,0.8421,-20.4894', units='m', no_defs=True)
WGS = pyproj.Proj(proj='latlong', towgs84="0,0,0", ellps="WGS84", no_defs=True)
GYM = pyproj.Proj(proj='merc', a=6378137, b=6378137, lat_ts=0.0, lon_0=0.0, x_0=0.0, y_0=0, k=1.0, units='m', nadgrids=None, no_defs=True)

def national_grid_to_wgs84(x, y):
    """Project from British National Grid to WGS-84 lat/lon"""
    lon, lat = pyproj.transform(BNG, WGS, x, y)
    return lat, lon

def wgs84_to_national_grid(lat, lon):
    """Project from WGS-84 lat/lon to British National Grid"""
    x, y = pyproj.transform(WGS, BNG, lon, lat)
    return x, y

def bng2gym(x, y):
    """ Project from British National Grid to spherical mercator
    """
    return pyproj.transform(BNG, GYM, x, y)

def gym2bng(x, y):
    """ Project from spherical mercator to British National Grid
    """
    return pyproj.transform(GYM, BNG, x, y)

def wgs84_to_tile(lat_deg, lon_deg, zoom):
    lat_rad = lat_deg / 360.0 * 2.0 * math.pi
    n = 2 ** zoom
    xtile = ((lon_deg + 180.0) / 360.0) * n
    ytile = (1.0 - (math.log(math.tan(lat_rad) + 1.0 / math.cos(lat_rad)) / math.pi)) / 2.0 * n
    return (xtile, ytile)

