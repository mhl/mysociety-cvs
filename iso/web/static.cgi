#!/usr/bin/env python2.5
#
# static.cgi:
# For FAQ only at present, but other static pages sure to be along
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: static.cgi,v 1.5 2009-05-06 19:30:21 matthew Exp $
#

import sys
sys.path.extend(("../pylib", "../../pylib"))
import fcgi
from page import *

def main(fs):
    page = fs.getfirst('page')
    if page == 'faq':
        return Response('faq', { 'title': 'Help' })
    return Response(status=302, url='/')

# Main FastCGI loop
while fcgi.isFCGI():
    fcgi_loop(main)

