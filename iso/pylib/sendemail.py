# email.py:
# Functions for sending email
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: sendemail.py,v 1.2 2009-05-14 12:50:47 matthew Exp $
#

import re, smtplib
from email.message import Message
from email.header import Header
from email.utils import formataddr, make_msgid
from email.charset import Charset, QP

charset = Charset('utf-8')
charset.body_encoding = QP

def send_email(sender, to, message, headers={}):
    """Sends MESSAGE from SENDER to TO, with HEADERS
    Returns True if successful, False if not"""

    message = re.sub('\r\n', '\n', message)

    msg = Message()
    msg.set_payload(message, charset)
    msg['Message-ID'] = make_msgid()

    for key, value in headers.items():
        if isinstance(value, tuple):
            email = re.sub('\r|\n', ' ', value[0])
            name = re.sub('\r|\n', ' ', value[1])
            if isinstance(name, str):
                name = unicode(name, 'utf-8')
            name = Header(name, 'utf-8')
            msg[key] = formataddr((str(name), email))
        else:
            value = re.sub('\r|\n', ' ', value)
            if isinstance(value, str):
                value = unicode(value, 'utf-8')
            msg[key] = Header(value, 'utf-8')

    success = True
    server = smtplib.SMTP('localhost')
    try:
        server.sendmail(sender, to, msg.as_string())
    except smtplib.SMTPResponseException, e:
        success = False
    finally:
        server.quit()
    return success

