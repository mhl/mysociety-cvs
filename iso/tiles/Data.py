"""
"""
import os
import sys
import struct
import psycopg2 as postgres

import Cone

sys.path.extend(("../pylib", "../../pylib", "/home/matthew/lib/python"))
import geoconvert

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
    #xmin, ymin = geoconvert.gym2bng(xmin, ymin)
    #xmax, ymax = geoconvert.gym2bng(xmax, ymax)
    
    # make it true
    xmin, xmax = min(xmin, xmax), max(xmin, xmax)
    ymin, ymax = min(ymin, ymax), max(ymin, ymax)
    
    # adjust by 2400 meters
    xmin, ymin = geoconvert.gym2bng(xmin, ymin)
    xmax, ymax = geoconvert.gym2bng(xmax, ymax)
    xmin, ymin, xmax, ymax = xmin - 2400, ymin - 2400, xmax + 2400, ymax + 2400
    xmin, ymin = geoconvert.bng2gym(xmin, ymin)
    xmax, ymax = geoconvert.bng2gym(xmax, ymax)
    
    # look at stations in database to find out which are on this tile
    capped_cull_zoom = max(tile.z, 9) # zoomed out culling is excessive and loses too much detail
    db.execute("""SELECT X(position_merc), Y(position_merc), id
                  FROM station
                  WHERE 
                    minimum_zoom <= %s
                    AND (position_merc && SetSRID(MakeBox2D(MakePoint(%s, %s), MakePoint(%s, %s)), 900913))""",
                (capped_cull_zoom, xmin, ymin, xmax, ymax))
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

    # add in origin station if there is one, and it is in the set
    db.execute("""SELECT target_e, target_n from map WHERE id = %s""", (map_id,))
    row = db.fetchone()
    if row[0]:
        x, y = geoconvert.bng2gym(row[0], row[1])
        # print >> log, "got origin station merc: x ", xmin, x, xmax, " y ", ymin, y, ymax, " grid: ", row[0], row[1]
        if xmin < x < xmax and ymin < y < ymax:
            place_times.append((x, y, 0))

#    raise Exception(repr(place_times))

    if log:
        print >> log, len(place_times), 'place-times within (%f, %f ... %f, %f) at zoom %d' % (xmin, ymin, xmax, ymax, tile.z)
    
    return place_times


