#!/usr/bin/env python2.5
#
# contact.cgi:
# Contact us page
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: contact.cgi,v 1.10 2009-05-14 12:21:45 matthew Exp $
#

import re
import sys
sys.path.extend(("../pylib", "../../pylib"))
import fcgi

from page import *
from sendemail import send_email
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
        return contact_page(fs, errors)

    postfix = '[ Sent by contact.cgi on %s. IP address %s%s. ]' % (
        os.environ.get('HTTP_HOST', 'n/a'),
        os.environ.get('REMOTE_ADDR', 'n/a'),
        os.environ.get('HTTP_X_FORWARDED_FOR', '') and ' (forwarded from '+os.environ.get('HTTP_X_FORWARDED_FOR')+')' or ''
    )
    message = message + "\n\n" + postfix

    send_email(email, mysociety.config.get('CONTACT_EMAIL'), message, {
        'Subject': 'Mapumental message: %s' % subject,
        'From': (email, name),
        'To': mysociety.config.get('CONTACT_EMAIL'),
    })

    return render_to_response('contact-thanks.html')

def contact_page(fs, errors = []):
    return render_to_response('contact.html', {
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

