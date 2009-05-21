#!/usr/bin/python2.5
#
# index.cgi:
# Main code
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: invite.cgi,v 1.6 2009-05-21 16:33:25 francis Exp $
#

import sys
sys.path.extend(("../pylib", "../../pylib", "/home/matthew/lib/python"))
import fcgi
from psycopg2 import IntegrityError

from page import *
from django.http import HttpResponseRedirect

import mysociety.config
mysociety.config.set_file("../conf/general")

import coldb
db = coldb.get_cursor()

def friend_invite(invite, email):
    if not email:
        return render_to_response('invite-friend.html', { 'email': email, 'error': 'Please provide an email address.' })
    if not validate_email(email):
        return render_to_response('invite-friend.html', { 'email': email, 'error': 'Please provide a valid email address.' })
    db.execute('BEGIN')
    try:
        db.execute("INSERT INTO invite (email, source, source_id) VALUES (%s, 'friend', %s)", (email, invite.id))
    except IntegrityError, e:
        # Let's assume the integrity error is because of a unique key
        # violation - ie. an identical row has appeared in the milliseconds
        # since we looked
        db.execute('ROLLBACK')
        return render_to_response('invite-friend.html', { 'email': email, 'error': 'That email address has already had an invite.' })
    db.execute('UPDATE invite SET num_invites = num_invites - 1 WHERE id=%s', (invite.id,))
    db.execute('COMMIT')
    db.execute('SELECT num_invites FROM invite WHERE id=%s', (invite.id,))
    num = db.fetchone()[0]
    vars = {
        'success': u'Thanks, we\u2019ll send an invite.',
    }
    if num==0:
        return render_to_response('invite-none.html', vars)
    return render_to_response('invite-friend.html', vars)

def log_email(email):
    if not email:
        return render_to_response('invite-email.html', { 'email': email, 'error': 'Please provide your email address.' })
    if not validate_email(email):
        return render_to_response('invite-email.html', { 'email': email, 'error': 'Please provide a valid email address.' })
    db.execute('BEGIN')
    try:
        db.execute("INSERT INTO invite (email, source) VALUES (%s, 'web')", (email,))
    except IntegrityError, e:
        # Let's assume the integrity error is because of a unique key
        # violation - ie. an identical row has appeared in the milliseconds
        # since we looked
        db.execute('ROLLBACK')
        return render_to_response('invite-email.html', { 'email': email, 'error': 'That email address is already in our system.' })
    db.execute('COMMIT')
    return render_to_response('invite-email-thanks.html')

def parse_token(token):
    db.execute('SELECT * FROM invite WHERE token=%s', (token,))
    row = db.fetchone()
    if not row:
        return HttpResponseRedirect('/signup')
    response = HttpResponseRedirect('/')
    response.set_cookie('token', value=token, max_age=86400*28)
    return response

#####################################################################
# Main FastCGI loop
    
def main(fs):
    # Someone signing themselves up
    if 'email' in fs:
        return log_email(fs.getfirst('email'))
    if 'signup' in fs:
        return render_to_response('invite-email.html', cache_max_age = 3600)

    # Link in email being clicked on
    if 'token' in fs:
        return parse_token(fs.getfirst('token'))

    # Invite system
    invite = Invite(db)
    if not invite.num_invites or invite.num_invites==0:
        return render_to_response('invite-none.html')
    if 'friend' in fs:
        return friend_invite(invite, fs.getfirst('friend'))
    return render_to_response('invite-friend.html')

# Main FastCGI loop
while fcgi.isFCGI():
    fcgi_loop(main)
    db.execute('ROLLBACK')

