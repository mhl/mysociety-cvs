#!/usr/bin/perl
#
# DaDem.pm:
# Implementation of DaDem functions, to be called by XMLRPC.
#
# Copyright (c) 2004 UK Citizens Online Democracy. All rights reserved.
# Email: chris@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: DaDem.pm,v 1.5 2004-10-18 09:24:56 francis Exp $
#

package DaDem;

use strict;
use mySociety::DaDem;
use mySociety::VotingArea;

use DBI;
use DBD::SQLite;

=head1 NAME

DaDem

=head1 DESCRIPTION

Implementation of DaDem.

=head1 FUNCTIONS

=over 4

=cut
sub dbh () {
    our $dbh;
    $dbh ||= DBI->connect('dbi:SQLite:dbname=/home/chris/projects/mysociety/MaPit/dadem.sqlite', '', '', { RaiseError => 1, AutoCommit => 0 });
    return $dbh;
}

=item get_representatives ID

Given the ID of an area, return a list of the representatives returned by that
area, or, on failure, an error code.

=cut
sub get_representatives ($$) {
    my ($x, $id) = @_;

    # Dummy postcode case
    if ($id >= 1000001 && $id <= 1000008) {
        my %db = (
                1000002 => [2000001],
                1000004 => [2000002, 2000003, 2000004],
                1000006 => [2000005],
                1000008 => [2000006, 2000007, 2000008, 2000009, 2000010, 2000011, 2000012]
            );
        return $db{$id};
    }

    # Real data
    my $y = dbh()->selectall_arrayref('select id from representative where area_id = ?', {}, $id);
    if (!$y) {
        return mySociety::DaDem::UNKNOWN_AREA;
    } else {
        return [ map { $_->[0] } @$y ];
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
    
    # Dummy postcode case
    if ($id >= 2000001 && $id <= 2000008) {
        my %db = (
            2000001 => {
                type => mySociety::VotingArea::CED,
                'voting_area' => 1000002,
                name => 'Maurice Leeke',
                contact_method => 'email',
                email => 'Maurice.Leeke@cambridgeshire.gov.uk'
            },

            2000002 => {
                'type' => mySociety::VotingArea::DIW,
                'voting_area' => 1000004,
                'name' => 'Diane Armstrong',
                'contact_method' => 'email',
                'email' => 'diane_armstrong@tiscali.co.uk'
            },
            
            2000003 => {
                'type' => mySociety::VotingArea::DIW,
                'voting_area' => 1000004,
                'name' => 'Max Boyce',
                'contact_method' => 'email',
                'email' => 'maxboyce@cix.co.uk'
            },
            
            2000004 => {
                'type' => mySociety::VotingArea::DIW,
                'voting_area' => 1000004,
                'name' => 'Ian Nimmo-Smith',
                'contact_method' => 'email',
                'email' => 'ian@monksilver.com'
            },
            
            2000005 => {
                'type' => mySociety::VotingArea::WMC,
                'voting_area' => 1000006,
                'name' => 'Anne Campbell',
                'contact_method' => 'fax',
                'fax' => '+441223311315'
            },
            
            2000006 => {
                'type' => mySociety::VotingArea::EUR,
                'voting_area' => 1000008,
                'name' => 'Anne Campbell',
                'name' => 'Geoffrey Van Orden',
                'contact_method' => 'fax',
                'fax' => '+3222849332'
            },
            
            2000007 => {
                'type' => mySociety::VotingArea::EUR,
                'voting_area' => 1000008,
                'name' => 'Jeffrey Titford',
                'contact_method' => 'fax',
                'fax' => '+441245252071'
            },
            
            2000008 => {
                'type' => mySociety::VotingArea::EUR,
                'voting_area' => 1000008,
                'name' => 'Richard Howitt',
                'contact_method' => 'email',
                'email' => 'richard.howitt@geo2.poptel.org.uk'
            },
            
            2000009 => {
                'type' => mySociety::VotingArea::EUR,
                'voting_area' => 1000008,
                'name' => 'Robert Sturdy',
                'contact_method' => 'email',
                'email' => 'rsturdy@europarl.eu.int'
            },
            
            2000010 => {
                'type' => mySociety::VotingArea::EUR,
                'voting_area' => 1000008,
                'name' => 'Andrew Duff',
                'contact_method' => 'email',
                'email' => 'mep@andrewduffmep.org'
            },
            
            2000011 => {
                'type' => mySociety::VotingArea::EUR,
                'voting_area' => 1000008,
                'name' => 'Christopher Beazley',
                'contact_method' => 'fax',
                'fax' => '+441920485805'
            },
            
            2000012 => {
                'type' => mySociety::VotingArea::EUR,
                'voting_area' => 1000008,
                'name' => 'Tom Wise',
                'contact_method' => 'email',
                'email' => 'ukipeast@globalnet.co.uk'
            }
        );
        return $db{$id};
    }

    # Real data case
    if (my ($name, $party, $method, $email, $fax) = dbh()->selectrow_array('select name, party, method, email, fax from representative where id = ?', {}, $id)) {
        # method 0: either; 1: fax; 2: email
        $method ||= 1 + int(rand(2));
        $method = 2 if ($method == 1 and !defined($fax));
        $method = 1 if ($method == 2 and !defined($email));
        $method = (qw(x fax email))[$method];
        return {
                name => $name,
                party => $party,
                method => $method,
                email => $email,
                fax => $fax
            };
    } else {
        return mySociety::DaDem::REP_NOT_FOUND
    }
}

1;

