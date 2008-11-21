#!/usr/bin/perl -w
#
# DBBahn.pm
#
# Package containing various Deutsche Bahn related functions
#
# Copyright (c) 2008 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#

my $rcsid = ''; $rcsid .= '$Id: DBBahn.pm,v 1.1 2008-11-21 18:37:08 francis Exp $';

use strict;
require 5.8.0;

use WWW::Mechanize;
use HTML::Entities;
use HTML::TreeBuilder;

sub get_timings {
    my ($to) = @_; # , $line) = @_;

    my @params = (
        queryPageDisplayed => 'yes',
	REQ0JourneyStopsSA => 1,
	REQ0JourneyStopsSG => 'London St Pancras International',
	REQ0JourneyStopsZA => 1,
	REQ0JourneyStopsZG => $to,

	REQ0JourneyDate    => 'Tu, 25.11.08',
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

    my $switched = '';
    my $html = $m->content();
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
            $switched = $2;
            $html = $m->content();
        }
    }
    $m = undef;

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
    $results = $results->as_HTML;
    $results =~ />dep<\/td>.*?<\/td>\s*<td[^>]*>\s*(.*?)\s*<\/td>/s;
    my $duration = "$1\t$actual_to";
    $duration .= "\t$switched" if $switched;
    return $duration;
}

1;
