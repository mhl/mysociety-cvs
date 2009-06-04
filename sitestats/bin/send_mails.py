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
from datetime import date
sys.path.append("../pylib")
import sitestats
os.environ['DJANGO_SETTINGS_MODULE'] = 'sitestats.settings'
from django.db import models
from django.contrib.auth.models import User
from django.core.mail import EmailMessage 
from sitestats.newsletters.models import CommonBaseMeasuresNewsletter, Newsletter, Subscription
from sitestats.newsletters.sources import piwik
from sitestats.newsletters.sources import google
###############################################################################
# Read parameters

parser = optparse.OptionParser()

parser.set_usage('''
./send_mails.py [OPTIONS]

Send out mySociety site stats emails. Run with "--help" to see available options.

''')

parser.add_option('--verbose', action='store_true', default=False, dest="verbose", help='Produce extra debugging output')
(options, args) = parser.parse_args()

print options.verbose

sources = {'piwik' : piwik.Piwik(), 'google' : google.Google()}


for newsletter in CommonBaseMeasuresNewsletter.objects.all():
    print newsletter.name
    for subscription in newsletter.subscription_set.all():
        print subscription.user.email
        content = newsletter.render('html', sources, date=date(2009, 1, 11))
        msg = EmailMessage('hi', content, 'test@localhost', [subscription.user.email])
        msg.content_subtype = "html"  
        msg.send()