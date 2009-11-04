#!/usr/bin/python2.5
#
# send_mails.py: Send out the mySociety site stats emails
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: louise@mysociety.org; WWW: http://www.mysociety.org/
#

import optparse
import sys
import os
from datetime import date, timedelta
filename = __file__
file_dir = os.path.abspath(os.path.dirname(filename))
sys.path.append(file_dir + "/../pylib")
import sitestats
os.environ['DJANGO_SETTINGS_MODULE'] = 'sitestats.settings'
from django.db import models
from django.contrib.auth.models import User
from sitestats.newsletters.models import *
from sitestats.newsletters.sources import *
from sitestats.newsletters.common import send_newsletters

###############################################################################
# Read parameters

parser = optparse.OptionParser()

parser.set_usage('''
./send_mails.py [OPTIONS]

Send out mySociety site stats emails. Run with "--help" to see available options.

''')

parser.add_option('--verbose', action='store_true', default=False, dest="verbose", help='Produce extra debugging output')
parser.add_option('--only', dest='only', default=None, help='Only send email for one user identified by username')
parser.add_option('--newsletter', dest='newsletter', default=None, help='Only send one type of newsletter e.g. TWFYNewsletter, CommonBaseMeasuresNewsletter')
(options, args) = parser.parse_args()

sources = { 'piwik'    : Piwik(), 
            'google'   : Google(), 
            'twfy_api' : TWFYApi(),
            'fms_api'  : FMSApi() }

date = date.today()

# get nearest past Sunday 
while date.weekday() != 6:
    date = date - timedelta(days=1)

newsletter_types = [CommonBaseMeasuresNewsletter, 
                    TWFYNewsletter, 
                    FMSNewsletter, 
                    HFYMPNewsletter,
                    WTTNewsletter,
                    PBNewsletter, 
                    WDTKNewsletter]                 
                         
if options.newsletter:
    newsletter_types = [newsletter for newsletter in newsletter_types if newsletter.__name__ == options.newsletter]   

send_newsletters(newsletter_types, date, sources, options)

