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

$Id: populate_stations.py,v 1.11 2009-04-20 11:41:03 francis Exp $
"""

import os
import sys

sys.path.append('/home/matthew/lib/python')
import pyproj

sys.path.append("../../pylib")
import mysociety.config
mysociety.config.set_file("../conf/general")

import coldb

BNG = pyproj.Proj(proj='tmerc', lat_0=49, lon_0=-2, k=0.999601, x_0=400000, y_0=-100000, ellps='airy', towgs84='446.448,-125.157,542.060,0.1502,0.2470,0.8421,-20.4894', units='m', no_defs=True)
GYM = pyproj.Proj(proj='merc', a=6378137, b=6378137, lat_ts=0.0, lon_0=0.0, x_0=0.0, y_0=0, k=1.0, units='m', nadgrids=None, no_defs=True)

if __name__ == '__main__':
    # if you run this on the command line, you get to put stuff in the database
    stations = open(sys.argv[1], 'r')
    db = coldb.get_cursor()
    db.execute("delete from station")
    
    for (i, line) in enumerate(stations):
        #print "populate_stations.py:", line.strip()

        # split the NPTDR id, easting, northing, and seconds on each line
        (id, text_id, osgbx, osgby, c) = line.split()

        (osgbx, osgby, c) = (int(osgbx), int(osgby), int(c))
        mercx, mercy = pyproj.transform(BNG, GYM, osgbx, osgby)
        
        try:
            sql_command = """INSERT INTO station
                          (id, text_id, position_osgb, position_merc, connectedness)
                          VALUES(%s, %s,
                            SetSRID(MakePoint(%s, %s), 27700),
                            SetSRID(MakePoint(%s, %s), 900913),
                            %s
                          )"""
            db.execute(sql_command, (id, text_id, osgbx, osgby, mercx, mercy, c))

        except postgres.IntegrityError, e:
            print "IntegrityError", (i, (osgbx, osgby, c))
            continue

        else:
            db.execute('COMMIT')

        if i % 1000 == 0:
            print >> sys.stderr, "station number", i

