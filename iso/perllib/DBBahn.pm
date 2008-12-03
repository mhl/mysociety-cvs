#!/usr/bin/perl -w
#
# DBBahn.pm
#
# Package containing various Deutsche Bahn related functions
#
# Copyright (c) 2008 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#

my $rcsid = ''; $rcsid .= '$Id: DBBahn.pm,v 1.4 2008-12-03 01:15:53 francis Exp $';

use strict;
require 5.8.0;

use FindBin;
use lib "$FindBin::Bin/../perllib";
use lib "$FindBin::Bin/../../perllib";

use WWW::Mechanize;
use HTML::Entities;
use HTML::TreeBuilder;
use Data::Dumper;

use mySociety::StringUtils;

sub get_timings {
    my ($to, $dbh) = @_; # , $line) = @_;

    # Get HTML of results page, using cache
    my $html = $dbh->selectrow_array('select content from cache where cache.url = ?', {}, $to);
    if (!$html) {
        my @params = (
            queryPageDisplayed => 'yes',
            REQ0JourneyStopsSA => 1,
            REQ0JourneyStopsSG => 'London St Pancras International',
            REQ0JourneyStopsZA => 1,
            REQ0JourneyStopsZG => $to,

            REQ0JourneyDate    => 'Tu, 02.12.08',
            wDayExt0 => 'Mo|Tu|We|Th|Fr|Sa|Su',
            REQ0JourneyTime    => '07:00',
            REQ0HafasSearchForw => 1,
            REQ1JourneyDate    => '',
            wDayExt1 => 'Mo|Tu|We|Th|Fr|Sa|Su',
            REQ1JourneyTime    => '',
            REQ1HafasSearchForw => 1,

            REQ0JourneyProduct_prod_list => '1:1111111111000000',
            existOptimizePrice => 1,
            REQ0HafasOptimize1 => '0:1',
            existOptionBits => 'yes',
            REQ0HafasChangeTime => '0:1',

            'REQ0Tariff_TravellerType.1' => 'E',
            'REQ0Tariff_TravellerAge.1' => 30,
            'REQ0Tariff_TravellerReductionClass.1' => '0',
            'REQ0Tariff_Class' => '2',

            start => 'Search connection',
        );

        my $url = 'http://reiseauskunft.bahn.de/bin/query.exe/en?ld=212.139&rt=1&OK';
        my $m = new WWW::Mechanize();
        $m->agent_alias('Windows Mozilla');
        $m->post($url, \@params);

        $html = $m->content();
        if ($html =~ /several possible stops/) {
            if ($html =~ /<option value="([^"]*?)">\Q$to\E<\/option>/) {
                $m->submit_form(
                    form_name => 'formular',
                    fields => { 'REQ0JourneyStopsZK' => $1 },
                    button => 'start'
                );
                $html = $m->content();
            } elsif ($html =~ /<option value="([^"]*?)">(.*?)<\/option>/) {
                $m->submit_form(
                    form_name => 'formular',
                    fields => { 'REQ0JourneyStopsZK' => $1 },
                    button => 'start'
                );
                $html = $m->content();
            }
        }
        $m = undef;

        $dbh->do('insert into cache (url, content) values (?, ?)', {}, $to, $html);
        $dbh->commit();

        sleep 1;
    }

    #print $html;exit;

    # Parse response

    if ($html =~ /Details for all/) {
        # Okay, pass through
    } elsif ($html =~ /several possible stops/) {
        return 'Multiple, no exact match'; # Shouldn't get here because of above
    } elsif ($html =~ /no route found/) {
        return 'No route found';
    } else {
        return 'Unknown error';
    }

    $html =~ /Pancras International<br \/>(.*?)<\/span>/;
    my $actual_to = $1;
    
    my $tree = HTML::TreeBuilder->new_from_content($html);
    my @results = $tree->look_down('class', 'result');
    my $results = $results[1];
    
    my @rows = $results->find('tr');

    # check header row is as expected
    my $row = shift @rows;
    my @cells = $row->find('th');
    $_ = shift @cells; die "unexpected header " . $_->as_text if $_->as_text ne "Station/Stop";
    $_ = shift @cells; die "unexpected header " . $_->as_text if $_->as_text ne "Date";
    $_ = shift @cells; die "unexpected header " . $_->as_text if $_->as_text ne "Time";
    $_ = shift @cells; die "unexpected header " . $_->as_text if $_->as_text ne "Duration";
    $_ = shift @cells; die "unexpected header " . $_->as_text if $_->as_text ne "Chg.";
    $_ = shift @cells; die "unexpected header " . $_->as_text if $_->as_text ne "Products";
    $_ = shift @cells; die "unexpected header " . $_->as_text if $_->as_text ne " Fare ";
    $_ = shift @cells; die "unexpected header " . $_->as_text if $_->as_text ne " Return journey ";
    $_ = shift @cells; die "unexpected header " . $_->as_text if $_->as_text ne " Remember ";

    # check second row is earlier thing
    $row = shift @rows;
    @cells = $row->find('td');
    die if $cells[2]->as_text ne "Earlier";

    # find the time we like most. We're taking the train that
    # leaves between 7am and 7:59am and is shortest in duration. Failing that
    # first one leaving after 8am.
    my ($best, $first_in_list);
    while (1) {
        my $row = shift @rows;
        my @cells = $row->find('td');
        @cells = map { mySociety::StringUtils::trim($_->as_text) } @cells;
        my ($depart_station, $depart_date, $depart_sort, $depart_time, $duration, $changes, $products, $fare, $return_journey, $remember) = @cells;
        last if $depart_sort eq 'Later';
        die if $depart_sort ne 'dep';

        $row = shift @rows;
        @cells = $row->find('td');
        @cells = map { mySociety::StringUtils::trim($_->as_text) } @cells;
        my ($arrive_station, $arrive_date, $arrive_sort, $arrive_time) = @cells;
        die if $arrive_sort ne 'arr';

        my $duration_seconds;
        if ($duration !~ m/^([0-9]+):([0-9]+)$/) {
            die "duration $duration not parsed";
        } else {
            $duration_seconds = $1 * 60 * 60 + $2 * 60;
        }

        my ($hour, $minute);
        if ($depart_time !~ m/^([0-9]+):([0-9]+)$/) {
            die "depart time $depart_time not parse";
        } else {
            $hour = $1;
            $minute = $2;
        }

        my $this_one;
        $this_one->{duration_seconds} = $duration_seconds;
        $this_one->{duration} = $duration;
        $this_one->{depart_date} = $depart_date;
        $this_one->{depart_time} = $depart_time;
        $this_one->{arrive_date} = $arrive_date;
        $this_one->{arrive_time} = $arrive_time;

        $first_in_list = $this_one if !$first_in_list;

        # only keep things during the hour of 7
        next if $hour != 7;

        #print "$depart_date $depart_time takes $duration or $duration_seconds secs\n";
        if (!defined($best) || $best->{duration_seconds} > $duration_seconds) {
            $best = $this_one;
        }

    }

    if (!$best) {
        $best = $first_in_list;
    }

    $best->{actual_to} = $actual_to;
    return $best;
}

1;
