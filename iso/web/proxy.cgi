#!/usr/bin/env python2.5
#
# proxy.cgi:
# No crossdomain.xml files present.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: proxy.cgi,v 1.13 2009-05-13 13:31:18 matthew Exp $
#

import sys, os.path, os, re, urllib
sys.path.extend(("../pylib", "../../pylib"))
import fcgi
from page import fcgi_loop
from django.http import HttpResponse, HttpResponseRedirect

import mysociety.config
mysociety.config.set_file("../conf/general")

def main(fs):
    dir = mysociety.config.get('CLOUDMADE_PROXY_CACHE_DIR', '/colwork/cloudmade-tiles')
    url = fs.getfirst('u', '')
    if url:
        m = re.match('http://(?:.\.)?tile\.cloudmade\.com/[^/]*/[^/]*/[^/]*/([^/]*)/([^/]*)/([^/]*)\.png$', url)
        if not m:
            return HttpResponseRedirect('/')
        zoom, x, y = m.groups()
    else:
        zoom = fs.getfirst('z', 0)
        x = fs.getfirst('x', 0)
        y = fs.getfirst('y', 0)
    if not zoom or not x or not y:
        return HttpResponseRedirect('/')
    cache_dir = os.path.join(dir, zoom, x)
    cache_path = os.path.join(cache_dir, y)
    if os.path.exists(cache_path):
        image = slurp_file(cache_path)
    else:
        url = 'http://tile.cloudmade.com/f42ed2bf2ce15484a17cef7fe5e6df0f/997/256/%s/%s/%s.png' % (zoom, x, y)
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
    return HttpResponse(image, mimetype='image/png')

# Main FastCGI loop
while fcgi.isFCGI():
    fcgi_loop(main)

