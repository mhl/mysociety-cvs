#!/usr/bin/env python2.5
#
# contact.cgi:
# Contact us page
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: contact.cgi,v 1.4 2009-04-01 15:33:05 matthew Exp $
#

import re
import sys
from email.mime.text import MIMEText
import smtplib
sys.path.extend(("../pylib", "../../pylib"))
import fcgi

from page import *
import mysociety.config
mysociety.config.set_file("../conf/general")

def main(fs):
    if 'submit_form' in fs:
        return contact_submit(fs)
    return contact_page(fs)

def contact_submit(fs):
    errors = []
    name = fs.getfirst('name', '')
    email = fs.getfirst('em', '')
    subject = fs.getfirst('subject', '')
    message = fs.getfirst('message', '')

    if not re.search(r'\S', name):
        errors.append('Please give your name')
    if not re.search('\S', email):
        errors.append('Please give your email')
    elif not validate_email(email):
        errors.append('Please give a valid email address')
    if not re.search(r'\S', subject):
        errors.append('Please give a subject')
    if not re.search(r'\S', message):
        errors.append('Please write a message')
    if errors:
        errors = '<ul id="errors"><li>%s</li></ul>' % '</li><li>'.join(errors)
        return contact_page(fs, errors)

    message = re.sub('\r\n', '\n', message)
    subject = re.sub('\r|\n', ' ', subject)
    name = re.sub('\r|\n', ' ', name)
    postfix = '[ Sent by contact.cgi on %s. IP address %s%s. ]' % (
        os.environ.get('HTTP_HOST', 'n/a'),
        os.environ.get('REMOTE_ADDR', 'n/a'),
        os.environ.get('HTTP_X_FORWARDED_FOR', '') and ' (forwarded from '+os.environ.get('HTTP_X_FORWARDED_FOR')+')' or ''
    )

    msg = MIMEText("%s\n\n%s" % (message, postfix))
    msg['From'] = '%s <%s>' % (name, email)
    msg['To'] = mysociety.config.get('CONTACT_EMAIL')
    msg['Subject'] = 'COL message: %s' % subject
    server = smtplib.SMTP('localhost')
    try:
        server.sendmail(email, mysociety.config.get('CONTACT_EMAIL'), msg.as_string())
    except Exception, e:
        return contact_page(fs, e)

    server.quit()
    return Response('contact-thanks')

def contact_page(fs, errors = ''):
    return Response('contact', {
        'errors': errors,
        'name': fs.getfirst('name', ''),
        'email': fs.getfirst('em', ''),
        'subject': fs.getfirst('subject', ''),
        'message': fs.getfirst('message', ''),
        'contact_email': mysociety.config.get('CONTACT_EMAIL'),
    })

# Main FastCGI loop
while fcgi.isFCGI():
    fcgi_loop(main)

