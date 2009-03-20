"""
"""
import os
import sys

import pyproj
import Cone

try:
    import psycopg as psycopgN
except ImportError:
    import psycopg2 as psycopgN

def get_db_cursor(*args, **kwargs):
    """
    """
    return psycopgN.connect(*args, **kwargs).cursor()

def get_place_times(map_id, tile, db, log):
    """ Given a result ID, a tile, and a DB cursor, return data points for all the bits that intersect
    """
    # tile bounds in spherical mercator
    xmin, ymin, xmax, ymax = tile.bounds()
    
    if log:
        print >> log, Cone.pixels_per_kilometer(tile)

    ## convert bounds to british national grid
    #xmin, ymin = gym2bng(xmin, ymin)
    #xmax, ymax = gym2bng(xmax, ymax)
    
    # make it true
    xmin, xmax = min(xmin, xmax), max(xmin, xmax)
    ymin, ymax = min(ymin, ymax), max(ymin, ymax)
    
    # adjust by 1800 meters
    xmin, ymin, xmax, ymax = xmin - 1800, ymin - 1800, xmax + 1800, ymax + 1800

    db.execute("""SELECT X(position_merc), Y(position_merc), minutes_to_target
                  FROM place_time
                  WHERE map_id = %d
                    AND Within(position_merc, SetSRID(MakeBox2D(MakePoint(%d, %d), MakePoint(%d, %d)), 900913))""" \
                % (map_id, xmin, ymin, xmax, ymax))

    place_times = db.fetchall()

    if log:
        print >> log, len(place_times), 'place-times within (%d, %d ... %d, %d)' % (xmin, ymin, xmax, ymax)
    
    return place_times

BNG = pyproj.Proj(proj='tmerc', lat_0=49, lon_0=-2, k=0.999601, x_0=400000, y_0=-100000, ellps='airy', towgs84='446.448,-125.157,542.060,0.1502,0.2470,0.8421,-20.4894', units='m', no_defs=True)
GYM = pyproj.Proj(proj='merc', a=6378137, b=6378137, lat_ts=0.0, lon_0=0.0, x_0=0.0, y_0=0, k=1.0, units='m', nadgrids=None, no_defs=True)

def bng2gym(x, y):
    """ Project from British National Grid to spherical mercator
    """
    return GYM(*BNG(x, y, inverse=True))

def gym2bng(x, y):
    """ Project from spherical mercator to British National Grid
    """
    return BNG(*GYM(x, y, inverse=True))

if __name__ == '__main__':
    # if you run this on the command line, you get to put stuff in the database
    map_id = int(sys.argv[1])
    place_times = open(sys.argv[2], 'r')
    db = get_db_cursor(database='mysociety_iso', host='geo.stamen', user='mysociety')
    
    # split the easting, northing, and seconds on each line
    place_times = (line.split() for line in place_times)

    # convert them all to numbers
    place_times = ((float(x), float(y), int(t)) for (x, y, t) in place_times)
    
    for (i, (osgbx, osgby, t)) in enumerate(place_times):
        mercx, mercy = bng2gym(osgbx, osgby)
        
        db.execute("""INSERT INTO place_time
                      (map_id, minutes_to_target, position_osgb, position_merc)
                      VALUES(%d, %d, SetSRID(MakePoint(%.9f, %.9f), 27700), SetSRID(MakePoint(%.9f, %.9f), 900913))""" \
                    % (map_id, t, osgbx, osgby, mercx, mercy))

        if i % 1000 == 0:
            print >> sys.stderr, i

    db.execute('COMMIT')
