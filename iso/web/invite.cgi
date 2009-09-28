#!/usr/bin/python2.5
#
# index.cgi:
# Main code
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: invite.cgi,v 1.22 2009-09-28 10:10:43 duncan Exp $
#

import sys
sys.path.extend(("../pylib", "../../pylib"))

from django.http import HttpResponseRedirect

import mysociety.config
mysociety.config.set_file("../conf/general")

import page
import storage

def invite_view(email, invite=None):
    """I think it's time to start calling things like this views.

    Arguments are:

    email - an email address as a string
    invite - either an Invite object or None

    If invite is None, then this is someone signing themself up on the web. 
    If invite is an Invite object, then it is someone who has been invited
    by a friend.
    """

    context = {'email': email}

    if not email:
        context['error'] = 'Please provide an email address.'
    if not page.validate_email(email):
        context['error'] = 'Please provide a valid email address.'
    else:
        try:
            num = storage.create_invite(
                email, 
                source_id=invite.id if invite else None
                )
        except storage.StorageError:
            context['error'] = 'That email address has already had an invite.'
        else:
            context['success'] = u'Thanks, we\u2019ll send an invite to %s.' %email
            # Since adding the email was successful, we probably don't want
            # the box still filled in.
            context.pop('email')

    if invite:
        if num:
            template = 'invite-friend.html'
        else:
            template = 'invite-none.html'
    else:
        if 'error' in context:
            template = 'invite-email.html'
        else:
            template = 'invite-email-thanks.html'

    return page.render_to_response(template, context)

def parse_token(token):
    if storage.get_invite_by_token(token):
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
        return invite_view(fs['email'])
    if 'signup' in fs:
        return page.render_to_response(
            'invite-email.html', 
            cache_max_age = 3600
            )

    # Link in email being clicked on
    if 'token' in fs:
        return parse_token(fs['token'])

    # Invite system
    invite = page.Invite()
    if not invite.num_invites:
        return page.render_to_response('invite-none.html')
    if 'friend' in fs:
        return invite_view(fs['friend'], invite=invite)

    return page.render_to_response('invite-friend.html')

# Main FastCGI loop
if __name__ == "__main__":
    page.wsgi_loop(main)

