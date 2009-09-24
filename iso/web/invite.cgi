#!/usr/bin/python2.5
#
# index.cgi:
# Main code
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: invite.cgi,v 1.14 2009-09-24 13:28:21 duncan Exp $
#

import sys
sys.path.extend(("../pylib", "../../pylib", "/home/matthew/lib/python"))
from psycopg2 import IntegrityError

import mysociety.config
mysociety.config.set_file("../conf/general")

from page import *
from django.http import HttpResponseRedirect

from coldb import db

#----------- start of storage functions ----------
# The first part of getting the explicit database stuff out of
# the rather front-end bits below. Some functions to view and
# store data, which we can later change for different storage.

def create_invite(email,
                  source='web',
                  source_id=None):

    db().execute('BEGIN')
    try:
        # FIXME - check that psycopg converts None to 'NULL'.
        db().execute("INSERT INTO invite (email, source, source_id) VALUES (%s, %s, %s)", (email, source, source_id))
    except IntegrityError, e:
        # Let's assume the integrity error is because of a unique key
        # violation - ie. an identical row has appeared in the milliseconds
        # since we looked
        db().execute('ROLLBACK')

        # FIXME - should probably raise a different Exception.
        raise 

    if source_id:
        # If this is an friend invite, then we need to decrement the source's invite count
        db().execute('UPDATE invite SET num_invites = num_invites - 1 WHERE id=%s', (source_id,))
        db().execute('COMMIT')

        db().execute('SELECT num_invites FROM invite WHERE id=%s', (source_id,))
        num = db().fetchone()[0]

        # Return the number of invites left.
        return num

#-------- end of storage functions ----------

def friend_invite(invite, email):
    template = 'invite-friend.html'
    vars = {}

    if not email:
        vars['error'] = 'Please provide an email address.'
    if not validate_email(email):
        vars['error'] = 'Please provide a valid email address.'
    else:
        try:
            num = create_invite(email, 'friend', invite.id)
        except IntegrityError:
            vars['error'] = 'That email address has already had an invite.'
        else:
            vars['success'] = u'Thanks, we\u2019ll send an invite.'

            if not num:
                template = 'invite-none.html'

    if 'error' in vars:
        vars['email'] = email

    return render_to_response(template, vars)


def log_email(email):
    if not email:
        return render_to_response('invite-email.html', { 'email': email, 'error': 'Please provide your email address.' })
    if not validate_email(email):
        return render_to_response('invite-email.html', { 'email': email, 'error': 'Please provide a valid email address.' })

    db().execute('BEGIN')
    try:
        db().execute("INSERT INTO invite (email, source) VALUES (%s, 'web')", (email,))
    except IntegrityError, e:
        # Let's assume the integrity error is because of a unique key
        # violation - ie. an identical row has appeared in the milliseconds
        # since we looked
        db().execute('ROLLBACK')
        return render_to_response('invite-email.html', { 'email': email, 'error': 'That email address is already in our system.' })
    db().execute('COMMIT')

    return render_to_response('invite-email-thanks.html')

def parse_token(token):
    db().execute('SELECT * FROM invite WHERE token=%s', (token,))
    row = db().fetchone()

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
        return log_email(fs['email'])
    if 'signup' in fs:
        return render_to_response('invite-email.html', cache_max_age = 3600)

    # Link in email being clicked on
    if 'token' in fs:
        return parse_token(fs['token'])

    # Invite system
    invite = Invite()
    if not invite.num_invites or invite.num_invites==0:
        return render_to_response('invite-none.html')
    if 'friend' in fs:
        return friend_invite(invite, fs['friend'])
    return render_to_response('invite-friend.html')

# Main FastCGI loop
if __name__ == "__main__":
    wsgi_loop(main)

