#!/usr/bin/perl -w

# rss.cgi:
# RSS for Neighbourhood Fix-It
#
# Copyright (c) 2007 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org. WWW: http://www.mysociety.org
#
# $Id: rss.cgi,v 1.7 2007-05-16 17:51:21 matthew Exp $

use strict;
require 5.8.0;

# Horrible boilerplate to set up appropriate library paths.
use FindBin;
use lib "$FindBin::Bin/../perllib";
use lib "$FindBin::Bin/../../perllib";
use URI::Escape;

use Page;
use mySociety::Config;
use mySociety::DBHandle qw(dbh);
use mySociety::Alert;
use mySociety::Web;

BEGIN {
    mySociety::Config::set_file("$FindBin::Bin/../conf/general");
    mySociety::DBHandle::configure(
        Name => mySociety::Config::get('BCI_DB_NAME'),
        User => mySociety::Config::get('BCI_DB_USER'),
        Password => mySociety::Config::get('BCI_DB_PASS'),
        Host => mySociety::Config::get('BCI_DB_HOST', undef),
        Port => mySociety::Config::get('BCI_DB_PORT', undef)
    );
}

sub main {
    my $q = shift;
    my $type = $q->param('type') || '';
    if ($type eq 'local_problems') {
        my $x = $q->param('x');
        my $y = $q->param('y');
        my $qs = 'x='.$x.';y='.$y;
	my $d = $q->param('d');
	$qs .= ";d=$d" if $d;
	$d = 10 unless $d;
	$d = 100 if $d > 100;
        $x = ($x * 5000 / 31);
        $y = ($y * 5000 / 31);
        mySociety::Alert::generate_rss($type, $qs, $x, $y, $d);
    } elsif ($type eq 'new_updates') {
        my $id = $q->param('id');
        my $qs = 'id='.$id;
        mySociety::Alert::generate_rss($type, $qs, $id);
    } elsif ($type eq 'new_problems') {
        mySociety::Alert::generate_rss($type, '');
    } elsif ($type eq 'council_problems') {
        my $id = $q->param('id');
        my $qs = 'council='.$id;
        mySociety::Alert::generate_rss($type, $qs, $id);
    } else {
        throw Error::Simple('Unknown alert type') unless $type;
    }
    dbh()->rollback();
}
Page::do_fastcgi(\&main);

