"""
Set the minimum_zoom for each station in the stations table based on proximity and connectedness.

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

$Id: cull_stations.py,v 1.2 2009-03-25 00:44:59 migurski Exp $
"""
import os
import sys
import math

try:
    import psycopg2 as postgres
except ImportError:
    import pgdb as postgres

def get_db_cursor(*args, **kwargs):
    """
    """
    return postgres.connect(*args, **kwargs).cursor()

if __name__ == '__main__':
    db = get_db_cursor(database='mysociety_iso', host='geo.stamen', user='mysociety')
    
    # width of the world tile in mercator units = 2 * pi * earth radius
    tile_widths = [6378137 * math.pi * 2]
    
    # set up tile widths, in mercator units, for each zoom level
    for zoom in range(1, 19):
        tile_widths.append(tile_widths[zoom - 1] / 2)
    
    # select all stations still at min. zoom = 0
    db.execute("""SELECT easting_osgb, northing_osgb, connectedness, X(position_merc), Y(position_merc)
                  FROM stations
                  WHERE minimum_zoom = 0
                  ORDER BY connectedness ASC""")

    for (easting_osgb, northing_osgb, connectedness, easting_merc, northing_merc) in db.fetchall():

        print connectedness, easting_osgb, northing_osgb,

        # narrow down a window around the station, searching
        # for nearby stations with a higher journey count.
        for (zoom, tile_width) in enumerate(tile_widths):
            minimum_zoom = zoom

            box_ll = easting_merc - tile_width/256, northing_merc - tile_width/256
            box_ur = easting_merc + tile_width/256, northing_merc + tile_width/256
        
            db.execute("""SELECT easting_osgb, northing_osgb, connectedness
                          FROM stations
                          WHERE connectedness > %d
                            AND easting_osgb != %d
                            AND northing_osgb != %d
                            AND Within(position_merc, SetSRID(MakeBox2D(MakePoint(%d, %d), MakePoint(%d, %d)), 900913))
                          LIMIT 1""" \
                        % (connectedness, easting_osgb, northing_osgb, box_ll[0], box_ll[1], box_ur[0], box_ur[1]))

            # if there's no nearby station with a higher journey count,
            # we've reached a zoom level where this one should be shown.
            if db.fetchone() is None:
                break

        print minimum_zoom
        
        db.execute("""UPDATE stations SET minimum_zoom = %d + 1
                      WHERE easting_osgb = %d
                        AND northing_osgb = %d""" \
                    % (minimum_zoom, easting_osgb, northing_osgb))

        db.execute("COMMIT")
