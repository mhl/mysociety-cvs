#!/usr/bin/perl -w -I../perllib -I../../perllib
#
# ref-index.cgi:
# Main petition page.
#
# Copyright (c) 2006 UK Citizens Online Democracy. All rights reserved.
# Email: chris@mysociety.org; WWW: http://www.mysociety.org/
#

my $rcsid = ''; $rcsid .= '$Id: ref-index.cgi,v 1.28 2006-11-14 18:21:16 matthew Exp $';

use strict;

# use Compress::Zlib;
use HTTP::Date qw();
use utf8;

use mySociety::Config;
BEGIN {
    mySociety::Config::set_file("../conf/general");
}
use mySociety::DBHandle qw(dbh);
use mySociety::Web qw(ent);
use mySociety::WatchUpdate;

use Petitions;
use Petitions::Page;

my $W = new mySociety::WatchUpdate();

my $foad = 0;
$SIG{TERM} = sub { $foad = 1; };
while (!$foad && (my $q = new mySociety::Web())) {
    my $qp_ref = $q->ParamValidate(ref => qr/^[A-Za-z0-9-]{6,16}$/);
    my $qp_id = $q->ParamValidate(id => qr/^[0-9]+$/);
    my $ref = Petitions::DB::check_ref($qp_ref);
    if (!defined($ref)) {
        Petitions::Page::bad_ref_page($q, $qp_ref);
        next;
    }

    # Perhaps redirect to canonical ref if non-canonical was given.
    if ($qp_ref ne $ref && $q->request_method() =~ /^(GET|HEAD)$/) {
        my $url = "/$ref/";
        $url .= '?' . $q->query_string() if ($q->query_string());
        print $q->redirect($url);   # ugh -- will add ?ref=$ref
        next;
    }

    my $lastmodified = dbh()->selectrow_array('select extract(epoch from petition_last_change_time((select id from petition where ref = ?)))', {}, $ref);
    next if ($q->Maybe304($lastmodified));

    my $qp_signed = $q->param('signed');

    my $p = Petitions::DB::get($ref, 0, 1);
    my $title = Petitions::sentence($p, 1);
    my $html =
        Petitions::Page::header($q, $title);

    $html .= $q->h1($q->span({-class => 'ltr'}, 'E-Petitions'));
    $html .= $q->h2($q->span({-class => 'ltr'}, 'Sign a petition'));

    $html .= $q->p({ -id => 'finished' }, "This petition is now closed, as its deadline has passed.")
        if ($p->{status} eq 'finished');

    if ($qp_signed) {
        $html .=
            $q->p({ -id =>'success' },
                    "Thank you, you're now signed up to this petition! If you'd like to
                    tell your friends about it, its permanent web address is:",
                    $q->br(),
                    $q->strong($q->a({ -href => "/$ref/" },
                        ent(mySociety::Config::get('BASE_URL') . "/$ref/"
                    ))));
                    # XXX: *** Send to friend ***
                    
    }

    # If the ref has been marked as not to be shown, do not give a hint at its existance
    if ($p->{status} eq 'rejected' && !Petitions::show_part($p, 'ref')) {
        Petitions::Page::bad_ref_page($q, $qp_ref);
        next;
    }

    $html .= Petitions::Page::display_box($q, $p);
    $html .= Petitions::Page::sign_box($q, $p)
        if ($p->{status} eq 'live' && !$qp_signed);
    $html .= Petitions::Page::response_box($q, $p) if ($p->{response});
    if ($p->{status} ne 'rejected') {
        $html .= Petitions::Page::signatories_box($q, $p);
    } else {
        $html .= $q->start_div({-id => 'signatories'})
            . $q->h2($q->span({-class => 'ltr'}, 'Petition Rejected'));
        $html .= Petitions::Page::reject_box($q, $p);
        $html .= $q->end_div();
    }
    $html .= Petitions::detail($p);
    my $stat = 'View.' . $p->{ref};
    $stat .= '.signed' if ($qp_signed);
    $html .= Petitions::Page::footer($q, $stat);

    utf8::encode($html);

    # Perhaps send gzipped content.
    # XXX: Something goes wrong in some combination of gzip, squid,
    # another proxy, IE, who knows. Anyway, don't use gzip
    # my $ce = undef;
    # my $ae = $q->http('Accept-Encoding');
    # if ($ae) {
    #     my %encodings  = map { s/;.*$//; $_ => 1 } split(/,\s*/, $ae);
    #     if ($encodings{'*'}
    #         || $encodings{'gzip'}
    #         || $encodings{'x-gzip'}) {
    #         $html = Compress::Zlib::memGzip($html);
    #         $ce = 'gzip';
    #     }
    # }

    print $q->header(
                -content_length => length($html),
                -last_modified => HTTP::Date::time2str($lastmodified),
                #($ce
                #    ? (-content_encoding => $ce)
                #    : () ),
                -cache_control => 'max-age=1',
                -expires => '+1s'),
                $html;
    $W->exit_if_changed();
}
