"""
"""
import os
import sys
import struct

import pyproj
import Cone

try:
    import psycopg2 as postgres
except ImportError:
    import pgdb as postgres

def get_db_cursor(*args, **kwargs):
    """
    """
    return postgres.connect(*args, **kwargs).cursor()

def get_place_times(map_id, tile, db, log, tmpwork):
    """ Given a result ID, a tile, and a DB cursor, return data points for all the bits that intersect
    """
    # tile bounds in spherical mercator
    xmin, ymin, xmax, ymax = tile.bounds()
    
    if log:
        print >> log, 'cone pixels per km', Cone.pixels_per_kilometer(tile)

    ## convert bounds to british national grid
    #xmin, ymin = gym2bng(xmin, ymin)
    #xmax, ymax = gym2bng(xmax, ymax)
    
    # make it true
    xmin, xmax = min(xmin, xmax), max(xmin, xmax)
    ymin, ymax = min(ymin, ymax), max(ymin, ymax)
    
    # adjust by 1800 meters
    xmin, ymin = gym2bng(xmin, ymin)
    xmax, ymax = gym2bng(xmax, ymax)
    xmin, ymin, xmax, ymax = xmin - 1800, ymin - 1800, xmax + 1800, ymax + 1800
    xmin, ymin = bng2gym(xmin, ymin)
    xmax, ymax = bng2gym(xmax, ymax)
    
    # look at stations in database to find out which are on this tile
    capped_cull_zoom = max(tile.z, 9) # zoomed out culling is excessive and loses too much detail
    db.execute("""SELECT X(position_merc), Y(position_merc), id
                  FROM station
                  WHERE 
                    minimum_zoom <= %s
                    AND (position_merc && SetSRID(MakeBox2D(MakePoint(%s, %s), MakePoint(%s, %s)), 900913))""" \
                % (capped_cull_zoom, xmin, ymin, xmax, ymax))
    db_results = db.fetchall()

    # look up each of those stations in the binary distances .iso file made by isodaemon.py
    iso_file = tmpwork + "/" + repr(map_id) + ".iso"
    isof = open(iso_file, 'rb')
    place_times = []
    for (x, y, id) in db_results:
        # the .iso file is just a list of shorts, containing times in minutes, 
        # in order of location id, so we can just seek by location id
        isof.seek(id * 2)
        tim_bytes = isof.read(2)
	if len(tim_bytes) != 2:
		raise Exception("failed to unpack x:%s y:%s station id:%s map id: %s bytes:%s" % (repr(x), repr(y), repr(id), repr(map_id), repr(tim_bytes)))
        tim = struct.unpack("h", tim_bytes)[0]
        if tim != -1:
            secs = tim * 60 
            place_times.append((x, y, secs ))
    isof.close()

#    raise Exception(repr(place_times))

    if log:
        print >> log, len(place_times), 'place-times within (%f, %f ... %f, %f) at zoom %d' % (xmin, ymin, xmax, ymax, tile.z)
    
    return place_times

BNG = pyproj.Proj(proj='tmerc', lat_0=49, lon_0=-2, k=0.999601, x_0=400000, y_0=-100000, ellps='airy', towgs84='446.448,-125.157,542.060,0.1502,0.2470,0.8421,-20.4894', units='m', no_defs=True)
GYM = pyproj.Proj(proj='merc', a=6378137, b=6378137, lat_ts=0.0, lon_0=0.0, x_0=0.0, y_0=0, k=1.0, units='m', nadgrids=None, no_defs=True)

def bng2gym(x, y):
    """ Project from British National Grid to spherical mercator
    """
    return pyproj.transform(BNG, GYM, x, y)

def gym2bng(x, y):
    """ Project from spherical mercator to British National Grid
    """
    return pyproj.transform(GYM, BNG, x, y)

