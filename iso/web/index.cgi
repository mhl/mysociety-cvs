#!/usr/bin/python2.5
#
# index.cgi:
# Main code
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: index.cgi,v 1.134 2009-10-16 20:21:04 duncan Exp $
#

import sys
import os.path
sys.path.extend(("../pylib", "../../pylib", "/home/matthew/lib/python"))

import mysociety.config
mysociety.config.set_file("../conf/general")

import page
import mysociety.mapit
from mysociety.rabx import RABXException

from django.http import HttpResponseRedirect

from coldb import db
import geoconvert
import isoweb
import storage
import utils

tmpwork = mysociety.config.get('TMPWORK')

#####################################################################
# Class representing the parameters for a map, and its status

class Map:
    '''Represents the parameters needed to make one public transport map.
    >>> map = Map({ 'target_postcode' : 'ox13dr' })
    >>> map.title()
    'OX1 3DR'
    >>> map.url()
    '/postcode/OX13DR'

    XXX Does lots of database things not easily tested in doctest
    '''

    # Given URL parameters, look up parameters of map
    def __init__(self, fs):
        # Be sure to properly sanitise any inputs read from fs into this
        # function, so they don't have characters that might need escaping in
        # them. This will make URLs look nicer, and is also assumed by Map.url
        # below.

        if 'station_id' in fs:
            # target is specific station
            self.text_id = page.sanitise_station_id(fs['station_id'])
            self.target_station_id, self.target_e, self.target_n = storage.get_station_coords(self.text_id)
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

    def title(self):
        # XXX Currently just location, needs to include arrival time etc.
        if self.target_station_id:
            return self.text_id
        elif self.target_postcode:
            return utils.canonicalise_postcode(self.target_postcode)
        else:
            return '%d,%d' % (self.target_e, self.target_n)

    def flash_direction(self):
        if self.target_direction == 'arrive_by':
            return 'arrive'
        elif self.target_direction == 'depart_after':
            return 'depart'

    def flash_hover_text(self):
        if self.target_direction == 'arrive_by':
            return 'to the chosen destination'
        elif self.target_direction == 'depart_after':
            return 'from the chosen starting point'

    # Merges hashes for URL into dict and return
    def get_url_params(self):
        new_d = {}

        if self.target_station_id:
            new_d['station_id'] = self.target_station_id
        elif self.target_postcode:
            new_d['target_postcode'] =  self.target_postcode
        else:
            new_d['target_e'] = self.target_e
            new_d['target_n'] = self.target_n

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

    def start_generation(self):
        self.id = storage.queue_map(self.target_station_id, self.target_postcode, self.target_e, self.target_n, self.target_direction, self.target_time, self.target_limit_time, self.target_date)

#         if 'new' in self.state:
#             self.state['new'] += 1

#             # Duncan: I'm confused as to what this next line does. Why
#             # would we want to change the number of maps ahead in the
#             # queue to state['new']?
#             self.state['ahead'] = self.state['new']

        # This should be True if the map has been queued, and false, otherwise.
        return self.id

    def target_time_formatted(self):
        return isoweb.format_time(self.target_time)

#####################################################################
# Controllers
 
def check_postcode(pc, invite):
    """Given a postcode, look up grid reference and redirect to a URL
    containing that"""

    context = {
        'invite': invite,
        'postcode': pc,
    }

    # Check postcode is valid
    try:
        f = mysociety.mapit.get_location(pc)
    except RABXException, e:
        context['error'] = e.text
        return page.render_to_response('index.html', context)

    #(station, station_long, station_id) = isoweb.nearest_station(E, N)
    #if not station:
    #    return page.render_to_response('index.html', { 'error': 'Could not find a station or bus stop :(' })

    if f['coordsyst'] == 'I':
        context['error'] = u'I\u2019m afraid we don\u2019t have information for Northern Ireland.'
        return page.render_to_response('index.html', context)

    # Canonicalise it, and redirect to that URL
    pc = page.sanitise_postcode(pc)

    return HttpResponseRedirect('/postcode/%s' % (pc))


def map_complete(map_object, invite):
    # Check there is a route file
    filename = os.path.join(tmpwork, '%s.iso' % str(map_object.id))
    if not os.path.exists(filename):
        return page.render_to_response('map-noiso.html', { 'map_id' : map_object.id })
    # Let's show the map
    if map_object.target_direction == 'arrive_by':
        initial_minutes = abs(map_object.target_time - map_object.target_limit_time) - 60
    else:
        initial_minutes = 60
    return page.render_to_response('map.html', {
        'map': map_object,
        'tile_web_host' : mysociety.config.get('TILE_WEB_HOST'),
        'show_max_minutes': abs(map_object.target_time - map_object.target_limit_time),
        'initial_minutes': initial_minutes,
        'invite': invite,
        'show_dropdown': len(invite.postcodes) > 3,
    })

