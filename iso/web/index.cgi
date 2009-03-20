#!/usr/bin/env python2.4
#
# index.cgi:
# Main code
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: index.cgi,v 1.4 2009-03-20 14:31:54 francis Exp $
#

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
    
def front_page():
    front = slurp_file('../templates/index.html')
    return front

def main(fs):
    if 'pc' in fs:
        return lookup(fs.getfirst('pc'))
    return front_page()

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

