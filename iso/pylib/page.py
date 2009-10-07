#!/usr/bin/env python2.5
#
# page.py:
# Various shared functions for web page display.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: page.py,v 1.31 2009-10-07 21:34:54 duncan Exp $
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

            response = main(fs)

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

def send_template_email(to, template, vars):
    message = render_to_string(template, vars)
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
    id = 0
    num_invites = 0
    _postcodes = []

    def __init__(self):
        cookie_str = ''
        if 'HTTP_COOKIE' in os.environ:
            cookie_str = os.environ['HTTP_COOKIE']
        cookies = Cookie.BaseCookie(cookie_str)
        if not 'token' in cookies:
            return
        self.token = cookies['token']
        self.check()

    def __str__(self):
        return self.token

    def check(self):
        token_row = storage.get_invite_by_token(self.token.value)
        
        if token_row:
            self.__dict__.update(token_row)

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


