#!/usr/bin/perl
#
# MaPit.pm:
# Implementation of MaPit functions, to be called by XMLRPC.
#
# Copyright (c) 2004 UK Citizens Online Democracy. All rights reserved.
# Email: chris@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: MaPit.pm,v 1.6 2004-10-18 09:44:21 chris Exp $
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
            name => 'Cambridgeshire County Council'
        },
        1000002 => {
            type => mySociety::VotingArea::CED,
            name => 'West Chesterton ED'
        },
        1000003 => {
            type => mySociety::VotingArea::DIS,
            name => 'Cambridge District Council'
        },
        1000004 => {
            type => mySociety::VotingArea::DIW,
            name => 'West Chesterton Ward'
        },
        1000005 => {
            type => mySociety::VotingArea::WMP,
            name => 'House of Commons'
        },
        1000006 => {
            type => mySociety::VotingArea::WMC,
            name => 'Cambridge'
        },
        1000007 => {
            type => mySociety::VotingArea::EUP,
            name => 'European Parliament'
        },
        1000008 => {
            type => mySociety::VotingArea::EUR,
            name => 'Eastern Euro Region'
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
    if ($pc eq 'zz99zz') {
        my %db = (
                mySociety::VotingArea::CTY , 1000001,
                mySociety::VotingArea::CED , 1000002,
                mySociety::VotingArea::DIS , 1000003,
                mySociety::VotingArea::DIW , 1000004,
                mySociety::VotingArea::WMP , 1000005,
                mySociety::VotingArea::WMC , 1000006,
                mySociety::VotingArea::EUP , 1000007,
                mySociety::VotingArea::EUR , 1000008
            );
        return \%db;
    }

    # Real data

    return mySociety::MaPit::BAD_POSTCODE if ($pc !~ m#^[A-Z]{1,2}[0-9]{1,4}[A-Z]{1,2}$#);

    my $pcid = dbh()->selectrow_array('select id from postcode where postcode = ?', {}, $pc);
    return mySociety::MaPit::POSTCODE_NOT_FOUND if (!$pcid);

    # Also add pseudo-areas.
    return {
            (
                map { $special_cases{$_}->{type} => $_ } keys %special_cases
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
    foreach (qw(type_name attend_prep rep_name rep_name_plural rep_suffix rep_prefix)) {
        no strict 'refs';
        $ret->{$_} = ${"mySociety::VotingArea::$_"}{$ret->{type}};
    }
    return $ret;
}

1;