def map(fs, invite):
    # Look up state of map etc.
    map_object = Map(fs)

    # If it is complete, then render it
    if map_object.current_state == 'complete':
        return map_complete(map_object, invite)

    # See how long it will take to make it
    map_progress = storage.get_map_queue_state(map_object.id)

    generation_time = storage.get_average_generation_time(
        target_direction=map_object.target_direction,
        target_time=map_object.target_time,
        target_limit_time=map_object.target_limit_time,
        target_date=map_object.target_date,
        )

    approx_waiting_time = map_progress['to_make'] * generation_time / float(max(map_progress['working'], 1))

    # ... if too long, ask for email
    if map_object.current_state in ('new', 'working') and approx_waiting_time > 60:
        context = {
            'title': map_object.title(),
            'state': map_progress,
            'approx_waiting_time': int(approx_waiting_time),
            }

        context.update(map_object.get_url_params())

        return page.render_to_response('map-provideemail.html', context)

    # If map isn't being made , set it going
    if not map_object.id:
        try:
            map_object.start_generation()
        except storage.AlreadyQueuedError:
            # Looks like someone else has put this kind of map in the queue
            # let's call map again from scratch.
            return map(fs, invite)

    if map_object.current_state == 'working':
        server, server_port = map_object.working_server.split(':')
        return page.render_to_response('map-working.html', {
            'title': map_object.title(),
            'approx_waiting_time': round(generation_time),
            'state' : map_progress,
            'server': server,
            'server_port': server_port,
            'refresh': int(generation_time)<5 and int(generation_time) or 5,
        })

    if map_object.current_state == 'error':
        return page.render_to_response('map-error.html', { 'map_id' : map_object.id })
    
    if map_object.current_state == 'new':
        return page.render_to_response('map-pleasewait.html', {
            'title': map_object.title(),
            'approx_waiting_time': int(approx_waiting_time),
            'state' : map_progress,
            'refresh': 2,
        })

    raise Exception("unknown state " + map_object.current_state)

# Email has been given, remember to mail them when map is ready
def log_email(fs, email):
    if not page.validate_email(email):
        return page.render_to_response('map-provideemail-error.html', {
            'target_postcode': fs['target_postcode'],
            'email': email,
        })
    # Okay, we have an email, set off the process
    map_object = Map(fs)

    if not map_object.id:
        try:
            map_object.start_generation()
        except storage.AlreadyQueuedError:
            map_object = Map(fs) # Fetch it again

    db().execute('BEGIN')
    db().execute('INSERT INTO email_queue (email, map_id) VALUES (%s, %s)', (email, map_object.id))
    db().execute('COMMIT')

    return page.render_to_response('map-provideemail-thanks.html')

# Used when in Flash you click on somewhere to get the route
#
# Duncan: I don't see how this can currently work, given two
# functions in isoweb (look_up_time_taken and look_up_route_node)
# that it depends on rely on struct without importing it.
# def get_route(fs, lat, lon):
#     E, N = geoconvert.wgs84_to_national_grid(lat, lon)
#     (station, station_long, station_id) = storage.get_nearest_station(E, N)

#     # Look up time taken
#     map = Map(fs)
#     tim = isoweb.look_up_time_taken(map.id, station_id)

#     # Look up route...
#     location_id = station_id
#     route = []
#     c = 0 
#     while True:
#         (next_location_id, next_journey_id) = isoweb.look_up_route_node(map.id, location_id)
#         leaving_time = isoweb.look_up_time_taken(map.id, location_id)

#         c = c + 1 
#         if c > 100:
#             raise Exception("route displayer probably in infinite loop")

#         route.append((location_id, next_location_id, next_journey_id))
#         if next_journey_id == isoweb.JOURNEY_NULL:
#             break
#         if next_journey_id == isoweb.JOURNEY_ALREADY_THERE:
#             break

