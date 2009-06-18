#
# common.py: Common functions for mySociety site statistics
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: louise@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: common.py,v 1.3 2009-06-18 09:14:11 louise Exp $
#

from datetime import date, timedelta
from django.core.mail import EmailMessage 
import mysociety
    
def end_of_current_week():
    return date.today() - timedelta(days=1)
    
def start_of_week(end_of_week):
    if (end_of_week == None):
        end_of_week = end_of_current_week()
    return end_of_week - timedelta(days=6)
    
def end_of_previous_week(date=None):
    if (date == None):
        date = end_of_current_week()
    return date - timedelta(days=7)

def percent_change(current, previous):
    if previous == 0:
        return 'n/a'
    percent_change = (float(current * 100) / float(previous)) - 100
    formatted_percent = "%d%%" % round(percent_change, 0)
    if formatted_percent[0] != '-':
        formatted_percent =  "+%s" % (formatted_percent)
    return formatted_percent

def send_newsletter(newsletter, date, sources, options):
    if options.verbose:
        if options.only:
            print "Only sending mail to %s" % (options.only)
        print "Getting data for %s newsletter" % (newsletter)
    for subscription in newsletter.subscription_set.all():
        format = subscription.user.profile.get_email_format_display()
        content = newsletter.render(format, sources, date)
    
        if not options.only or subscription.user.username == options.only:
            if options.verbose:
                print "Sending %s format %s newsletter to %s" % (format, newsletter, subscription.user.email)
            msg = EmailMessage("%s for %s" % (newsletter.subject, date.strftime("%d/%m/%y")), content, mysociety.config.get('MAIL_FROM'), [subscription.user.email])
            if format == 'html':
                msg.content_subtype = "html"  
            msg.send()
    