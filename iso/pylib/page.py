#!/usr/bin/env python2.5
#
# page.py:
# Various shared functions
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: page.py,v 1.13 2009-05-13 17:44:40 matthew Exp $
#

import os, re, cgi, fcgi, cgitb, sys
import Cookie
import random

cgitb.enable()

from django.conf import settings
settings.configure( TEMPLATE_DIRS=(sys.path[0] + '/../templates/',), TEMPLATE_DEBUG=True)
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect

from sendemail import send_email
import mysociety.config

def render_to_response(template, vars={}, mimetype=None):
    vars.update({
        'self': os.environ.get('REQUEST_URI', ''),
    })
    return HttpResponse(render_to_string(template, vars), mimetype=mimetype)

def fcgi_loop(main):
    req = fcgi.Accept()
    fs = req.getFieldStorage()
    response = main(fs)
    if isinstance(response, HttpResponseRedirect):
        req.out.write("Status: 302 Found\r\n")
    if req.env.get('REQUEST_METHOD') == 'HEAD':
        req.out.write('\r\n'.join(['%s: %s' % (key, value) for key, value in response._headers.values()]) + '\r\n\r\n')
    else:
        req.out.write(str(response))
    req.Finish()

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
# Cookie invite handling stuff

INVITE_NUM_MAPS = 3

class Invite(object):
    id = 0
    num_invites = 0
    _postcodes = []

    def __init__(self, db):
        cookie_str = ''
        if 'HTTP_COOKIE' in os.environ:
            cookie_str = os.environ['HTTP_COOKIE']
        cookies = Cookie.BaseCookie(cookie_str)
        if not 'token' in cookies:
            return
        self.db = db
        self.token = cookies['token']
        self.check()

    def __str__(self):
        return self.token

    def check(self):
        self.db.execute('SELECT * FROM invite WHERE token=%s', (self.token.value,))
        row = self.db.fetchone()
        if not row: return
        self.__dict__.update(row)

    @property
    def postcodes(self):
        if not self._postcodes:
            self.db.execute('SELECT postcode FROM invite_postcode WHERE invite_id=%s', (self.id, ))
            self._postcodes = [ row['postcode'] for row in self.db.fetchall() ]
        return self._postcodes

    @property
    def maps_left(self):
        return INVITE_NUM_MAPS - len(self.postcodes)

    def add_postcode(self, pc):
        self.db.execute('''INSERT INTO invite_postcode (invite_id, postcode) VALUES (%s, '%s')''' % (self.id, pc))
        self.db.execute('COMMIT')
        self._postcodes.append(pc)

# Random token generation

def random_token():
    chars = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789'
    token = ''
    for k in range(17):
        token += random.choice(chars)
    return token


