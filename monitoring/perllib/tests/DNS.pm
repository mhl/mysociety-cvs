#!/usr/bin/perl
#
# DNS.pm:
# Test that local DNS servers are working.
#
# Copyright (c) 2006 UK Citizens Online Democracy. All rights reserved.
# Email: chris@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: DNS.pm,v 1.6 2012-08-22 14:26:51 ian Exp $
#

package DNS;

use strict;

use Net::DNS;

my @dnsservers = qw(ns0.ukcod.org.uk ns1.ukcod.org.uk);

my @records = (
        [qw(www.pledgebank.com.             A)],
        [qw(ukcod.org.uk.                   MX)],
        [qw(73.247.168.192.in-addr.arpa.    PTR)]
    );

sub email() { return 'serious'; }

sub test () {
    return if !mySociety::Config::get('RUN_EXTRA_SERVERS_TESTS');

    foreach my $dnsserver (@dnsservers) {
        my $dns = new Net::DNS::Resolver(
                        nameservers => [$dnsserver],
                        recurse => 0
                    );
        $dns->tcp_timeout(2);
        $dns->udp_timeout(2);
        foreach my $record (@records) {
            my ($name, $type) = @$record;
            my $r = $dns->search($name, $type);
            # XXX we just check that we get *a* successful response -- we
            # should verify that it's sane too, probably.
            if (!$r) {
                print "$dnsserver: $type $name: no response (timed out?)\n";
            } elsif ($r->header()->rcode() ne 'NOERROR') {
                print "$dnsserver: $type $name: failed; rcode = ", $r->header()->rcode(), "\n";
            }
        }
    }
}

1;
