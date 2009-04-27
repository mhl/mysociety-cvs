#!/usr/bin/python
#
# index.cgi:
# Main code
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: index.cgi,v 1.57 2009-04-27 15:33:31 francis Exp $
#

import re
import sys
import os.path
import traceback
sys.path.extend(("../pylib", "../../pylib", "/home/matthew/lib/python"))
import fcgi
import psycopg2 as postgres
import pyproj
import struct

from page import *
import mysociety.config
import mysociety.mapit
mysociety.config.set_file("../conf/general")
from mysociety.rabx import RABXException

import coldb

db = coldb.get_cursor()

tmpwork = mysociety.config.get('TMPWORK')

#####################################################################
# Helper functions

def nearest_station(E, N):
    db.execute('''SELECT text_id, long_description, id FROM station WHERE
        position_osgb && Expand(GeomFromText('POINT(%d %d)', 27700), 50000)
        AND Distance(position_osgb, GeomFromText('POINT(%d %d)', 27700)) < 50000
        ORDER BY Distance(position_osgb, GeomFromText('POINT(%d %d)', 27700))
        LIMIT 1''' % (E, N, E, N, E, N))
    row = db.fetchone()

    if not row:
        return None

    return row

def current_generation_time():
    db.execute('''SELECT AVG(working_took) FROM map WHERE working_start > (SELECT MAX(working_start) FROM map) - '1 day'::interval;''')
    avg_time, = db.fetchone()
    return avg_time

def get_map(text_id):
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

    return (map, target_latest, target_earliest, target_date, target_station_id, easting, northing, lat, lon)

def format_time(mins_after_midnight):
    hours = mins_after_midnight / 60
    mins = mins_after_midnight % 60
    return "%02d:%02d:00" % (hours, mins)

def look_up_time_taken(map_id, station_id):
    iso_file = tmpwork + "/" + repr(map_id) + ".iso"
    isof = open(iso_file, 'rb')
    isof.seek(station_id * 2)
    tim = struct.unpack("h", isof.read(2))[0]
    return tim

def look_up_route_node(map_id, station_id):
    iso_file = tmpwork + "/" + repr(map_id) + ".iso.routes"
    isof = open(iso_file, 'rb')
    isof.seek(station_id * 8)
    location_id = struct.unpack("i", isof.read(4))[0]
    journey_id = struct.unpack("i", isof.read(4))[0]
    return (location_id, journey_id)

# Constants from cpplib/makeplan.h
JOURNEY_NULL = -1
JOURNEY_ALREADY_THERE = -2
JOURNEY_WALK = -3

BNG = pyproj.Proj(proj='tmerc', lat_0=49, lon_0=-2, k=0.999601, x_0=400000, y_0=-100000, ellps='airy', towgs84='446.448,-125.157,542.060,0.1502,0.2470,0.8421,-20.4894', units='m', no_defs=True)
WGS = pyproj.Proj(proj='latlong', towgs84="0,0,0", ellps="WGS84", no_defs=True)

def national_grid_to_wgs84(x, y):
    """Project from British National Grid to WGS-84 lat/lon"""
    lon, lat = pyproj.transform(BNG, WGS, x, y)
    return lat, lon

def wgs84_to_national_grid(lat, lon):
    """Project from WGS-84 lat/lon to British National Grid"""
    x, y = pyproj.transform(WGS, BNG, lon, lat)
    return x, y

#####################################################################
# Controllers
 
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

    (station, station_long, station_id) = nearest_station(E, N)

    if not station:
        return Response('index', {
            'error': '<div id="errors">Could not find a station or bus stop :(</div>'
        })

    return Response(status=302, url='/station/%s' % station)

def map(text_id):
    db.execute('BEGIN')
    (map, target_latest, target_earliest, target_date, target_station_id, easting, northing, lat, lon) = get_map(text_id)

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

    tile_web_host = mysociety.config.get('TILE_WEB_HOST')
    file = os.path.join(tmpwork, str(map_id))
    if current_state == 'complete':
        # Check there is a route file
        if not os.path.exists(file + ".iso"):
            return Response('map-noiso', { 'map_id' : map_id }, id='map-noiso')
        # Let's show the map
        return Response('map', {
            'centre_lat': lat,
            'centre_lon': lon,
            'tile_id': map_id,
            'tile_web_host' : tile_web_host,
        }, id='map')

    # Info for progress
    state = { 'new': 0, 'working': 0, 'complete': 0, 'error' : 0 }
    db.execute('''SELECT count(*) FROM map WHERE created < (SELECT created FROM map WHERE id = %s) AND state = 'new' ''', (map_id,))
    state['ahead'] = db.fetchone()[0]
    db.execute('''SELECT state, count(*) FROM map GROUP BY state''')
    for row in db.fetchall():
        state[row[0]] = row[1]

    # Pseudo-code
    if not fs.getfirst('wait') and current_state in ('new', 'working') and state['ahead'] * current_generation_time() > 60:
        return Response('map-provideemail', { 'state': state }, id='map-wait')

    # Please wait...
    if current_state == 'working':
        return Response('map-working', { 'state' : state, 'server' : working_server }, refresh=3, id='map-wait')
    elif current_state == 'error':
        return Response('map-error', { 'map_id' : map_id }, id='map-wait')
    elif current_state == 'new':
        return Response('map-pleasewait', { 'state': state }, refresh=2, id='map-wait')
    else:
        raise Exception("unknown state " + current_state)

