#!/usr/bin/python2.5
#
# index.cgi:
# Main code
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: invite.cgi,v 1.16 2009-09-24 15:09:41 duncan Exp $
#

import sys
sys.path.extend(("../pylib", "../../pylib", "/home/matthew/lib/python"))

from django.http import HttpResponseRedirect

import mysociety.config
mysociety.config.set_file("../conf/general")

from page import validate_email, \
                 render_to_response, \
                 wsgi_loop

from storage import StorageError , \
                    create_invite, \
                    token_exists

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
        except StorageError:
            vars['error'] = 'That email address has already had an invite.'
        else:
            vars['success'] = u'Thanks, we\u2019ll send an invite.'

            if not num:
                template = 'invite-none.html'

    if 'error' in vars:
        vars['email'] = email

    return render_to_response(template, vars)


def log_email(email):
    vars = {'email': email}

    if not email:
        vars['error'] = 'Please provide your email address.'
    elif not validate_email(email):
        vars['error'] = 'Please provide a valid email address.'
    else:
        try:
            create_invite(email, 'web')
        except StorageError:
            vars['error'] = 'That email address is already in our system.'

    template = 'invite-email.html' if 'error' in vars else 'invite-email-thanks.html'

    return render_to_response(template, vars)

def parse_token(token):
    if token_exists(token):
        response = HttpResponseRedirect('/')
        response.set_cookie('token', value=token, max_age=86400*28)
    else:
        response = HttpResponseRedirect('/signup')
        
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

