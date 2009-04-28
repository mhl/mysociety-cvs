#!/usr/bin/env python2.5
#
# proxy.cgi:
# No crossdomain.xml files present.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: proxy.cgi,v 1.6 2009-04-28 14:42:31 matthew Exp $
#

import sys, os.path, os, re, urllib
sys.path.extend(("../pylib", "../../pylib"))
import fcgi
from page import *

def main(fs):
    dir = '/tmp/tilecache-cloudmade'
    url = fs.getfirst('u', '')
    m = re.match('http://.\.tile\.cloudmade\.com/[^/]*/[^/]*/[^/]*/[^/]*/[^/]*/[^/]*\.png$', url)
    if not url or not m:
        return Response(status=302, url='/')
    zoom, x, y = url.split('/')[-3:]
    cache_dir = os.path.join(dir, zoom, x)
    cache_path = os.path.join(cache_dir, y)
    if os.path.exists(cache_path):
        image = slurp_file(cache_path)
    else:
        fp = urllib.urlopen(url)
        image = fp.read()
        fp.close()
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

