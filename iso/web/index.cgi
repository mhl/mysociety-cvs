#!/usr/bin/env python2.5
#
# index.cgi:
# Main code
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: index.cgi,v 1.47 2009-04-01 14:30:58 matthew Exp $
#

import re
import sys
import os.path
import traceback
sys.path.extend(("../pylib", "../../pylib", "/home/matthew/lib/python"))
import fcgi
import psycopg2 as postgres
import pyproj

from page import *
import mysociety.config
import mysociety.mapit
mysociety.config.set_file("../conf/general")
from mysociety.rabx import RABXException

db = postgres.connect(
            host=mysociety.config.get('COL_DB_HOST'),
            port=mysociety.config.get('COL_DB_PORT'),
            database=mysociety.config.get('COL_DB_NAME'),
            user=mysociety.config.get('COL_DB_USER'),
            password=mysociety.config.get('COL_DB_PASS')
).cursor()

def lookup(pc):
    """Given a postcode, look up the nearest station ID
    and redirect to a URL containing that"""

    try:
        f = mysociety.mapit.get_location(pc)
    except RABXException, e:
        return Response('index', {
            'error': '<div id="errors">%s</div>' % e
        })

    E = int(f['easting'])
    N = int(f['northing'])

    db.execute('''SELECT text_id FROM station WHERE
        position_osgb && Expand(GeomFromText('POINT(%d %d)', 27700), 50000)
        AND Distance(position_osgb, GeomFromText('POINT(%d %d)', 27700)) < 50000
        ORDER BY Distance(position_osgb, GeomFromText('POINT(%d %d)', 27700))
        LIMIT 1''' % (E, N, E, N, E, N))
    row = db.fetchone()
    if not row:
        return Response('index', {
            'error': '<div id="errors">Could not find a station or bus stop :(</div>'
        })

    return Response(status=302, url='/station/%s' % row[0])

def map(text_id):
    db.execute('BEGIN')
    db.execute('''SELECT id, X(position_osgb), Y(position_osgb) FROM station
        WHERE text_id = %s FOR UPDATE''', (text_id,))
    row = db.fetchone()
    target_station_id, easting, northing = row
    lat, lon = national_grid_to_wgs84(easting, northing)

    # XXX These data are all fixed for now
    target_latest = 540
    target_earliest = 0
    target_date = '2008-10-07'

    db.execute('''SELECT id, state, working_server FROM map WHERE target_station_id = %s
        AND target_latest = %s AND target_earliest = %s AND target_date = %s''', (target_station_id, target_latest, target_earliest, target_date))
    map = db.fetchone()
    if map is None:
        # Start off generation of map!
        db.execute("SELECT nextval('map_id_seq')")
        map_id = db.fetchone()[0]
        db.execute('INSERT INTO map (id, state, target_station_id, target_latest, target_earliest, target_date) VALUES (%s, %s, %s, %s, %s, %s)', (map_id, 'new', target_station_id, target_latest, target_earliest, target_date))
        db.execute('COMMIT')
        current_state = 'new'
        working_server = None
    else:
        map_id = map[0]
        current_state = map[1]
        working_server = map[2]
        db.execute('ROLLBACK')

    tmpwork = mysociety.config.get('TMPWORK')
    file = os.path.join(tmpwork, str(map_id))
    if os.path.exists(file + ".iso"):
        # We've got a generated file, let's show the map!
        return Response('map', {
            'centre_lat': lat,
            'centre_lon': lon,
            'tile_id': map_id,
        }, id='map')

    # Info for progress
    db.execute('''SELECT state, count(*) FROM map GROUP BY state''')
    rows = db.fetchall()
    state = { 'new': 0, 'working': 0, 'complete': 0, 'error' : 0 }
    for row in rows:
        state[row[0]] = row[1]
    db.execute('''SELECT count(*) FROM map WHERE created < (SELECT created FROM map WHERE id = %s) AND state = 'new' ''', (map_id,))
    state['ahead'] = db.fetchone()[0]

    # Please wait...
    if current_state == 'working':
        return Response('map-working', { 'state' : state, 'server' : working_server }, refresh=True, id='map-wait')
    elif current_state == 'error':
        return Response('map-error', { 'map_id' : map_id }, id='map-wait')
    elif current_state == 'new':
        return Response('map-pleasewait', { 'state': state }, refresh=True, id='map-wait')
    else:
        raise Exception("unknown state " + current_state)
    
def main(fs):
    if 'pc' in fs:
        return lookup(fs.getfirst('pc'))
    elif 'station_id' in fs:
        return map(fs.getfirst('station_id'))
    return Response('index')

BNG = pyproj.Proj(proj='tmerc', lat_0=49, lon_0=-2, k=0.999601, x_0=400000, y_0=-100000, ellps='airy', towgs84='446.448,-125.157,542.060,0.1502,0.2470,0.8421,-20.4894', units='m', no_defs=True)
WGS = pyproj.Proj(proj='latlong', towgs84="0,0,0", ellps="WGS84", no_defs=True)

def national_grid_to_wgs84(x, y):
    """Project from British National Grid to WGS-84 lat/lon"""
    lon, lat = pyproj.transform(BNG, WGS, x, y)
    return lat, lon

# Main FastCGI loop
while fcgi.isFCGI():
    fcgi_loop(main)
    db.execute('ROLLBACK')

