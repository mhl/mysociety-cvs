#!/usr/bin/env python2.5
#
# static.cgi:
# For FAQ only at present, but other static pages sure to be along
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: static.cgi,v 1.3 2009-04-01 14:12:46 matthew Exp $
#

import sys, fcgi
sys.path.extend(("../pylib"))
from page import *

def main(fs):
    page = fs.getfirst('page')
    if page == 'faq':
        return Response('faq')
    return Response(status=302, url='/')

# Main FastCGI loop
while fcgi.isFCGI():
    fcgi_loop(main)

