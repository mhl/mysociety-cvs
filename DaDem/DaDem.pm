#!/usr/bin/perl
#
# DaDem.pm:
# Implementation of DaDem functions, to be called by XMLRPC.
#
# Copyright (c) 2004 UK Citizens Online Democracy. All rights reserved.
# Email: chris@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: DaDem.pm,v 1.4 2004-10-17 13:24:56 chris Exp $
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
