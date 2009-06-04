#!/usr/bin/env python2.5
#
# static.cgi:
# For FAQ only at present, but other static pages sure to be along
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: static.cgi,v 1.9 2009-06-04 14:44:34 francis Exp $
#

import sys
sys.path.extend(("../pylib", "../../pylib"))

import mysociety.config
mysociety.config.set_file("../conf/general")

from page import *
from django.http import HttpResponseRedirect

def main(fs):
    page = fs.get('page')
    if page == 'faq':
        return render_to_response('faq.html')
    return HttpResponseRedirect('/')

# Main FastCGI loop
if __name__ == "__main__":
    wsgi_loop(main)


