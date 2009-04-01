#!/usr/bin/env python2.5
#
# index.cgi:
# Main code
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: static.cgi,v 1.1 2009-04-01 10:38:27 matthew Exp $
#

import re
import sys
import os.path
import traceback
sys.path.extend(("../pylib", "../../pylib", "/home/matthew/lib/python"))
import fcgi
import psycopg2 as postgres
import pyproj

from page import *
import mysociety.config
import mysociety.mapit
mysociety.config.set_file("../conf/general")
from mysociety.rabx import RABXException

def main(fs):
    if 'page' in fs and fs['page'] == 'faq':
	return Response('faq')
    return Response(status=302, url='/')

# Main FastCGI loop
while fcgi.isFCGI():
    fcgi_loop(main)

