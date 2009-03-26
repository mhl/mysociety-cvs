#!/usr/bin/env python2.4
#
# index.cgi:
# Main code
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: index.cgi,v 1.33 2009-03-26 15:49:00 matthew Exp $
#

import sha
import re
import sys
import os.path
import traceback
sys.path.append("../../pylib")
sys.path.append("/home/matthew/lib/python")
import fcgi, cgi
import psycopg2 as postgres
import pyproj

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
            return "Status: 302 Found\r\nLocation: %s\r\n" % self.url
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

    db.execute('''SELECT text_id FROM station WHERE
        position_osgb && Expand(GeomFromText('POINT(%d %d)', 27700), 50000)
        AND Distance(position_osgb, GeomFromText('POINT(%d %d)', 27700)) < 50000
        ORDER BY Distance(position_osgb, GeomFromText('POINT(%d %d)', 27700))
        LIMIT 1''' % (E, N, E, N, E, N))
    row = db.fetchone()
    if not row:
        return Response('index', {
            'error': 'Could not find a station or bus stop :('
        })

    return Response(status=302, url='/station/%s' % row[0])

def map(text_id):
    db.execute('BEGIN')
    db.execute('''SELECT id, X(position_osgb), Y(position_osgb) FROM station
        WHERE text_id = %s FOR UPDATE''', (text_id,))
    row = db.fetchone()
    target_station_id, lat, lon = row

    # XXX These data are all fixed for now
    target_latest = 540
    target_earliest = 0
    target_date = '2008-10-07'

    db.execute('''SELECT id FROM map WHERE target_station_id = %s
        AND target_latest = %s AND target_earliest = %s AND target_date = %s''', (target_station_id, target_latest, target_earliest, target_date))
    map = db.fetchone()
    if map is None:
        # Start off generation of map!
        db.execute("SELECT nextval('map_id_seq')")
        map_id = db.fetchone()[0]
        db.execute('INSERT INTO map (id, state, target_station_id, target_latest, target_earliest, target_date) VALUES (%s, %s, %s, %s, %s, %s)', (map_id, 'new', target_station_id, target_latest, target_earliest, target_date))
        db.execute('COMMIT')
    else:
        map_id = map[0]
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

    # Please wait...
    return Response('map-pleasewait', {
    }, refresh=True)
    
def main(fs):
    if 'pc' in fs:
        return lookup(fs.getfirst('pc'))
    elif 'station_id' in fs:
        return map(fs.getfirst('station_id'))
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

BNG = pyproj.Proj(proj='tmerc', lat_0=49, lon_0=-2, k=0.999601, x_0=400000, y_0=-100000, ellps='airy', towgs84='446.448,-125.157,542.060,0.1502,0.2470,0.8421,-20.4894', units='m', no_defs=True)
WGS = pyproj.Proj(proj='latlong', towsg84="0,0,0", ellps="WGS84", no_defs=True)

def national_grid_to_wgs84(x, y):
    """Project from British National Grid to WGS-84 lat/lon"""
    return pyproj.transform(BNG, WGS, x, y)

# Main FastCGI loop
while fcgi.isFCGI():
    req = fcgi.Accept()
    fs = req.getFieldStorage()

    try:
        response = main(fs)
        if response.headers():
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
        traceback.print_exc()

    db.execute('ROLLBACK')
    req.Finish()

