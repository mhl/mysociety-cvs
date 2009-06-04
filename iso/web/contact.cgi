#!/usr/bin/env python2.5
#
# contact.cgi:
# Contact us page
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: contact.cgi,v 1.13 2009-06-04 14:40:27 francis Exp $
#

import re
import sys
sys.path.extend(("../pylib", "../../pylib"))
import fcgi

import mysociety.config
mysociety.config.set_file("../conf/general")

from page import *
from sendemail import send_email

def main(fs):
    if 'submit_form' in fs:
        return contact_submit(fs)
    return contact_page(fs)

def contact_submit(fs):
    errors = []
    name = fs.get('name', '')
    email = fs.get('em', '')
    subject = fs.get('subject', '')
    message = fs.get('message', '')

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

    success = send_email(email, mysociety.config.get('CONTACT_EMAIL'), message, {
        'Subject': 'Mapumental message: %s' % subject,
        'From': (email, name),
        'To': mysociety.config.get('CONTACT_EMAIL'),
    })
    if not success:
        return contact_page(fs, [ 'I am afraid we could not send your message. Please try again later.' ])

    return render_to_response('contact-thanks.html')

def contact_page(fs, errors = []):
    return render_to_response('contact.html', {
        'errors': errors,
        'name': fs.get('name', ''),
        'email': fs.get('em', ''),
        'subject': fs.get('subject', ''),
        'message': fs.get('message', ''),
        'contact_email': mysociety.config.get('CONTACT_EMAIL'),
    })

# Main FastCGI loop
if __name__ == "__main__":
    wsgi_loop(main)
