#!/usr/bin/python
#
# index.cgi:
# Main code
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: index.cgi,v 1.78 2009-04-30 17:03:53 matthew Exp $
#

import sys
import os.path
sys.path.extend(("../pylib", "../../pylib", "/home/matthew/lib/python"))
import fcgi
import pyproj
import struct
import re

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

# Make sure no bad characters in postcode
def sanitise_postcode(pc):
    pc = pc.upper()
    pc = re.sub('[^A-Z0-9]', '', pc)
    return pc
# Make sure no bad characters in station ID
def sanitise_station_id(text_id):
    text_id = text_id.upper()
    text_id = re.sub('[^A-Z0-9]', '', text_id)
    return text_id

# Used when not specified in URL (so changing will change meaning of old URLs)
default_target_latest = 540
default_target_earliest = 0
default_target_date = '2008-10-07'

class Map:
    state = {}

    # Given URL parameters, look up parameters of map
    def __init__(self, fs, for_update = False):
        if for_update:
            for_update = 'FOR UPDATE';
        else:
            for_update = ''

        # Be sure to properly sanitise any inputs read from fs into this
        # function, so they don't have characters that might need escaping in
        # them. This will make URLs look nicer, and is also assumed by Map.url
        # below.

        if 'station_id' in fs:
            # target is specific station
            text_id = sanitise_station_id(fs.getfirst('station_id'))
            db.execute('''SELECT id, X(position_osgb), Y(position_osgb) FROM station WHERE text_id = %s ''' + for_update, (text_id,))
            row = db.fetchone()
            self.target_station_id, self.target_e, self.target_n = row
            self.target_postcode = None
        else:
            # target is a grid reference
            if 'target_postcode' in fs:
                self.target_postcode = sanitise_postcode(fs.getfirst('target_postcode'))
                f = mysociety.mapit.get_location(self.target_postcode)
                self.target_e = int(f['easting'])
                self.target_n = int(f['northing'])
            else:
                self.target_postcode = None
                self.target_e = int(fs.getfirst('target_e'))
                self.target_n = int(fs.getfirst('target_n'))
            self.target_station_id = None

        # Used for centring map
        self.lat, self.lon = national_grid_to_wgs84(self.target_e, self.target_n)

        # XXX These data are all fixed for now
        self.target_latest = default_target_latest
        if 'target_latest' in fs:
            self.target_latest = int(fs.getfirst('target_latest'))
        self.target_earliest = default_target_earliest
        if 'target_earliest' in fs:
            self.target_earliest = int(fs.getfirst('target_earliest'))
        self.target_date = default_target_date

        # Get record from database
        if self.target_station_id:
            db.execute('''SELECT id, state, working_server FROM map WHERE 
                target_station_id = %s AND 
                target_latest = %s AND target_earliest = %s 
                AND target_date = %s''', 
                (self.target_station_id, self.target_latest, self.target_earliest, self.target_date))
        else:
            db.execute('''SELECT id, state, working_server FROM map WHERE 
                target_e = %s AND target_n = %s AND 
                target_latest = %s AND target_earliest = %s 
                AND target_date = %s''', 
                (self.target_e, self.target_n, self.target_latest, self.target_earliest, self.target_date))
        row = db.fetchone()
        if row is None:
            (self.id, self.current_state, self.working_server) = (None, 'new', None)
        else:
            (self.id, self.current_state, self.working_server) = row

    def current_generation_time(self):
        db.execute('''SELECT AVG(working_took) FROM map WHERE
            working_start > (SELECT MAX(working_start) FROM map) - '1 day'::interval AND
            target_latest = %s AND target_earliest = %s 
            AND target_date = %s''', 
            (self.target_latest, self.target_earliest, self.target_date))
        avg_time, = db.fetchone()
        return avg_time or 10

    # How far is making this map? 
    def get_progress_info(self):
        self.state = { 'new': 0, 'working': 0, 'complete': 0, 'error' : 0 }
        db.execute('''SELECT state, count(*) FROM map GROUP BY state''')
        for row in db.fetchall():
            self.state[row[0]] = row[1]

        if self.id:
            db.execute('''SELECT count(*) FROM map WHERE created < (SELECT created FROM map WHERE id = %s) AND state = 'new' ''', (self.id,))
            self.state['ahead'] = db.fetchone()[0]
            self.maps_to_be_made = self.state['ahead'] + self.state['working']
        else:
            self.maps_to_be_made = self.state['new'] + self.state['working'] + 1

    # Merges hashes for URL into dict and return
    def add_url_params(self, d):
        new_d = d.copy()
        if self.target_station_id:
            new_d.update( { 'station_id' : self.target_station_id } )
        elif self.target_postcode:
            new_d.update( { 'target_postcode': self.target_postcode } )
        else:
            new_d.update( { 'target_e' : self.target_e, 'target_n' : self.target_n } )
        return new_d

    # Construct own URL
    def url(self):
        # We assume members have been properly sanitised when loaded, so there
        # are no characters that need escaping.

        if self.target_station_id:
            url = "/station/" + self.target_station_id
        elif self.target_postcode:
            url = "/postcode/" + self.target_postcode
        elif self.target_e and self.target_n:
            url = "/grid/" + str(self.target_e) + "/" + str(self.target_n)
        else:
            raise Exception("can't make URL")

        url_params = []
        if self.target_latest != default_target_latest:
            url_params.append("target_latest=" + str(self.target_latest))
        if self.target_earliest != default_target_earliest:
            url_params.append("target_earliest=" + str(self.target_earliest))
        if len(url_params) > 0:
            url = url + "?" + "&".join(url_params)
        
        return url

    # Construct own URL, ensure ends inside query parameters so can add more
    # (Flash just appends strings to this URL for e.g. route URL)
    def url_with_params(self):
        ret = self.url()
        if not '?' in ret:
            ret = ret + "?"
        else:
            ret = ret + "&"
        return ret

    # Start off generation of map!
    def start_generation(self):
        db.execute("SELECT nextval('map_id_seq')")
        self.id = db.fetchone()[0]
        db.execute('INSERT INTO map (id, state, target_station_id, target_postcode, target_e, target_n, target_latest, target_earliest, target_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (self.id, 'new', self.target_station_id, self.target_postcode, self.target_e, self.target_n, self.target_latest, self.target_earliest, self.target_date))
        db.execute('COMMIT')
        if 'new' in self.state:
            self.state['ahead'] = self.state['new']
            self.state['new'] += 1

    def target_latest_formatted(self):
        return format_time(self.target_latest)

def format_time(mins_after_midnight):
    hours = mins_after_midnight / 60
    mins = mins_after_midnight % 60
    if hours == 12 and mins == 0:
        return 'noon'
    suffix = hours < 12 and 'am' or 'pm'
    hours = hours % 12
    if hours == 0:
        hours = 12
    time = str(hours)
    if mins:
        time += ':%02d' % mins
    time += suffix
    return time

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

def pretty_vehicle_code(vehicle_code):
    if vehicle_code == 'T':
        return "Train";
    elif vehicle_code == 'B':
        return "Bus";
    elif vehicle_code == 'C':
        return "Coach";
    elif vehicle_code == 'M':
        return "Metro";
    elif vehicle_code == 'A':
        return "Air";
    elif vehicle_code == 'F':
        return "Ferry";
    else:
        assert False;

# Constants from cpplib/makeplan.h
JOURNEY_NULL = -1
JOURNEY_ALREADY_THERE = -2
JOURNEY_WALK = -3

LOCATION_NULL = -1
LOCATION_TARGET = 0

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
 
def check_postcode(pc):
    """Given a postcode, look up grid reference and redirect to a URL
    containing that"""

    # Check postcode is valid
    try:
        f = mysociety.mapit.get_location(pc)
    except RABXException, e:
        return Response('index', {
            'error': '<div id="errors">%s</div>' % e
        })

    #(station, station_long, station_id) = nearest_station(E, N)
    #if not station:
    #    return Response('index', {
    #        'error': '<div id="errors">Could not find a station or bus stop :(</div>'
    #    })

    if f['coordsyst'] == 'I':
        return Response('index', {
            'error': '<div id="errors">I&rsquo;m afraid we don&rsquo;t have information for Northern Ireland.</div>'
        })

    # Canonicalise it, and redirect to that URL
    pc = sanitise_postcode(pc)

    return Response(status=302, url='/postcode/%s' % (pc))

def map(fs, email=''):
    db.execute('BEGIN')
    map = Map(fs, for_update = True)

    if map.current_state == 'complete':
        # Check there is a route file
        file = os.path.join(tmpwork, '%s.iso' % str(map.id))
        if not os.path.exists(file):
            return Response('map-noiso', { 'map_id' : map.id }, id='map-noiso')
        # Let's show the map
        return Response('map', {
            'centre_lat': map.lat,
            'centre_lon': map.lon,
            'tile_id': map.id,
            'tile_web_host' : mysociety.config.get('TILE_WEB_HOST'),
            'target_latest_formatted': map.target_latest_formatted(),
            'route_url_base': map.url_with_params()
        }, id='map')

    # See how long it will take to make it
    map.get_progress_info()
    generation_time = map.current_generation_time()
    approx_waiting_time = map.maps_to_be_made * generation_time
    # ... if too long, ask for email
    if map.current_state in ('new', 'working') and approx_waiting_time > 60:
        return Response('map-provideemail', map.add_url_params({
            'state': map.state,
            'approx_waiting_time': int(approx_waiting_time),
            'email': email,
        }), id='map-wait')

    # If map isn't being made , set it going
    if map.id is None:
        map.start_generation()

    # Please wait...
    if map.current_state == 'working':
        server, server_port = map.working_server.split(':')
        return Response('map-working', {
            'approx_waiting_time': generation_time,
            'state' : map.state,
            'server': server,
            'server_port': server_port,
        }, refresh=int(generation_time)<5 and int(generation_time) or 5, id='map-wait')
    elif map.current_state == 'error':
        return Response('map-error', { 'map_id' : map.id }, id='map-wait')
    elif map.current_state == 'new':
        return Response('map-pleasewait', {
            'approx_waiting_time': int(approx_waiting_time),
            'state' : map.state,
        }, refresh=2, id='map-wait')
    else:
        raise Exception("unknown state " + map.current_state)

# Email has been given, remember to mail them when map is ready
def log_email(fs, email):
    if not validate_email(email):
        return Response('map-provideemail-error', {
            'target_postcode': fs.getfirst('target_postcode'),
            'email': email,
        }, id='map-wait')
    # Okay, we have an email, set off the process
    db.execute('BEGIN')
    map = Map(fs, for_update = True)
    if map.id is None:
        map.start_generation()
    db.execute('INSERT INTO email_queue (email, map_id) VALUES (%s, %s)', (email, map.id))
    db.execute('COMMIT')
    return Response('map-provideemail-thanks', { })

# Used when in Flash you click on somewhere to get the route
def get_route(fs, lat, lon):
    E, N = wgs84_to_national_grid(lat, lon)
    (station, station_long, station_id) = nearest_station(E, N)

    # Look up time taken
    map = Map(fs, for_update = True)
    tim = look_up_time_taken(map.id, station_id)

    # Look up route...
    location_id = station_id
    route = []
    c = 0 
    while True:
        (next_location_id, next_journey_id) = look_up_route_node(map.id, location_id)
        leaving_time = look_up_time_taken(map.id, location_id)

        c = c + 1 
        if c > 100:
            raise Exception("route displayer probably in infinite loop")

        route.append((location_id, next_location_id, next_journey_id))
        if next_journey_id == JOURNEY_NULL:
            break
        if next_journey_id == JOURNEY_ALREADY_THERE:
            break

        location_id = next_location_id
    # ... get station names from database
    ids = ','.join([ str(int(route_node[0])) for route_node in route ]) + "," + str(station_id)
    db.execute('''SELECT text_id, long_description, id FROM station WHERE id in (%s)''' % ids)
    name_by_id = {}
    for row in db.fetchall():
        name_by_id[row['id']] = row['long_description'] + " (" + row['text_id'] + ")"
    name_by_id[LOCATION_TARGET] = 'TARGET'
    # ... get journey info from database
    ids = ','.join([ str(int(route_node[2])) for route_node in route ])
    db.execute('''SELECT text_id, vehicle_code, id FROM journey WHERE id in (%s)''' % ids)
    journey_by_id = {}
    vehicle_code_by_id = {}
    for row in db.fetchall():
        journey_by_id[row['id']] = row['text_id']
        vehicle_code_by_id[row['id']] = row['vehicle_code']
    # ... and show it
    route_str = "From " + str(name_by_id[station_id]) + " \n"
    for location_id, next_location_id, journey_id in route:
        location_time = look_up_time_taken(map.id, location_id)
        leaving_after_midnight = map.target_latest - location_time
        route_str += format_time(leaving_after_midnight) + " "
        if journey_id > 0: 
            next_location_name = name_by_id[next_location_id]
            vehicle_code = vehicle_code_by_id[journey_id]
            route_str += pretty_vehicle_code(vehicle_code) + " (" + journey_by_id[journey_id] + ") to " + next_location_name
        elif journey_id == JOURNEY_WALK:
            next_location_name = name_by_id[next_location_id]
            route_str += "Walk to " + next_location_name;
        elif journey_id == JOURNEY_ALREADY_THERE:
            location_name = name_by_id[location_id]
            arrived = True
            route_str += "You've arrived"
        elif journey_id == JOURNEY_NULL:
            route_str += "No route found"
        route_str += "\n";

    return Response('route', 
            { 'lat': lat, 'lon': lon, 'e': E, 'n': N, 'station' : station, 'station_long' : station_long, 'time_taken' : tim, 'route_str' : route_str},
                type='xml')

#####################################################################
# Main FastCGI loop
    
def main(fs):
    got_map_spec = ('station_id' in fs or 'target_e' in fs or 'target_postcode' in fs)

    if 'lat' in fs:
        return get_route(fs, fs.getfirst('lat'), fs.getfirst('lon'))
    elif 'pc' in fs:
        return check_postcode(fs.getfirst('pc'))
    elif got_map_spec and 'email' in fs:
        return log_email(fs, fs.getfirst('email'))
    elif got_map_spec:
        return map(fs)
    return Response('index')

# Main FastCGI loop
while fcgi.isFCGI():
    fcgi_loop(main)
    db.execute('ROLLBACK')

