#!/usr/bin/env python2.4
#
# index.cgi:
# Main code
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: index.cgi,v 1.25 2009-03-26 12:06:15 matthew Exp $
#

import sha
import re
import sys
import os.path
sys.path.append("../../pylib")
import fcgi, cgi
from pyPgSQL import PgSQL

import mysociety.config
import mysociety.mapit
mysociety.config.set_file("../conf/general")
from mysociety.rabx import RABXException

db = PgSQL.connect(mysociety.config.get('COL_DB_HOST') + ':' + mysociety.config.get('COL_DB_PORT') + ':' + mysociety.config.get('COL_DB_NAME') + ':' + mysociety.config.get('COL_DB_USER') + ':' + mysociety.config.get('COL_DB_PASS'))

class Response(object):
    def __init__(self, template='', vars={}, status=200, url='', refresh=False, id=''):
        self.template = template
        self.vars = vars
	self.status = status
	self.url = url
	self.refresh = refresh
	self.id = id

    def __str__(self):
        if self.status == 302:
            return "Please visit <a href='%s'>%s</a>." % (self.url, self.url)
	return template(self.template, self.vars)

    def headers(self):
        if self.status == 302:
	    return "Location: %s\r\n" % self.url
	return ''

def lookup(pc):
    """Given a postcode, look up the nearest station ID
    and redirect to a URL containing that"""

    try:
        f = mysociety.mapit.get_location(pc)
    except RABXException, e:
        return Response('index', {
            'error': e
        })

    E = int(f['easting'])
    N = int(f['northing'])
    lat = f['wgs84_lat']
    lon = f['wgs84_lon']

    q = db.cursor()
    q.execute('''SELECT text_id FROM station WHERE
        position_osgb && Expand('POINT(%d %d)'::geometry, 50000)
	AND Distance(position_osgb, 'POINT(%d %d)') < 50000''' % (E, N, E, N))
    row = q.fetchone()
    if not row:
        return Response('index', {
            'error': 'Could not find a station or bus stop :('
        })

    return Response(status=302, url='/station/%s' % row['text_id'])

def map(id):
    global page_vars

    tmpwork = mysociety.config.get('TMPWORK')
    file = os.path.join(tmpwork, id)
    if os.path.exists(file + ".iso"):
        # We've got a generated file, let's show the map!
        return Response('map', {
            'centre_lat': lat,
            'centre_lon': lon,
            'tile_id': id + ".txt"
        }, id='map')

    # Call out to tile generation
    binarycache = os.path.join(tmpwork, "fastindex-oxford-2008-10-07")
    cmd = "../bin/fastplan %s %s 540 coordinate 0 %d %d" % (binarycache, file, E, N)
    ret = os.system(cmd)
    if ret != 0:
        raise Exception("index.cgi: Error code from command: " + cmd)

    return Response('map-pleasewait', {
        'postcode': pc
    }, refresh=True)
    
def main(fs):
    if 'pc' in fs:
        return lookup(fs.getfirst('pc'))
    elif 'id' in fs:
        return map(fs.getfirst('id'))
    return Response('index')

# Functions

def template(name, vars={}):
    template = slurp_file('../templates/%s.html' % name)
    template = re.sub('{{ ([a-z_]*) }}', lambda x: cgi.escape(str(vars.get(x.group(1), '')), True), template)
    template = re.sub('{{ ([a-z_]*)\|safe }}', lambda x: str(vars.get(x.group(1), '')), template)
    return template

def slurp_file(filename):
    f = file(filename, 'rb')
    content = f.read()
    f.close()
    return content

def redirect(url):
    print "Location: %s\r\n\r\n" % url
    print "Please visit <a href='%s'>%s</a>." % (url, url)

# Main FastCGI loop
while fcgi.isFCGI():
    req = fcgi.Accept()
    fs = req.getFieldStorage()

    try:
        response = main(fs)
	req.out.write(response.headers())

        req.out.write("Content-Type: text/html; charset=utf-8\r\n\r\n")
        if req.env.get('REQUEST_METHOD') == 'HEAD':
            req.Finish()
            continue

        footer = template('footer')
        header = template('header', {
            'postcode': fs.getfirst('pc', ''),
            'refresh': response.refresh and '<meta http-equiv="refresh" content="5">' or '',
            'body_id': response.id and ' id="%s"' % response.id or '',
        })
        req.out.write(header + str(response) + footer)

    except Exception, e:
        req.out.write("Content-Type: text/plain\r\n\r\n")
        req.out.write("Sorry, we've had some sort of problem.\n\n")
        req.out.write(str(e) + "\n")

    req.Finish()

