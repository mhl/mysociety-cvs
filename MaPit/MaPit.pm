#!/usr/bin/perl
#
# MaPit.pm:
# Implementation of MaPit functions, to be called by XMLRPC.
#
# Copyright (c) 2004 UK Citizens Online Democracy. All rights reserved.
# Email: chris@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: MaPit.pm,v 1.10 2004-10-20 13:43:06 francis Exp $
#

package MaPit;

use strict;

use mySociety::MaPit;
use mySociety::VotingArea;

use DBI;
use DBD::SQLite;

=head1 NAME

MaPit

=head1 DESCRIPTION

Implementation of MaPit

=head1 FUNCTIONS

=over 4

=cut
sub dbh () {
    our $dbh;
    $dbh ||= DBI->connect('dbi:SQLite:dbname=/home/chris/projects/mysociety/MaPit/mapit.sqlite', '', '', { RaiseError => 1, AutoCommit => 0 });
    return $dbh;
}

# Special cases to represent parliaments, assemblies themselves.
use constant DUMMY_ID => 1000000;
my %special_cases = (
        # Enclosing bodies
        900000 => {
            type => mySociety::VotingArea::WMP,
            name => 'House of Commons',
        },
        900001 => {
            type => mySociety::VotingArea::EUP,
            name => 'European Parliament',
        },
     
        # Test data
        1000001 => {
            type => mySociety::VotingArea::CTY,
            name => 'Everyone\'s County Council'
        },
        1000002 => {
            type => mySociety::VotingArea::CED,
            name => 'Chest Westerton ED'
        },
        1000003 => {
            type => mySociety::VotingArea::DIS,
            name => 'Our District Council'
        },
        1000004 => {
            type => mySociety::VotingArea::DIW,
            name => 'Chest Westerton Ward'
        },
        1000005 => {
            type => mySociety::VotingArea::WMP,
            name => 'House of Commons'
        },
        1000006 => {
            type => mySociety::VotingArea::WMC,
            name => 'Your and My Society'
        },
        1000007 => {
            type => mySociety::VotingArea::EUP,
            name => 'European Parliament'
        },
        1000008 => {
            type => mySociety::VotingArea::EUR,
            name => 'Windward Euro Region'
        }
    );

=item get_voting_areas POSTCODE

Return voting area IDs for POSTCODE.

=cut
sub get_voting_areas ($$) {
    my ($x, $pc) = @_;
    
    $pc =~ s/\s+//g;
    $pc = uc($pc);

    # Dummy postcode case
    if ($pc eq 'ZZ99ZZ') {
        return {
                map { $special_cases{$_}->{type} => $_ } keys(%special_cases)
            };
    }

    # Real data
    return mySociety::MaPit::BAD_POSTCODE if ($pc !~ m#^[A-Z]{1,2}[0-9]{1,2}[A-Z]?[0-9]{1,2}[A-Z]{1,2}$#);

    my $pcid = dbh()->selectrow_array('select id from postcode where postcode = ?', {}, $pc);
    return mySociety::MaPit::POSTCODE_NOT_FOUND if (!$pcid);

    # Also add pseudo-areas.
    return {
            (
                map { $special_cases{$_}->{type} => $_ } grep { $_ < DUMMY_ID } keys %special_cases
            ), (
                map { $mySociety::VotingArea::type_to_id{$_->[0]} => $_->[1] } @{
                    dbh()->selectall_arrayref('select type, id from postcode_area, area where postcode_area.area_id = area.id and postcode_area.postcode_id = ?', {}, $pcid)
                }
            )
        };
}

=item get_voting_area_info ID

=cut
sub get_voting_area_info ($$) {
    my ($x, $id) = @_;

    my $ret;
    if (exists($special_cases{$id})) {
        $ret = $special_cases{$id};
    } else {
        # Real data
        my ($type, $name);
        return mySociety::MaPit::AREA_NOT_FOUND unless (($type, $name) = dbh()->selectrow_array('select type, name from area where id = ?', {}, $id));
     
        $ret = {
                name => $name,
                type => $mySociety::VotingArea::type_to_id{$type}
            };
    }

    # Annotate with information about the representative type returned for that area.
    foreach (qw(type_name attend_prep rep_name rep_name_plural
                rep_name_long rep_name_long_plural rep_suffix rep_prefix)) {
        no strict 'refs';
        $ret->{$_} = ${"mySociety::VotingArea::$_"}{$ret->{type}};
    }
    return $ret;
}

1;
