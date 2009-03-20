#!/usr/bin/env python2.4
#
# index.cgi:
# Main code
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: index.cgi,v 1.5 2009-03-20 15:28:32 matthew Exp $
#

import re
import sys
sys.path.append("../../pylib")
import fcgi, cgi

import mysociety.config
import mysociety.mapit
mysociety.config.set_file("../conf/general")

def lookup(pc):
    f = mysociety.mapit.get_location(pc)
    E = int(f['easting'])
    N = int(f['northing'])

    out = '<p>You entered %s, %dE %dN.</p>' % (cgi.escape(pc, True), E, N)

    return out
    
def test():
    lat = '51.759865102943905'
    lon = '-1.2658309936523438'
    tile_id = 'foo'
    return template('map', {
        'centre_lat': lat,
        'centre_lon': lon,
        'tile_id': tile_id
    })

def front_page():
    front = slurp_file('../templates/index.html')
    return front

def main(fs):
    if 'pc' in fs:
        return lookup(fs.getfirst('pc'))
    if 'map' in fs:
        return test()
    return front_page()

# Functions

def template(name, vars):
    template = slurp_file('../templates/%s.html' % name)
    template = re.sub('{{ ([a-z_]*) }}', lambda x: vars.get(x.group(1)), template)
    return template

def slurp_file(filename):
    f = file(filename, 'rb')
    content = f.read()
    f.close()
    return content

# Main FastCGI loop
while fcgi.isFCGI():
    req = fcgi.Accept()
    fs = req.getFieldStorage()

    try:
        req.out.write("Content-Type: text/html; charset=utf-8\r\n\r\n")
        if req.env.get('REQUEST_METHOD') == 'HEAD':
            req.Finish()
            continue

        header = slurp_file('../templates/header.html')
        footer = slurp_file('../templates/footer.html')
        content = main(fs)
        req.out.write(header + content + footer)

    except Exception, e:
        req.out.write("Content-Type: text/plain\r\n\r\n")
        req.out.write("Sorry, we've had some sort of problem.\n\n")
        req.out.write(str(e) + "\n")

    req.Finish()

