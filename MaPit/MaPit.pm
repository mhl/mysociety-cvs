#!/usr/bin/perl
#
# MaPit.pm:
# Implementation of MaPit functions, to be called by XMLRPC.
#
# Copyright (c) 2004 UK Citizens Online Democracy. All rights reserved.
# Email: chris@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: MaPit.pm,v 1.4 2004-10-17 13:24:56 chris Exp $
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

=item get_voting_areas POSTCODE

Return voting area IDs for POSTCODE.

=cut
sub get_voting_areas ($$) {
    my ($x, $pc) = @_;
    
    $pc =~ s/\s+//g;
    $pc = uc($pc);

    return mySociety::MaPit::BAD_POSTCODE if ($pc !~ m#^[A-Z]{1,2}[0-9]{1,4}[A-Z]{1,2}$#);

    my $pcid = dbh()->selectrow_array('select id from postcode where postcode = ?', {}, $pc);
    return mySociety::MaPit::POSTCODE_NOT_FOUND if (!$pcid);

    return {
            map { $_->[0] => $_->[1] } @{
                    dbh()->selectall_arrayref('select type, id from postcode_area, area where postcode_area.area_id = area.id and postcode_area.postcode_id = ?', {}, $pcid)
                }
        };
}

=item get_voting_area_info ID

=cut
sub get_voting_area_info ($$) {
    my ($x, $id) = @_;

    my ($type, $name);
    return mySociety::MaPit::AREA_NOT_FOUND unless (($type, $name) = dbh()->selectrow_array('select type, name from area where id = ?', {}, $id));
 
    my $ret = {
            name => $name,
            type => $mySociety::VotingArea::type_to_id{$type}
        };

    # Annotate with information about the representative type returned for that area.
    foreach (qw(type_name attend_prep rep_name rep_name_plural rep_suffix rep_prefix)) {
        no strict 'refs';
        $ret->{$_} = ${"mySociety::VotingArea::$_"}{$ret->{type}};
    }
    return $ret;
}

1;
