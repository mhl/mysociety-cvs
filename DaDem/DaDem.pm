#!/usr/bin/perl
#
# DaDem.pm:
# DaDem functions, to be called by XMLRPC.
#
# Copyright (c) 2004 UK Citizens Online Democracy. All rights reserved.
# Email: chris@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: DaDem.pm,v 1.1 2004-10-06 15:41:23 chris Exp $
#

package DaDem;

use Data::Dumper;

sub fish () {
    return "soup";
}

=item get_representatives ID

=cut
sub get_representatives ($$) {
    my ($x, $id) = @_;
    my %db = (
            2 => [1],
            4 => [2, 3, 4],
            6 => [5],
            8 => [6, 7, 8, 9, 10, 11, 12]
        );
warn "id = $id, db{$id} = $db{$id}\n";
    if (exists($db{$id})) {
        return $db{$id};
    } else {
        return 1;   # DADEM_UNKNOWN_AREA
    }
}

=item get_representative_info ID

=cut
sub get_representative_info ($$) {
    my ($x, $id) = @_;
warn '$_ = ' . Dumper($id)."\n";
    my %db = (
            1 => {
                type => VotingArea::CED,
                name => 'Maurice Leeke',
                contact_method => 'email',
                email => 'Maurice.Leeke@cambridgeshire.gov.uk'
            },

            2 => {
                'type' => VotingArea::DIW,
                'name' => 'Diane Armstrong',
                'contact_method' => 'email',
                'email' => 'diane_armstrong@tiscali.co.uk'
            },
            
            3 => {
                'type' => VotingArea::DIW,
                'name' => 'Max Boyce',
                'contact_method' => 'email',
                'email' => 'maxboyce@cix.co.uk'
            },
            
            4 => {
                'type' => VotingArea::DIW,
                'name' => 'Ian Nimmo-Smith',
                'contact_method' => 'email',
                'email' => 'ian@monksilver.com'
            },
            
            5 => {
                'type' => VotingArea::WMC,
                'name' => 'Anne Campbell',
                'contact_method' => 'fax',
                'fax' => '+441223311315'
            },
            
            6 => {
                'type' => VotingArea::EUR,
                'name' => 'Geoffrey Van Orden',
                'contact_method' => 'fax',
                'fax' => '+3222849332'
            },
            
            7 => {
                'type' => VotingArea::EUR,
                'name' => 'Jeffrey Titford',
                'contact_method' => 'fax',
                'fax' => '+441245252071'
            },
            
            8 => {
                'type' => VotingArea::EUR,
                'name' => 'Richard Howitt',
                'contact_method' => 'email',
                'email' => 'richard.howitt@geo2.poptel.org.uk'
            },
            
            9 => {
                'type' => VotingArea::EUR,
                'name' => 'Robert Sturdy',
                'contact_method' => 'email',
                'email' => 'rsturdy@europarl.eu.int'
            },
            
            10 => {
                'type' => VotingArea::EUR,
                'name' => 'Andrew Duff',
                'contact_method' => 'email',
                'email' => 'mep@andrewduffmep.org'
            },
            
            11 => {
                'type' => VotingArea::EUR,
                'name' => 'Christopher Beazley',
                'contact_method' => 'fax',
                'fax' => '+441920485805'
            },
            
            12 => {
                'type' => VotingArea::EUR,
                'name' => 'Tom Wise',
                'contact_method' => 'email',
                'email' => 'ukipeast@globalnet.co.uk'
            }
        );
    
    if (exists($db{$id})) {
        return $db{$id};
    } else {
        return 2; # DADEM_REP_NOT_FOUND
    }
}

1;
