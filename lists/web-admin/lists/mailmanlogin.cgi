#!/usr/bin/perl -w -I../../../perllib
#
# mailmanlogin.cgi:
# Log in to part of the Mailman admin interface and obtain a cookie, which we
# give back to the user.
# 
# This is designed to be called through the mod_rewrite mechanism to ensure
# that the user is logged in which an appropriate cookie, bypassing Mailman's
# own idiotic scheme.
#
# Copyright (c) 2006 UK Citizens Online Democracy. All rights reserved.
# Email: chris@mysociety.org; WWW: http://www.mysociety.org/
#

my $rcsid = ''; $rcsid .= '$Id: mailmanlogin.cgi,v 1.3 2006-06-28 12:58:08 chris Exp $';

use strict;

BEGIN {
    use mySociety::Config;
    mySociety::Config::set_file('../../conf/general');
}

use CGI::Fast;
use WWW::Mechanize;

my $M = new WWW::Mechanize(agent => "mailmanlogin $rcsid");
my $hh = new HTTP::Headers();
$M->default_headers($hh);

# Details of the local Mailman installation.
my $mailman_login_url = 'http://lists.mysociety.org/admin/lists/mailman/admin/mailman';
my $mailman_site_password = 'secret';

# get_mailman_cookie
# Obtain a site-wide login cookie for Mailman, by filling out the admin
# interface login page and capturing the cookie in the response.
sub get_mailman_cookie () {
    our ($cookie, $cookie_time);

    return $cookie if ($cookie && $cookie_time > time() - 600);

    # Nuke any existing cookies -- we want to make sure we get a new one.
    $cookie = undef;
    $M->cookie_jar()->clear();
    $M->get($mailman_login_url) or return undef;
    
    $M->submit_form(
            form_number => 1,
            fields => {
                adminpw => $mailman_site_password
            }
        ) or return undef;

    # Now see if there's a cookie in the response.
    $M->cookie_jar()->scan(sub ($$$$$$$$$$$) {
            my ($key, $val) = @_[1 .. 2];
            if ($key eq 'site') {
                $cookie = $val;
                $cookie_time = time();
            }
        });

    return $cookie;
}

# Main loop. We are called with a parameter url, giving the real Mailman URL
# to redirect to. We redirect adding a cookie to log the user in to the
while (my $q = new CGI::Fast()) {
    my $url = $q->param('url');
    if (!defined($url)) {
        print $q->redirect('/admin/lists/mailman/admin');
        next;
    }

    $hh->header(Authorization => $ENV{HTTP_AUTHORIZATION});

    my $cookie = get_mailman_cookie();
    if ($cookie) {
        $cookie = $q->cookie(
                        -name => 'site',
                        -value => $cookie,
                        -secure => 1, # XXX will mod_proxy honour this?
                        -path => '/',
                        -expires => '+365d'
                    );
    }

    print $q->redirect(
                -uri => $url,
                -cookie => $cookie
            );
}