#         location_id = next_location_id
#     # ... get station names from database
#     ids = ','.join([ str(int(route_node[0])) for route_node in route ]) + "," + str(station_id)
#     db().execute('''SELECT text_id, long_description, id FROM station WHERE id in (%s)''' % ids)
#     name_by_id = {}
#     for row in db().fetchall():
#         name_by_id[row['id']] = row['long_description'] + " (" + row['text_id'] + ")"
#     name_by_id[isoweb.LOCATION_TARGET] = 'TARGET'
#     # ... get journey info from database
#     ids = ','.join([ str(int(route_node[2])) for route_node in route ])
#     db().execute('''SELECT text_id, vehicle_code, id FROM journey WHERE id in (%s)''' % ids)
#     journey_by_id = {}
#     vehicle_code_by_id = {}
#     for row in db().fetchall():
#         journey_by_id[row['id']] = row['text_id']
#         vehicle_code_by_id[row['id']] = row['vehicle_code']
#     # ... and show it
#     route_str = "From " + str(name_by_id[station_id]) + " \n"
#     for location_id, next_location_id, journey_id in route:
#         location_time = isoweb.look_up_time_taken(map.id, location_id)
#         if map.target_direction == 'arrive_by':
#             leaving_after_midnight = map.target_time - location_time
#         elif map.target_direction == 'depart_after':
#             leaving_after_midnight = map.target_time - location_time
#         else:
#             assert(False)
#         route_str += isoweb.format_time(leaving_after_midnight) + " "
#         if journey_id > 0: 
#             next_location_name = name_by_id[next_location_id]
#             vehicle_code = vehicle_code_by_id[journey_id]
#             route_str += isoweb.pretty_vehicle_code(vehicle_code) + " (" + journey_by_id[journey_id] + ") to " + next_location_name
#         elif journey_id == isoweb.JOURNEY_WALK:
#             next_location_name = name_by_id[next_location_id]
#             route_str += "Walk to " + next_location_name;
#         elif journey_id == isoweb.JOURNEY_ALREADY_THERE:
#             location_name = name_by_id[location_id]
#             arrived = True
#             route_str += "You've arrived"
#         elif journey_id == isoweb.JOURNEY_NULL:
#             route_str += "No route found"
#         route_str += "\n";

#     return page.render_to_response('route.xml', {
#         'lat': lat, 'lon': lon,
#         'e': E, 'n': N,
#         'station' : station,
#         'station_long' : station_long,
#         'time_taken' : tim,
#         'route_str' : route_str
#     }, mimetype='text/xml')

def stats_view():
    state = storage.get_map_queue_state()
    current_connections = page.current_proxy_connections()
    return page.render_to_response(
        'map-stats.html', 
        {
            'state': state,
            'current_connections' : current_connections, 
            'max_connections' : page.max_connections,
            }
        )

def check_invite(invite):
    # Currently this chucks the user out to signup if they
    # don't have an invite. Later we'll want to modify this
    # to create an invite on the fly.
    if not invite.id:
        return HttpResponseRedirect('/signup')


#####################################################################
# Main FastCGI loop

def main(fs, cookies=None):
    if 'stats' in fs:
        return stats_view()

    invite = page.Invite(cookies.get('token').value if cookies else None)

    # Everything below currently needs an invite.
    # This will redirect if invite is missing.
    check_invite(invite)

    #got_map_spec = ('station_id' in fs or 'target_e' in fs or 'target_postcode' in fs)
    got_map_spec = ('target_postcode' in fs)

# Duncan - not currently in use.
#    if 'lat' in fs: # Flash request for route
#        return get_route(fs, float(fs['lat']), float(fs['lon']))

    if 'pc' in fs: # Front page submission
        return check_postcode(fs['pc'], invite)

    if got_map_spec and 'email' in fs: # Overloaded email request
        return log_email(fs, fs['email'])

    if got_map_spec: # Page for generating/ displaying map
        postcode = page.sanitise_postcode(fs['target_postcode'])
        postcodes = invite.postcodes
        if (postcode, utils.canonicalise_postcode(postcode)) not in postcodes:
            if invite.maps_left <= 0:
                return page.render_to_response('beta-limit.html', { 'postcodes': postcodes })
            invite.add_postcode(postcode)

        # If the load is too high on the server, don't allow new map
        current_connections = page.current_proxy_connections()
        if current_connections >= page.max_connections:
            context = {
                'current_connections': current_connections, 
                'max_connections': page.max_connections
                }

            return page.render_to_response('map-http-overload.html', context)

        return map(fs, invite)

    # Front page display
    return page.render_to_response('index.html', {
        'invite': invite,
        'most_recent': storage.get_latest_postcodes(limit=10),
        'show_dropdown': len(invite.postcodes) > 3
    })

# Main FastCGI loop
if __name__ == "__main__":
    page.wsgi_loop(main)


