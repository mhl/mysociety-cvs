#!/usr/bin/env python2.5
#
# page.py:
# Various shared functions for web page display.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: page.py,v 1.43 2009-10-20 15:49:18 duncan Exp $
#

import os, re, cgitb, sys
import Cookie
import random
import urllib2
import flup.server.fcgi_fork

cgitb.enable()

from django.conf import settings
settings.configure( TEMPLATE_DIRS=(sys.path[0] + '/../templates/',), TEMPLATE_DEBUG=True)
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect

from paste.request import parse_formvars

from sendemail import send_email
import mysociety.config
from coldb import db

import storage
import utils
import isoweb
import geoconvert

def render_to_response(
    template, 
    context=None, 
    mimetype=None, 
    cache_max_age=None
    ):

    if context is None:
        context = {}

    context.update({
        'self': os.environ.get('REQUEST_URI', ''),
    })
    response = HttpResponse(render_to_string(template, context), mimetype=mimetype)

    if cache_max_age:
        response['Cache-Control'] = 'max-age: ' + str(cache_max_age)

    return response

def wsgi_loop(main):
    def wsgiApp(environ, start_response):
        try:
            fs = parse_formvars(environ)

            fcgi_env = environ.copy()
            for k in os.environ.keys():
                del os.environ[k]
            for k, v in fcgi_env.items():
                if re.match('paste.', k) or re.match('wsgi.', k):
                    continue
                os.environ[k] = v

            cookies = Cookie.BaseCookie(os.environ.get('HTTP_COOKIE', ''))
            response = main(fs, cookies=cookies)

            status = "200 OK"
            if isinstance(response, HttpResponseRedirect):
                status = "302 Found"

            items = response.items()
            if response.cookies:
                cookie_header = str(response.cookies)
                (cookie_key, cookie_value) = cookie_header.split(": ")
                items.append((cookie_key, cookie_value))
            start_response(status, items)

            if os.environ['REQUEST_METHOD'] == 'HEAD':
                return('\r\n'.join(['%s: %s' % (k, v) for k, v in response.items()]) + '\r\n\r\n')
            else:
                return response.content
        finally:
            db().execute('ROLLBACK')


    flup.server.fcgi_fork.WSGIServer(wsgiApp).run()

def slurp_file(filename):
    f = file(filename, 'rb')
    content = f.read()
    f.close()
    return content

# Email functions

def validate_email(address):
    if re.match('([^()<>@,;:\\".\[\] \000-\037\177\200-\377]+(\s*\.\s*[^()<>@,;:\\".\[\] \000-\037\177\200-\377]+)*|"([^"\\\r\n\200-\377]|\.)*")\s*@\s*[A-Za-z0-9][A-Za-z0-9-]*(\s*\.\s*[A-Za-z0-9][A-Za-z0-9-]*)*$', address):
        return True
    else:
        return False

def send_template_email(to, template, context):
    message = render_to_string(template, context)
    subject = 'Message from Mapumental'
    m = re.match('Subject: (.*)\n', message)
    if m:
        subject = m.group(1)
        message = re.sub(m.group(0), '', message)

    send_email(mysociety.config.get('CONTACT_EMAIL'), to, message, {
        'From': (mysociety.config.get('CONTACT_EMAIL'), 'Mapumental'),
        'To': to,
        'Subject': subject,
    })


def activate_invite(invite_id):
    token = random_token()
    storage.set_invite_token(invite_id, token)

    return token

def create_invite_with_token(email, source='manual'):
    token = random_token()

    storage.create_invite(email, source=source, token=token)

    return token


def email_invite(invite, debug=False):
    inviter_email = invite.get('inviter_email')
    template = 'email-invite.txt' if inviter_email else 'email-signup.txt'

    if debug:
        print "Sending invite to", invite['email'], "from", inviter_email, "using template", template,

    token = activate_invite(invite['id'])

    url = mysociety.config.get('BASE_URL') + 'T/' + token
    send_template_email(invite['email'], template, {
            'url': url,
            'pid': os.getpid(),
            'inviter_email': inviter_email,
            })

    if debug:
        print "done"

# Cookie invite handling stuff

class Invite(object):
    def __init__(self, token):
        # Used so that an invite which isn't in the database still has an id
        # attribute and no invites.
        defaults_dict = {'id': None, 'num_invites': 0}

        self._postcodes = []
        self.token = token

        self._token_row = (storage.get_invite_by_token(token) or defaults_dict) if token else defaults_dict

    def __getattr__(self, name):
        if name in self._token_row:
            return self._token_row[name]
        else:
            raise AttributeError('%s' %self._token_row)

    def __str__(self):
        return self.token

    @property
    def postcodes(self):
        if not self._postcodes:
            self._postcodes = storage.get_postcodes_by_invite(self.id)
        return self._postcodes

    @property
    def maps_left(self):
        return self.num_maps - len(self.postcodes)

    def add_postcode(self, pc):
        storage.add_postcode(self.id, pc)
        self._postcodes.append( (pc, utils.canonicalise_postcode(pc)) )

