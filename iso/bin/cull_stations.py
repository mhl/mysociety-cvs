#!/usr/bin/python
"""
Set the minimum_zoom for each station in the station table based on proximity and connectedness.

Connectedness is a measure of how "major" a station is, and is meaningful only
to the extent that a more-connected station should beat out a less-connected station.

Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
Email: mike@stamen.com; WWW: http://www.mysociety.org/

$Id: cull_stations.py,v 1.2 2009-04-20 11:41:03 francis Exp $
"""
import os
import sys
import math

sys.path.append("../../pylib")
import mysociety.config
mysociety.config.set_file("../conf/general")

sys.path.append("../pylib")
import coldb

if __name__ == '__main__':
    db = coldb.get_cursor()
 
    # width of the world tile in mercator units = 2 * pi * earth radius
    tile_widths = [6378137 * math.pi * 2]
    
    # set up tile widths, in mercator units, for each zoom level
    for zoom in range(1, 19):
        tile_widths.append(tile_widths[zoom - 1] / 2)
    
    # select all stations still at min. zoom = 0
    db.execute("""SELECT id, text_id, X(position_osgb), Y(position_osgb), connectedness, X(position_merc), Y(position_merc)
                  FROM station
                  WHERE minimum_zoom = 0
                  ORDER BY connectedness ASC""")

    for (id, text_id, easting_osgb, northing_osgb, connectedness, easting_merc, northing_merc) in db.fetchall():

        print "cull_stations.py:", id, text_id, connectedness, easting_osgb, northing_osgb,

        # narrow down a window around the station, searching
        # for nearby stations with a higher journey count.
        for (zoom, tile_width) in enumerate(tile_widths):
            minimum_zoom = zoom

            box_ll = easting_merc - tile_width/256, northing_merc - tile_width/256
            box_ur = easting_merc + tile_width/256, northing_merc + tile_width/256
        
            db.execute("""SELECT id, connectedness
                          FROM station
                          WHERE connectedness > %s
                            AND id != %s
                            AND (position_merc && SetSRID(MakeBox2D(MakePoint(%s, %s), MakePoint(%s, %s)), 900913))
                          LIMIT 1""" \
                        % (connectedness, id, box_ll[0], box_ll[1], box_ur[0], box_ur[1]))

            # if there's no nearby station with a higher journey count,
            # we've reached a zoom level where this one should be shown.
            if db.fetchone() is None:
                break

        print "minimum_zoom", minimum_zoom
        
        db.execute("""UPDATE station SET minimum_zoom = %s + 1
                      WHERE id = %s """ \
                    % (minimum_zoom, id))

        db.execute("COMMIT")