# Used when in Flash you click on somewhere to get the route
def get_route(text_id, lat, lon):
    E, N = wgs84_to_national_grid(lat, lon)
    (station, station_long, station_id) = nearest_station(E, N)

    # Look up time taken
    (map, target_latest, target_earliest, target_date, target_station_id, easting, northing, lat, lon) = get_map(text_id)
    map_id = map[0]
    tim = look_up_time_taken(map_id, station_id)

    # Look up route...
    location_id = station_id
    route = []
    c = 0 
    while True:
        (next_location_id, next_journey_id) = look_up_route_node(map_id, location_id)
        leaving_time = look_up_time_taken(map_id, location_id)

        c = c + 1 
        if c > 100:
            raise Exception("route displayer probably in infinite loop")

        route.append((location_id, next_location_id, next_journey_id))
        if next_journey_id == JOURNEY_ALREADY_THERE:
            break

        location_id = next_location_id
    # ... get station names from database
    ids = ','.join([ str(int(route_node[0])) for route_node in route ]) + "," + str(station_id)
    db.execute('''SELECT text_id, long_description, id FROM station WHERE id in (%s)''' % ids)
    name_by_id = {}
    for row in db.fetchall():
        name_by_id[row[2]] = row[1] + " (" + row[0] + ")"
    # ... and show it
    route_str = "From " + str(name_by_id[station_id]) + " \n"
    for location_id, next_location_id, journey_id in route:
        location_time = look_up_time_taken(map_id, location_id)
        leaving_after_midnight = target_latest - location_time
        route_str += format_time(leaving_after_midnight) + " "
        if journey_id > 0: 
            next_location_name = name_by_id[next_location_id]
            route_str += "Leave to " + next_location_name;
        elif journey_id == JOURNEY_WALK:
            next_location_name = name_by_id[next_location_id]
            route_str += "Leave to " + next_location_name + " by walking";
        elif journey_id == JOURNEY_ALREADY_THERE:
            location_name = name_by_id[location_id]
            route_str += "You've at " + location_name;
        route_str += "\n";

    """
        if (next_journey_id > 0) {
            const Journey& journey = this->journeys[next_journey_id];
            const Location& next_location = this->locations[route_node.location_id];
            ret += (boost::format("    %s Leave to %s by %s %s\n") % format_time(leaving_time) % next_location.text_id % journey.pretty_vehicle_type() % journey.text_id).str();
            location_id = route_node.location_id;
        } else if (next_journey_id == JOURNEY_WALK) {
            const Location& next_location = this->locations[route_node.location_id];
            ret += (boost::format("    %s Leave to %s by walking\n") % format_time(leaving_time) % next_location.text_id).str();
            location_id = route_node.location_id;
        } else if (next_journey_id == JOURNEY_ALREADY_THERE) {
            ret += (boost::format("    %s You've arrived at %s\n") % format_time(leaving_time) % location.text_id).str();
            break;
        } else {
            assert(0);
        }
    """

    return Response('route', 
            { 'lat': lat, 'lon': lon, 'e': E, 'n': N, 'station' : station, 'station_long' : station_long, 'time_taken' : tim, 'route_str' : route_str},
                type='xml')

#####################################################################
# Main FastCGI loop
    
def main(fs):
    if 'lat' in fs:
        return get_route(fs.getfirst('station_id'), fs.getfirst('lat'), fs.getfirst('lon'))
    elif 'pc' in fs:
        return lookup(fs.getfirst('pc'))
    elif 'station_id' in fs:
        return map(fs.getfirst('station_id'))
    return Response('index')

# Main FastCGI loop
while fcgi.isFCGI():
    fcgi_loop(main)
    db.execute('ROLLBACK')

