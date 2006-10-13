#!/usr/bin/perl -w -I../perllib -I../../perllib
#
# ref-sign.cgi:
# Signup form for petitions site. Also process confirmation mail links.
#
# Copyright (c) 2006 UK Citizens Online Democracy. All rights reserved.
# Email: chris@mysociety.org; WWW: http://www.mysociety.org/
#

my $rcsid = ''; $rcsid .= '$Id: ref-sign.cgi,v 1.22 2006-10-13 17:03:52 matthew Exp $';

use strict;

use Digest::HMAC_SHA1 qw(hmac_sha1);
use MIME::Base64;
use utf8;

use mySociety::Config;
BEGIN {
    mySociety::Config::set_file("../conf/general");
}
use mySociety::DBHandle qw(dbh);
use mySociety::Web qw(ent);
use mySociety::WatchUpdate;
use mySociety::Util;

use Petitions;
use Petitions::Page;
use Petitions::RPC;

my $W = new mySociety::WatchUpdate();

sub i_check_email ($$) {
    return mySociety::Util::is_valid_email($_[1]);
}

sub i_check_postcode ($$) {
    return mySociety::Util::is_valid_postcode($_[1]);
}

use Data::Dumper;

# signup_page Q REF
# Generate the signup page for REF.
use Time::HiRes qw(sleep time);
sub signup_page ($$) {
    my mySociety::Web $q = shift;
    my $p = shift;
    
    my $html =
        Petitions::Page::header($q, 'Signature addition');

    my $qp_name = $q->param('name');
    my $qp_email = $q->ParamValidate(email => \&i_check_email);
    my $qp_email2 = $q->ParamValidate(email2 => \&i_check_email);
    my $qp_address = $q->param('address');
    my $qp_postcode = $q->ParamValidate(postcode => \&i_check_postcode);
    my $qp_overseas = $q->param('overseas');
    $qp_overseas = undef if $qp_overseas eq '-- Select --';

    my %errors;
    $errors{name} = 'Please enter your name'
        if (!$qp_name || $qp_name eq '<Enter your name>');
    if (!$qp_email) {
        $errors{email} = 'Please enter a valid email address';
    } elsif (!$qp_email2 || $qp_email ne $qp_email2) {
        $errors{email2} = 'The two email addresses do not match';
    }
    $errors{address} = 'Please enter your address'
        if (!$qp_address);
    $errors{postcode} = 'Please enter a valid postcode, such as OX1 3DR, or choose an overseas territory'
        if (!$qp_postcode && !$qp_overseas);
    $errors{postcode} = 'Please enter a valid postcode OR choose an overseas territory'
        if (defined($qp_postcode) && defined($qp_overseas));

    if (!keys(%errors)) {
        # Success. Add the signature, assuming that we can.
#        my $s = Petitions::DB::is_valid_to_sign($p->{id}, $qp_email);
#        dbh()->commit();    # finish transaction
#       # XXX ref-index will have checked that the petition is valid to sign
        # before sending us here, but ser isn't timestamped so we should
        # re-check here. But mustn't use the database, obviously.
        my $s = 'ok';
        if ($s eq 'finished') {
            $html .= $q->p('Sorry, but that petition has finished, so you cannot sign it.');
        } elsif ($s eq 'none') {
            $html .= $q->p("We couldn't find that petition.");
        } else {
            # Either OK or already signed. We must not give away the fact that
            # any particular person has already signed a petition, so act the
            # same in each case.
            if (Petitions::RPC::do_rpc({
                            ref => $p->{ref},
                            email => $qp_email,
                            name => $qp_name,
                            address => $qp_address,
                            postcode => $qp_postcode,
                            overseas => $qp_overseas
                        })) {
                $html .=
                    $q->h1({-class => 'ltr'}, "Now check your email!")
                    . $q->p({-class => 'noprint loudmessage', -align => 'center'},
                        "We've sent you an email; before your signature is added to
                        the petition you'll have to click the link in it."
                    );
            } else {
                $errors{busy} =
                        "Sorry, but we weren't able to add your signature to
                        the petition, because our site is extremely busy at
                        the moment. Please try again in a few minutes' time.";
            }
        }
    } 
    
    if (keys(%errors)) {
        $html .=
            $q->div({ -id => 'errors' },
                $q->ul(
                    $q->li([
                        map { ent($_) } values(%errors)
                    ])
                )
            )
            . Petitions::Page::display_box($q, $p)
            . Petitions::Page::sign_box($q, $p);
    }
    $html .= Petitions::Page::footer($q, 'Sign_' . $p->{ref});

    utf8::encode($html);
    print $q->header(-content_length => length($html)), $html;
}

