#!/usr/bin/perl
#
# DaDem.pm:
# Implementation of DaDem functions, to be called by XMLRPC.
#
# Copyright (c) 2004 UK Citizens Online Democracy. All rights reserved.
# Email: chris@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: DaDem.pm,v 1.7 2004-10-18 10:00:40 francis Exp $
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

# Dummy data, for test purposes.
my %dummy_representatives = (
        2000001 => {
            type => mySociety::VotingArea::CED,
            'voting_area' => 1000002,
            name => 'Jim Tackson',
            contact_method => 'email',
            email => 'jim.tackson@dummy.mysociety.org'
        },

        2000002 => {
            'type' => mySociety::VotingArea::DIW,
            'voting_area' => 1000004,
            'name' => 'Mefan Stagdalinski',
            'contact_method' => 'email',
            'email' => 'mefan.stagdalinksi@dummy.mysociety.org'
        },
        
        2000003 => {
            'type' => mySociety::VotingArea::DIW,
            'voting_area' => 1000004,
            'name' => 'Manno Itchell',
            'contact_method' => 'email',
            'email' => 'manno.itchell@dummy.mysociety.org'
        },
        
        2000004 => {
            'type' => mySociety::VotingArea::DIW,
            'voting_area' => 1000004,
            'name' => 'Gil Phyford',
            'contact_method' => 'email',
            'email' => 'gil.phyford@dummy.mysociety.org'
        },
        
        2000005 => {
            'type' => mySociety::VotingArea::WMC,
            'voting_area' => 1000006,
            'name' => 'Stom Teinberg',
            'contact_method' => 'fax',
            'fax' => '0000000000'
        },
        
        2000006 => {
            'type' => mySociety::VotingArea::EUR,
            'voting_area' => 1000008,
            'name' => 'Lis Chrightfoot',
            'contact_method' => 'fax',
            'fax' => '0000000000'
        },
        
        2000007 => {
            'type' => mySociety::VotingArea::EUR,
            'voting_area' => 1000008,
            'name' => 'Crames Jonin',
            'contact_method' => 'fax',
            'fax' => '0000000000'
        },
        
        2000008 => {
            'type' => mySociety::VotingArea::EUR,
            'voting_area' => 1000008,
            'name' => 'Lom Toosemore',
            'contact_method' => 'email',
            'email' => 'lom.toosemore@dummy.mysociety.org'
        },
        
        2000009 => {
            'type' => mySociety::VotingArea::EUR,
            'voting_area' => 1000008,
            'name' => 'Brike Macken',
            'contact_method' => 'email',
            'email' => 'brike.macken@dummy.mysociety.org'
        },
        
        2000010 => {
            'type' => mySociety::VotingArea::EUR,
            'voting_area' => 1000008,
            'name' => 'Yowena Roung',
            'contact_method' => 'email',
            'email' => 'yowena.roung@dummy.mysociety.org'
        },
        
        2000011 => {
            'type' => mySociety::VotingArea::EUR,
            'voting_area' => 1000008,
            'name' => 'Ancis Frirving',
            'contact_method' => 'fax',
            'fax' => '0000000000'
        },
        
        2000012 => {
            'type' => mySociety::VotingArea::EUR,
            'voting_area' => 1000008,
            'name' => 'Tu Stily',
            'contact_method' => 'email',
            'email' => 'tu.stily@dummy.mysociety.org'
        }
    );

my %dummy_areas;
foreach (keys %dummy_representatives) {
    push(@{$dummy_areas{$dummy_representatives{$_}->{voting_area}}}, $_);
}


=item get_representatives ID

Given the ID of an area, return a list of the representatives returned by that
area, or, on failure, an error code.

=cut
sub get_representatives ($$) {
    my ($x, $id) = @_;

    # Dummy postcode case
    if (exists($dummy_areas{$id})) {
        return $dummy_areas{$id};
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
    if (exists($dummy_representatives{$id})) {
        return $dummy_representatives{$id};
    }

    # Real data case
    if (my ($type, $name, $party, $method, $email, $fax) = dbh()->selectrow_array('select area_type, name, party, method, email, fax from representative where id = ?', {}, $id)) {
        # method 0: either; 1: fax; 2: email
        $method ||= 1 + int(rand(2));
        $method = 2 if ($method == 1 and !defined($fax));
        $method = 1 if ($method == 2 and !defined($email));
        $method = (qw(x fax email))[$method];
        return {
                type => $mySociety::VotingArea::type_to_id{$type},
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

