#!/usr/bin/perl
#
# MaPit.pm:
# Implementation of MaPit functions, to be called by XMLRPC.
#
# Copyright (c) 2004 UK Citizens Online Democracy. All rights reserved.
# Email: chris@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: MaPit.pm,v 1.2 2004-10-15 16:35:47 francis Exp $
#

package MaPit;

use strict;
use mySociety::MaPit;
use mySociety::VotingArea;

=head1 NAME

MaPit

=head1 DESCRIPTION

Implementation of MaPit

=head1 FUNCTIONS

=over 4

=item get_voting_areas POSTCODE

=cut
sub get_voting_areas ($$) {
    my ($x, $pc) = @_;
    $pc =~ s/\s+//g;
    $pc = uc($pc);
    if ($pc !~ m#^[A-Z]{1,2}[0-9]{1,4}[A-Z]{1,2}$#) { # XXX
        return mySociety::MaPit::BAD_POSTCODE;
    } elsif ($pc eq 'CB41XP') {
        my %db = (
                mySociety::VotingArea::CTY , 1,
                mySociety::VotingArea::CED , 2,
                mySociety::VotingArea::DIS , 3,
                mySociety::VotingArea::DIW , 4,
                mySociety::VotingArea::WMP , 5,
                mySociety::VotingArea::WMC , 6,
                mySociety::VotingArea::EUP , 7,
                mySociety::VotingArea::EUR , 8
            );
        return \%db;
    } else {
        return mySociety::MaPit::POSTCODE_NOT_FOUND;
    }
}

=item get_voting_area_info ID

=cut
sub get_voting_area_info ($$) {
    my ($x, $id) = @_;

    my %db = (
            1 => {'type' => mySociety::VotingArea::CTY, 'name' => 'Cambridgeshire County Council'},
            2 => {'type' => mySociety::VotingArea::CED, 'name' => 'West Chesterton ED'},
            3 => {'type' => mySociety::VotingArea::DIS, 'name' => 'Cambridge District Council'},
            4 => {'type' => mySociety::VotingArea::DIW, 'name' => 'West Chesterton Ward'},
            5 => {'type' => mySociety::VotingArea::WMP, 'name' => 'House of Commons'},
            6 => {'type' => mySociety::VotingArea::WMC, 'name' => 'Cambridge'},
            7 => {'type' => mySociety::VotingArea::EUP, 'name' => 'European Parliament'},
            8 => {'type' => mySociety::VotingArea::EUR, 'name' => 'Eastern Euro Region'}
        );

    if (exists($db{$id})) {
        $db{$id}{'type_name'} = $mySociety::VotingArea::name{$db{$id}{'type'}};
        $db{$id}{'attend_prep'} = $mySociety::VotingArea::attend_prep{$db{$id}{'type'}};
        $db{$id}{'rep_name'} = $mySociety::VotingArea::rep_name{$db{$id}{'type'}};
        $db{$id}{'rep_name_plural'} = $mySociety::VotingArea::rep_name_plural{$db{$id}{'type'}};
        $db{$id}{'rep_suffix'} = $mySociety::VotingArea::rep_suffix{$db{$id}{'type'}};
        $db{$id}{'rep_prefix'} = $mySociety::VotingArea::rep_prefix{$db{$id}{'type'}};

        return $db{$id};
    } else {
        return mySociety::MaPit::AREA_NOT_FOUND;
    }
}

1;