# confirm_page Q REF TOKEN
# Given a confirm TOKEN, validate a signup or petition creation.
sub confirm_page ($$$) {
    my ($q, $ref, $token) = @_;
    
    my $html = '';
    my ($what, $id);
    if (!(($what, $id) = Petitions::Token::check($token))) {
        # Token was not valid.
        $html = Petitions::Page::header($q, "Something is wrong")
                . $q->p("
                    Unfortunately, we couldn't understand the signup link that
                    you've used. If you typed the link in manually, please
                    re-check that you've got it absolutely right.")
                . Petitions::Page::footer($q, 'Bad_confirm_link');
    } elsif ($what eq 'e') {
        # Edit rejected petition for resubmission. Redirect to /new.
        print $q->redirect("/new?token=$token");
    } elsif (Petitions::RPC::do_rpc({
                    confirm => $what,
                    id => $id
                })) {

        if ($what eq 'p') {
            # Display message about petition creation.
            $html = Petitions::Page::header($q, "Petition created")
                    . $q->p({ -class => 'noprint loudmessage' },
                        "Thank you for creating your petition")
                    . $q->p({ -class => 'noprint loudmessage',
                        -align => 'center' }, "
                        It has been entered on our system and will now go to
                        the Number 10 team for approval.")
                    . Petitions::Page::footer($q, 'Confirm_Petition');
        } else {
            # Redirect so that the token isn't left in the browser.
            print $q->redirect("/$ref?signed=1");
            return;
        }
    } else {
        my $desc;
        if ($what eq 'p') {
            $desc = "the creation of your petition";
        } else {
            $desc = "your signature";
        }
        $html = Petitions::Page::header($q, "Sorry, we couldn't confirm $desc")
                . $q->p("
                    Unfortunately, we weren't able to confirm $desc,
                    because our site is extremely busy at the moment.
                    Please try again in a few minutes' time.")
                . Petitions::Page::footer($q, 'Confirm_something_busy');
    }

    utf8::encode($html);
    print $q->header(-content_length => length($html)), $html;
}

my $foad = 0;
$SIG{TERM} = sub { $foad = 1; };

# accept_loop
# Accept and handle FastCGI requests.
sub accept_loop () {
    while (!$foad && (my $q = new mySociety::Web())) {
        my $qp_ref = $q->ParamValidate(ref => qr/^[A-Za-z0-9-]{6,16}$/);
        if (!defined($qp_ref)) {
            print $q->redirect("/");
            next;
        }

        # Confirm page.
        my $qp_token = $q->ParamValidate(token => qr/^[A-Za-z0-9_-]+$/);
        if (defined($qp_token)) {
            confirm_page($q, $qp_ref, $qp_token);
            next;
        }

        # This page is only ever invoked for a POST form, so redirect to the
        # petition page if this is a GET.
        if ($q->request_method() ne 'POST') {
            warn "bad method";
            print $q->redirect("/$qp_ref");
            next;
        }

        # Get the serialised petition data from the query and check it.
        my $qp_ser = $q->ParamValidate(ser => qr#^[A-za-z0-9/+=]+$#);
        if (!defined($qp_ser)) {
            warn "missing/invalid serialised data in POST request";
            print $q->redirect("/$qp_ref");
            next;
        }
        my $ser = decode_base64($qp_ser);
        if (substr($ser, -20) ne hmac_sha1(substr($ser, 0, length($ser) - 20), Petitions::DB::secret())) {
            warn "bad signature in serialised data '$qp_ser'";
            print $q->redirect("/$qp_ref");
            next;
        }

        my $p = RABX::unserialise(substr($ser, 0, length($ser) - 20));

        signup_page($q, $p);

    #    $W->exit_if_changed();
    }
}

# Awful. We need lots of processes to handle lots of concurrent signups (since
# they need to wait while petsignupd batches requests and acks them) but we
# mustn't have lots of database connections (because they're expensive). So do
# a dummy query to force Petitions::DB to cache the secret, which we need to
# validate incoming data, and then disconnect.
my $secret = Petitions::DB::secret();
dbh()->disconnect();

# We launch child processes here, so we can have more ref-sign.cgi processes
# without having to alter the global FastCGI server number config parameter
# NB: This doesn't run well in a cgi environment, only in fastcgi
mySociety::Util::manage_child_processes({
               web => [mySociety::Config::get("NUM_SIGN_PROCESSES", 20),
                        \&accept_loop]
            });

exit(0);

