#!/usr/bin/perl
#
# DaDem.pm:
# Implementation of DaDem functions, to be called by XMLRPC.
#
# Copyright (c) 2004 UK Citizens Online Democracy. All rights reserved.
# Email: chris@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: DaDem.pm,v 1.3 2004-10-14 15:49:22 francis Exp $
#

package DaDem;

use strict;
use mySociety::DaDem;
use mySociety::VotingArea;
use Data::Dumper;

=head1 NAME

DaDem

=head1 DESCRIPTION

Implementation of DaDem.

=head1 FUNCTIONS

=over 4

=item get_representatives ID

Given the ID of an area, return a list of the representatives returned by that
area, or, on failure, an error code.

=cut
sub get_representatives ($$) {
    my ($x, $id) = @_;
    my %db = (
            2 => [1],
            4 => [2, 3, 4],
            6 => [5],
            8 => [6, 7, 8, 9, 10, 11, 12]
        );

    if (exists($db{$id})) {
        return $db{$id};
    } else {
        return 1;   # DADEM_UNKNOWN_AREA
    }
}

=item get_representative_info ID

Given the ID of a representative, return a reference to a hash of information
about that representative, including:

=over 4

=item type

Numeric code for the type of voting area (for instance, CED or ward) for which
the representative is returned.

=item name

The representative's name.

=item contact_method

How to contact the representative.

=item email

The representative's email address (only specified if contact_method is
CONTACT_EMAIL).

=item fax

The representative's fax number (only specified if contact_method is
CONTACT_FAX).

=back

or, on failure, an error code.

=cut
sub get_representative_info ($$) {
    my ($x, $id) = @_;
    my %db = (
            1 => {
                type => mySociety::VotingArea::CED,
                'voting_area' => 2,
                name => 'Maurice Leeke',
                contact_method => 'email',
                email => 'Maurice.Leeke@cambridgeshire.gov.uk'
            },

            2 => {
                'type' => mySociety::VotingArea::DIW,
                'voting_area' => 4,
                'name' => 'Diane Armstrong',
                'contact_method' => 'email',
                'email' => 'diane_armstrong@tiscali.co.uk'
            },
            
            3 => {
                'type' => mySociety::VotingArea::DIW,
                'voting_area' => 4,
                'name' => 'Max Boyce',
                'contact_method' => 'email',
                'email' => 'maxboyce@cix.co.uk'
            },
            
            4 => {
                'type' => mySociety::VotingArea::DIW,
                'voting_area' => 4,
                'name' => 'Ian Nimmo-Smith',
                'contact_method' => 'email',
                'email' => 'ian@monksilver.com'
            },
            
            5 => {
                'type' => mySociety::VotingArea::WMC,
                'voting_area' => 6,
                'name' => 'Anne Campbell',
                'contact_method' => 'fax',
                'fax' => '+441223311315'
            },
            
            6 => {
                'type' => mySociety::VotingArea::EUR,
                'voting_area' => 8,
                'name' => 'Anne Campbell',
                'name' => 'Geoffrey Van Orden',
                'contact_method' => 'fax',
                'fax' => '+3222849332'
            },
            
            7 => {
                'type' => mySociety::VotingArea::EUR,
                'voting_area' => 8,
                'name' => 'Jeffrey Titford',
                'contact_method' => 'fax',
                'fax' => '+441245252071'
            },
            
            8 => {
                'type' => mySociety::VotingArea::EUR,
                'voting_area' => 8,
                'name' => 'Richard Howitt',
                'contact_method' => 'email',
                'email' => 'richard.howitt@geo2.poptel.org.uk'
            },
            
            9 => {
                'type' => mySociety::VotingArea::EUR,
                'voting_area' => 8,
                'name' => 'Robert Sturdy',
                'contact_method' => 'email',
                'email' => 'rsturdy@europarl.eu.int'
            },
            
            10 => {
                'type' => mySociety::VotingArea::EUR,
                'voting_area' => 8,
                'name' => 'Andrew Duff',
                'contact_method' => 'email',
                'email' => 'mep@andrewduffmep.org'
            },
            
            11 => {
                'type' => mySociety::VotingArea::EUR,
                'voting_area' => 8,
                'name' => 'Christopher Beazley',
                'contact_method' => 'fax',
                'fax' => '+441920485805'
            },
            
            12 => {
                'type' => mySociety::VotingArea::EUR,
                'voting_area' => 8,
                'name' => 'Tom Wise',
                'contact_method' => 'email',
                'email' => 'ukipeast@globalnet.co.uk'
            }
        );
    
    if (exists($db{$id})) {
        return $db{$id};
    } else {
        return mySociety::DaDem::REP_NOT_FOUND
    }
}

1;
