#!/usr/bin/python

"""
Populate the stations table.

This script accepts a filename as an argument, which is assumed to be formatted:
    <easting OSGB> <northing OSGB> <connectedness>
    <easting OSGB> <northing OSGB> <connectedness>
    <easting OSGB> <northing OSGB> <connectedness>
    ...
    
...for each station.

Connectedness is a measure of how "major" a station is, and is meaningful only
to the extent that a more-connected station should beat out a less-connected station.

Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
Email: mike@stamen.com; WWW: http://www.mysociety.org/

$Id: populate_stations.py,v 1.4 2009-03-25 15:51:42 francis Exp $
"""
import os
import sys

import pyproj

sys.path.append("../../pylib")
import mysociety.config
mysociety.config.set_file("../conf/general")

try:
    import psycopg2 as postgres
except ImportError:
    import pgdb as postgres

def get_db_cursor(*args, **kwargs):
    """
    """
    return postgres.connect(*args, **kwargs).cursor()

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
    stations = open(sys.argv[1], 'r')
    db = get_db_cursor(
            host=mysociety.config.get('COL_DB_HOST'),
            port=mysociety.config.get('COL_DB_PORT'),
            database=mysociety.config.get('COL_DB_NAME'),
            user=mysociety.config.get('COL_DB_USER'),
            password=mysociety.config.get('COL_DB_PASS')
    )
    db.execute("begin")
    db.execute("delete from station")
    
    # split the easting, northing, and seconds on each line
    stations = (line.split() for line in stations)

    for (i, (text_id, osgbx, osgby, c)) in enumerate(stations):
        (osgbx, osgby, c) = (int(osgbx), int(osgby), int(c))
        mercx, mercy = bng2gym(osgbx, osgby)
        
        try:
            sql_command = """INSERT INTO station
                          (text_id, position_osgb, position_merc, connectedness)
                          VALUES(%s,
                            SetSRID(MakePoint(%s, %s), 27700),
                            SetSRID(MakePoint(%s, %s), 900913),
                            %s
                          )"""
            db.execute(sql_command, (text_id, osgbx, osgby, mercx, mercy, c))

        except postgres.IntegrityError, e:
            print (i, (osgbx, osgby, c))
            continue

#        except postgres.ProgrammingError, e:
#            db = get_db_cursor(database='mysociety_iso', host='geo.stamen', user='mysociety')
#            continue

        else:
            db.execute('COMMIT')

        if i % 1000 == 0:
            print >> sys.stderr, i

