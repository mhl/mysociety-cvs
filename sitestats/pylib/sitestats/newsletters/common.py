#
# common.py: Common functions for mySociety site statistics
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: louise@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: common.py,v 1.5 2009-06-22 11:43:03 louise Exp $
#

from datetime import date, timedelta
from django.core.mail import EmailMessage 
import mysociety
    
def format_extension(format):
    extensions = {'html': 'html',
                  'text': 'txt'}
    return extensions[format]
    
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

def send_mail(subject, date, content, email_from, email_to, format):
    msg = EmailMessage("%s for %s" % (subject, date.strftime("%d/%m/%y")), content, email_from, [email_to])
    if format == 'html':
        msg.content_subtype = "html"  
    msg.send()
    
def msg(message, options):
    if options.verbose:
        print message
        
def mail_separator(format, text):
    if format == 'html':
        return "<h2>%s</h2>" % (text)
    else:
        return "\n\n\n%s\n%s\n\n" % (text, len(text) * "=")
        
def send_newsletters(newsletter_types, date, sources, options):
    if options.only:
        msg("Only sending mail to %s" % (options.only), options)
    combined_mails = {}
    email_from = mysociety.config.get('MAIL_FROM')
    
    for newsletter_type in newsletter_types:
        for newsletter in newsletter_type.objects.all():
            msg("Getting data for %s newsletter" % (newsletter), options)
            for subscription in newsletter.subscription_set.all():
                user = subscription.user
                format = user.profile.get_email_format_display()
                content = newsletter.render(format, sources, date)
    
                if not options.only or user.username == options.only:
                    
                    if (user.profile.one_email):
                        content_with_header = mail_separator(format, newsletter.subject) + content
                        existing_content = combined_mails.setdefault(user, '') 
                        combined_mails[user] = existing_content + content_with_header
                    else:
                        msg("Sending %s format %s newsletter to %s" % (format, newsletter, user.email), options)
                        send_mail(newsletter.subject, date, content, email_from, user.email, format)
                       
    for user, content in combined_mails.items():
        msg("Sending %s format combined newsletter to %s" % (format, user.email), options)
        send_mail('Combined site statistics', date, content, email_from, user.email, user.profile.get_email_format_display())