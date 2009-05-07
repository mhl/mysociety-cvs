#!/usr/bin/env python2.5
#
# proxy.cgi:
# No crossdomain.xml files present.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: proxy.cgi,v 1.11 2009-05-07 18:51:00 matthew Exp $
#

import sys, os.path, os, re, urllib
sys.path.extend(("../pylib", "../../pylib"))
import fcgi
from page import *

import mysociety.config
mysociety.config.set_file("../conf/general")

def main(fs):
    dir = mysociety.config.get('CLOUDMADE_PROXY_CACHE_DIR', '/colwork/cloudmade-tiles')
    url = fs.getfirst('u', '')
    if url:
        m = re.match('http://(.\.)?tile\.cloudmade\.com/[^/]*/[^/]*/[^/]*/[^/]*/[^/]*/[^/]*\.png$', url)
        if not m:
            return Response(status=302, url='/')
        zoom, x, y = url.split('/')[-3:]
    else:
        zoom = fs.getfirst('z', 0)
        x = fs.getfirst('x', 0)
        y = fs.getfirst('y', 0)
        url = 'http://tile.cloudmade.com/f42ed2bf2ce15484a17cef7fe5e6df0f/997/256/%s/%s/%s.png' % (zoom, x, y)
    if not zoom or not x or not y:
        return Response(status=302, url='/')
    cache_dir = os.path.join(dir, zoom, x)
    cache_path = os.path.join(cache_dir, y)
    if os.path.exists(cache_path):
        image = slurp_file(cache_path)
    else:
        fp = urllib.urlopen(url)
        image = fp.read()
        fp.close()
        if len(image) != 53: # Not found XXX
            if not os.path.exists(os.path.join(dir, zoom)):
                os.mkdir(os.path.join(dir, zoom))
            if not os.path.exists(os.path.join(dir, zoom, x)):
                os.mkdir(os.path.join(dir, zoom, x))
            fp = open(cache_path, 'w') 
            fp.write(image)
            fp.close()
    response = ImageResponse(image=image)
    return response

# Main FastCGI loop
while fcgi.isFCGI():
    fcgi_loop(main)