#####################################################################
# Class representing the parameters for a map, and its status

class Map(object):
    id = None
    working_server = None

    target_station_id = None
    target_postcode = None

    def __init__(self, 
                 easting, 
                 northing, 
                 target_direction=None, 
                 target_time=None,
                 target_limit_time=None,
                 ):
        self.target_e = easting
        self.target_n = northing

        # Used for centring map
        self.lat, self.lon = geoconvert.national_grid_to_wgs84(self.target_e, self.target_n)

        # Times, directions and date
        if target_direction:
            if target_direction in ['arrive_by', 'depart_after']:
                self.target_direction = target_direction
            else:
                raise Exception("Bad direction parameter specified, only arrive_by and depart_after supported")
        else:
            self.target_direction = isoweb.default_target_direction
            
        self.target_time = target_time or isoweb.default_target_time
        self.target_limit_time = target_limit_time or isoweb.default_target_limit_time(self.target_direction)

        # XXX date is fixed for now
        self.target_date = isoweb.default_target_date

        self.update_status()

    def update_status(self):
        status = storage.get_map_status(
            self.target_direction,
            self.target_time,
            self.target_limit_time,
            self.target_date,
            easting = self.target_e,
            northing = self.target_n,
            )

        if status:
            self.id, self.current_status, self.working_server = status
        else:
            self.current_status = 'new'

    # Construct own URL, ensure ends inside query parameters so can add more
    # (Flash just appends strings to this URL for e.g. route URL)
    def url_with_params(self):
        ret = self.url()
        if not '?' in ret:
            ret = ret + "?"
        else:
            ret = ret + "&"
        return ret

    def target_time_formatted(self):
        return isoweb.format_time(self.target_time)
    
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

    def title(self):
        # XXX Currently just location, needs to include arrival time etc.
        return '%d,%d' % (self.target_e, self.target_n)

    def get_base_url(self):
        return "/grid/" + str(self.target_e) + "/" + str(self.target_n)

    # Construct own URL
    def url(self):
        url = self.get_base_url()

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

    # Merges hashes for URL into dict and return
    def get_url_params(self):
        return {'target_e': self.target_e, 'target_n': self.target_n}

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
                                                                                       
class StationMap(Map):
    def __init__(self, station_id, **kwargs):
        self.text_id = sanitise_station_id(station_id)
        self.target_station_id, easting, northing = storage.get_station_coords(self.text_id)

        super(StationMap, self).__init__(int(easting), int(northing), **kwargs)

    def update_status(self):
        status = storage.get_map_status(
            self.target_direction,
            self.target_time,
            self.target_limit_time,
            self.target_date,
            station_id = self.target_station_id
            )

        if status:
            self.id, self.current_status, self.working_server = status
        else:
            self.current_status = 'new'

    def title(self):
        return self.text_id

    def get_base_url(self):
        return "/station/" + self.target_station_id
                                                                                       
    def get_url_params(self):
        return {'station_id': self.target_station_id}

class PostcodeMap(Map):
    def __init__(self, postcode, **kwargs):
        self.target_postcode = sanitise_postcode(postcode)
        f = mysociety.mapit.get_location(self.target_postcode)

        super(PostcodeMap, self).__init__(int(f['easting']), int(f['northing']), **kwargs)

    def title(self):
        return utils.canonicalise_postcode(self.target_postcode)

    def get_base_url(self):
        return "/postcode/" + self.target_postcode

    def get_url_params(self):
        return {'target_postcode': self.target_postcode}

def create_map_from_fs(fs):
    postcode = fs.get('target_postcode')
    if postcode:
        return PostcodeMap(postcode)
    
    station_id = fs.get('station_id')
    if station_id:
        return StationMap(station_id)

    easting = fs.get('target_e')
    northing = fs.get('target_n')

    if easting and northing:
        return Map(int(easting), int(northing))

    raise Exception("Insufficient info to find a map.")


# Random token generation
def random_token():
    chars = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789'
    token = ''
    for k in range(17):
        token += random.choice(chars)
    return token

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

# Read the haproxy statistics page to see if there are too many connections
haproxy_stats_url = mysociety.config.get('BASE_URL') + 'haproxy_stats'
max_connections = int(mysociety.config.get('MAX_HAPROXY_CONNECTIONS'))
def current_proxy_connections():
    try:
        stats = urllib2.urlopen(haproxy_stats_url).read()
    except urllib2.HTTPError, e:
        # on test sites etc. no haproxy
        if e.code == 404:
            return -1
        raise

    matches = re.search("current conns = ([0-9]+)", stats)
    current_connections = int(matches.groups()[0])

    return current_connections


