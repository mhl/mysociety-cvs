#!/usr/bin/python2.5
#
# index.cgi:
# Main code
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: index.cgi,v 1.123 2009-06-07 19:18:36 matthew Exp $
#

import sys
import os.path
sys.path.extend(("../pylib", "../../pylib", "/home/matthew/lib/python"))
import struct
import re
import psycopg2
import Cookie
import psycopg2.errorcodes
import urllib2

import mysociety.config
mysociety.config.set_file("../conf/general")

import page
from page import *
import mysociety.mapit
from mysociety.rabx import RABXException

from django.http import HttpResponseRedirect

from coldb import db
import geoconvert
import isoweb

tmpwork = mysociety.config.get('TMPWORK')

#####################################################################
# Class representing the parameters for a map, and its status

def get_queue_state():
    state = { 'new': 0, 'working': 0, 'complete': 0, 'error' : 0 }
    db().execute('''SELECT state, count(*) FROM map GROUP BY state''')
    for row in db().fetchall():
        state[row[0]] = row[1]
    return state

class Map:
    '''Represents the parameters needed to make one public transport map.
    >>> map = Map({ 'target_postcode' : 'ox13dr' })
    >>> map.title()
    'OX1 3DR'
    >>> map.url()
    '/postcode/OX13DR'

    XXX Does lots of database things not easily tested in doctest
    '''

    state = {}

    # Given URL parameters, look up parameters of map
    def __init__(self, fs):
        # Be sure to properly sanitise any inputs read from fs into this
        # function, so they don't have characters that might need escaping in
        # them. This will make URLs look nicer, and is also assumed by Map.url
        # below.

        if 'station_id' in fs:
            # target is specific station
            self.text_id = page.sanitise_station_id(fs['station_id'])
            db().execute('''SELECT id, X(position_osgb), Y(position_osgb) FROM station WHERE text_id = %s''', (self.text_id,))
            row = db().fetchone()
            self.target_station_id, self.target_e, self.target_n = row
            self.target_postcode = None
        else:
            # target is a grid reference
            if 'target_postcode' in fs:
                self.target_postcode = page.sanitise_postcode(fs['target_postcode'])
                f = mysociety.mapit.get_location(self.target_postcode)
                self.target_e = int(f['easting'])
                self.target_n = int(f['northing'])
            else:
                self.target_postcode = None
                self.target_e = int(fs['target_e'])
                self.target_n = int(fs['target_n'])
            self.target_station_id = None

        # Used for centring map
        self.lat, self.lon = geoconvert.national_grid_to_wgs84(self.target_e, self.target_n)

        # Times, directions and date
        self.target_direction = isoweb.default_target_direction
        if 'target_direction' in fs:
            direction = fs['target_direction']
            if direction in ['arrive_by', 'depart_after']:
                self.target_direction = direction
            else:
                raise Exception("Bad direction parameter specified, only arrive_by and depart_after supported")
        self.target_time = isoweb.default_target_time
        if 'target_time' in fs:
            self.target_time = int(fs['target_time'])
        self.target_limit_time = isoweb.default_target_limit_time(self.target_direction)
        if 'target_limit_time' in fs:
            self.target_limit_time = int(fs['target_limit_time'])
        # XXX date is fixed for now
        self.target_date = isoweb.default_target_date

        # Get record from database
        if self.target_station_id:
            db().execute('''SELECT id, state, working_server FROM map WHERE 
                target_station_id = %s AND 
                target_direction = %s AND
                target_time = %s AND target_limit_time = %s 
                AND target_date = %s''', 
                (self.target_station_id, self.target_direction, self.target_time, self.target_limit_time, self.target_date))
        else:
            db().execute('''SELECT id, state, working_server FROM map WHERE 
                target_e = %s AND target_n = %s AND 
                target_direction = %s AND
                target_time = %s AND target_limit_time = %s 
                AND target_date = %s''', 
                (self.target_e, self.target_n, self.target_direction, self.target_time, self.target_limit_time, self.target_date))
        row = db().fetchone()
        if row is None:
            (self.id, self.current_state, self.working_server) = (None, 'new', None)
        else:
            (self.id, self.current_state, self.working_server) = row

    def current_generation_time(self):
        # Take average time for maps with the same times, taken from the last
        # day, or last 50 at most.
        # XXX will need to make times ranges if we let people enter any time in UI
        db().execute('''SELECT AVG(working_took) FROM 
            ( SELECT working_took FROM map WHERE
                target_direction = %s AND
                target_time = %s AND target_limit_time = %s AND target_date = %s AND
                working_start > (SELECT MAX(working_start) FROM map) - '1 day'::interval 
                ORDER BY working_start DESC LIMIT 50
            ) AS working_took
            ''', 
            (self.target_direction, self.target_time, self.target_limit_time, self.target_date))
        avg_time, = db().fetchone()
        return avg_time or 30

    # How far is making this map? 
    def get_progress_info(self):
        self.state = get_queue_state()

        if self.id:
            db().execute('''SELECT count(*) FROM map WHERE created <= (SELECT created FROM map WHERE id = %s) AND state = 'new' ''', (self.id,))
            self.state['ahead'] = db().fetchone()[0]
            self.maps_to_be_made = self.state['ahead'] + self.state['working']
        else:
            self.maps_to_be_made = self.state['new'] + self.state['working'] + 1

        self.concurrent_map_makers = self.state['working']
        if self.concurrent_map_makers < 1:
            self.concurrent_map_makers = 1

    def title(self):
        # XXX Currently just location, needs to include arrival time etc.
        if self.target_station_id:
            return self.text_id
        elif self.target_postcode:
            return canonicalise_postcode(self.target_postcode)
        else:
            return '%d,%d' % (self.target_e, self.target_n)

    def direction(self):
        if self.target_direction == 'arrive_by':
            return 'arrive'
        elif self.target_direction == 'depart_after':
            return 'depart'

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
        if self.target_direction != isoweb.default_target_direction:
            url_params.append("target_direction=" + str(self.target_direction))
        if self.target_time != isoweb.default_target_time:
            url_params.append("target_time=" + str(self.target_time))
        if self.target_limit_time != isoweb.default_target_limit_time(self.target_direction):
            url_params.append("target_limit_time=" + str(self.target_limit_time))
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
    # Returns False if the insert failed due to an integrity error
    # True otherwise
    def start_generation(self):
        db().execute('BEGIN')
        db().execute("SELECT nextval('map_id_seq')")
        self.id = db().fetchone()[0]
        try:
            db().execute('INSERT INTO map (id, state, target_station_id, target_postcode, target_e, target_n, target_direction, target_time, target_limit_time, target_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (self.id, 'new', self.target_station_id, self.target_postcode, self.target_e, self.target_n, self.target_direction, self.target_time, self.target_limit_time, self.target_date))
        except psycopg2.IntegrityError, e:
            db().execute('ROLLBACK')
            if e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                # The integrity error is because of a unique key violation - ie. an
                # identical row has appeared in the milliseconds since we looked
                self.id = None
                return False
            else:
                raise
        except:
            db().execute('ROLLBACK')
            raise
        db().execute('COMMIT')
        if 'new' in self.state:
            self.state['new'] += 1
            self.state['ahead'] = self.state['new']
        return True

    def target_time_formatted(self):
        return isoweb.format_time(self.target_time)

#####################################################################
# Controllers
 
def check_postcode(pc, invite):
    """Given a postcode, look up grid reference and redirect to a URL
    containing that"""

    vars = {
        'invite': invite,
        'postcode': pc,
    }

    # Check postcode is valid
    try:
        f = mysociety.mapit.get_location(pc)
    except RABXException, e:
        vars['error'] = e.text
        return render_to_response('index.html', vars)

    #(station, station_long, station_id) = isoweb.nearest_station(E, N)
    #if not station:
    #    return render_to_response('index.html', { 'error': 'Could not find a station or bus stop :(' })

    if f['coordsyst'] == 'I':
        vars['error'] = u'I\u2019m afraid we don\u2019t have information for Northern Ireland.'
        return render_to_response('index.html', vars)

    # Canonicalise it, and redirect to that URL
    pc = page.sanitise_postcode(pc)

    return HttpResponseRedirect('/postcode/%s' % (pc))

def map_complete(map, invite):
    # Check there is a route file
    file = os.path.join(tmpwork, '%s.iso' % str(map.id))
    if not os.path.exists(file):
        return render_to_response('map-noiso.html', { 'map_id' : map.id })
    # Let's show the map
    if map.target_direction == 'arrive_by':
        initial_minutes = abs(map.target_time - map.target_limit_time) - 60
    else:
        initial_minutes = 60
    return render_to_response('map.html', {
        'map': map,
        'tile_web_host' : mysociety.config.get('TILE_WEB_HOST'),
        'show_max_minutes': abs(map.target_time - map.target_limit_time),
        'initial_minutes': initial_minutes,
        'invite': invite,
        'show_dropdown': len(invite.postcodes) > 3,
    })

def map(fs, invite):
    # Look up state of map etc.
    map = Map(fs)

    # If the load is too high on the server, don't allow new map
    current_connections = page.current_proxy_connections()
    if current_connections >= page.max_connections:
        return render_to_response('map-http-overload.html', map.add_url_params({ 'current_connections' : current_connections, 'max_connections' : page.max_connections }))

    # If it is complete, then render it
    if map.current_state == 'complete':
        return map_complete(map, invite)

    # See how long it will take to make it
    map.get_progress_info()
    generation_time = map.current_generation_time()
    approx_waiting_time = map.maps_to_be_made * generation_time / float(map.concurrent_map_makers)
    # ... if too long, ask for email
    if map.current_state in ('new', 'working') and approx_waiting_time > 60:
        return render_to_response('map-provideemail.html', map.add_url_params({
            'title': map.title(),
            'state': map.state,
            'approx_waiting_time': int(approx_waiting_time),
        }))

    # If map isn't being made , set it going
    if map.id is None:
        if not map.start_generation():
            map = Map(fs) # Fetch it again, it must be there now

    # Please wait...
    if map.current_state == 'complete':
        return map_complete(map, invite)
    elif map.current_state == 'working':
        server, server_port = map.working_server.split(':')
        return render_to_response('map-working.html', {
            'title': map.title(),
            'approx_waiting_time': round(generation_time),
            'state' : map.state,
            'server': server,
            'server_port': server_port,
            'refresh': int(generation_time)<5 and int(generation_time) or 5,
        })
    elif map.current_state == 'error':
        return render_to_response('map-error.html', { 'map_id' : map.id })
    elif map.current_state == 'new':
        return render_to_response('map-pleasewait.html', {
            'title': map.title(),
            'approx_waiting_time': int(approx_waiting_time),
            'state' : map.state,
            'refresh': 2,
        })
    else:
        raise Exception("unknown state " + map.current_state)

# Email has been given, remember to mail them when map is ready
def log_email(fs, email):
    if not validate_email(email):
        return render_to_response('map-provideemail-error.html', {
            'target_postcode': fs['target_postcode'],
            'email': email,
        })
    # Okay, we have an email, set off the process
    map = Map(fs)
    if map.id is None:
        if not map.start_generation():
            map = Map(fs) # Fetch it again

    db().execute('BEGIN')
    db().execute('INSERT INTO email_queue (email, map_id) VALUES (%s, %s)', (email, map.id))
    db().execute('COMMIT')
    return render_to_response('map-provideemail-thanks.html')

# Used when in Flash you click on somewhere to get the route
def get_route(fs, lat, lon):
    E, N = geoconvert.wgs84_to_national_grid(lat, lon)
    (station, station_long, station_id) = isoweb.nearest_station(E, N)

    # Look up time taken
    map = Map(fs)
    tim = isoweb.look_up_time_taken(map.id, station_id)

    # Look up route...
    location_id = station_id
    route = []
    c = 0 
    while True:
        (next_location_id, next_journey_id) = isoweb.look_up_route_node(map.id, location_id)
        leaving_time = isoweb.look_up_time_taken(map.id, location_id)

        c = c + 1 
        if c > 100:
            raise Exception("route displayer probably in infinite loop")

        route.append((location_id, next_location_id, next_journey_id))
        if next_journey_id == isoweb.JOURNEY_NULL:
            break
        if next_journey_id == isoweb.JOURNEY_ALREADY_THERE:
            break

        location_id = next_location_id
    # ... get station names from database
    ids = ','.join([ str(int(route_node[0])) for route_node in route ]) + "," + str(station_id)
    db().execute('''SELECT text_id, long_description, id FROM station WHERE id in (%s)''' % ids)
    name_by_id = {}
    for row in db().fetchall():
        name_by_id[row['id']] = row['long_description'] + " (" + row['text_id'] + ")"
    name_by_id[isoweb.LOCATION_TARGET] = 'TARGET'
    # ... get journey info from database
    ids = ','.join([ str(int(route_node[2])) for route_node in route ])
    db().execute('''SELECT text_id, vehicle_code, id FROM journey WHERE id in (%s)''' % ids)
    journey_by_id = {}
    vehicle_code_by_id = {}
    for row in db().fetchall():
        journey_by_id[row['id']] = row['text_id']
        vehicle_code_by_id[row['id']] = row['vehicle_code']
    # ... and show it
    route_str = "From " + str(name_by_id[station_id]) + " \n"
    for location_id, next_location_id, journey_id in route:
        location_time = isoweb.look_up_time_taken(map.id, location_id)
        if map.target_direction == 'arrive_by':
            leaving_after_midnight = map.target_time - location_time
        elif map.target_direction == 'depart_after':
            leaving_after_midnight = map.target_time - location_time
        else:
            assert(False)
        route_str += isoweb.format_time(leaving_after_midnight) + " "
        if journey_id > 0: 
            next_location_name = name_by_id[next_location_id]
            vehicle_code = vehicle_code_by_id[journey_id]
            route_str += isoweb.pretty_vehicle_code(vehicle_code) + " (" + journey_by_id[journey_id] + ") to " + next_location_name
        elif journey_id == isoweb.JOURNEY_WALK:
            next_location_name = name_by_id[next_location_id]
            route_str += "Walk to " + next_location_name;
        elif journey_id == isoweb.JOURNEY_ALREADY_THERE:
            location_name = name_by_id[location_id]
            arrived = True
            route_str += "You've arrived"
        elif journey_id == isoweb.JOURNEY_NULL:
            route_str += "No route found"
        route_str += "\n";

    return render_to_response('route.xml', {
        'lat': lat, 'lon': lon,
        'e': E, 'n': N,
        'station' : station,
        'station_long' : station_long,
        'time_taken' : tim,
        'route_str' : route_str
    }, mimetype='text/xml')

#####################################################################
# Main FastCGI loop

def main(fs):
    if 'stats' in fs:
        state = get_queue_state()
        current_connections = page.current_proxy_connections()
        return render_to_response('map-stats.html', {
            'state': state,
            'current_connections' : current_connections, 
            'max_connections' : page.max_connections 
        })

    invite = Invite()
    if not invite.id:
        return HttpResponseRedirect('/signup')

    #got_map_spec = ('station_id' in fs or 'target_e' in fs or 'target_postcode' in fs)
    got_map_spec = ('target_postcode' in fs)

    if 'lat' in fs: # Flash request for route
        return get_route(fs, float(fs['lat']), float(fs['lon']))
    elif 'pc' in fs: # Front page submission
        return check_postcode(fs['pc'], invite)
    elif got_map_spec and 'email' in fs: # Overloaded email request
        return log_email(fs, fs['email'])
    elif got_map_spec: # Page for generating/ displaying map
        postcode = page.sanitise_postcode(fs['target_postcode'])
        postcodes = invite.postcodes
        if (postcode, canonicalise_postcode(postcode)) not in postcodes:
            if invite.maps_left <= 0:
                return render_to_response('beta-limit.html', { 'postcodes': postcodes })
            invite.add_postcode(postcode)
        return map(fs, invite)

    # Front page display
    db().execute('''SELECT target_postcode FROM map WHERE state='complete' AND target_postcode IS NOT NULL
        ORDER BY working_start DESC LIMIT 10''')
    most_recent = [ canonicalise_postcode(row[0]) for row in db().fetchall() ]
    return render_to_response('index.html', {
        'invite': invite,
        'most_recent': most_recent,
        'show_dropdown': len(invite.postcodes) > 3
    })

# Main FastCGI loop
if __name__ == "__main__":
    wsgi_loop(main)


