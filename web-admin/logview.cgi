#!/usr/bin/perl -w -I../../projects/mysociety/perllib
#
# logview.cgi:
# Log viewing script.
#
# Copyright (c) 2005 UK Citizens Online Democracy. All rights reserved.
# Email: chris@mysociety.org; WWW: http://www.mysociety.org/
#

my $rcsid = ''; $rcsid .= '$Id: logview.cgi,v 1.1 2005-01-28 19:44:45 chris Exp $';

use Carp qw(verbose);
use CGI::Fast;
use DateTime;
use DateTime::Format::Strptime;
use Error qw(:try);

use mySociety::Logfile;
use mySociety::Logfile::ErrorLog;
use mySociety::Logfile::Aggregate;

use constant MAX_FILES => 32;

$lf = new mySociety::Logfile::Aggregate('mySociety::Logfile::ErrorLog', "/data/vhost/www.writetothem.com/logs/error_log.*")
    or die;

my $timeparser = new DateTime::Format::Strptime(pattern => '%Y%m%d%H%M%S');

while (my $q = new CGI::Fast()) {
    my $when;
    if (defined(my $w = $q->param('when'))) {
        $when = $timeparser->parse($w);
    }
    $when ||= DateTime->now();
    my $howlong = $q->param('howlong');
    $howlong = 7200 if (!defined($howlong) || $howlong !~ m#^[0-9]\d+$#);
    print "Content-Type: text/plain\n\n";
    $off = $lf->findtime($when - new DateTime::Duration(seconds => $howlong));

    if (defined($off)) {
        my $t;
        do {
            my $l = $lf->getline($off);
            my $f = $lf->parse($l);
            print "$f->{time} " if (exists($f->{time}));
            print "-> $f->{text}\n";
            $t = $f->{time} if (exists($f->{time}));

            $off = $lf->nextline($off);
        } while (defined($off) and $t <= $when);
    } else {
        print "  [ no log entries in interval ]\n";
    }
}

