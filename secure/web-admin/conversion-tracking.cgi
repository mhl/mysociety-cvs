#!/usr/bin/perl -w

use strict;
use FindBin;
use lib "$FindBin::Bin/../../perllib";
use lib "$FindBin::Bin/../../track/perllib";
use mySociety::CGIFast;

use Track::Stats;
use Track;

while (my $q = new mySociety::CGIFast()) {
    my %out = Track::Stats::generate();

    print $q->header;
    print $q->h1('Conversion tracking');
    print $q->h2('Live');
    foreach my $period (reverse sort keys %out) {
        my $sites = $out{$period};
        print "$period\n" . '=' x length($period) . "\n\n";
        foreach my $site (sort keys %$sites) {
            my $adverts = $sites->{$site};
            print "$site\n" . '-' x length($site) . "\n\n";
            foreach my $ad (sort keys %$adverts) {
	        my $data = $adverts->{$ad};
                print "$ad : ";
                $data->{1} = 0 unless defined $data->{1};
                my $shown = (defined($data->{0}) ? $data->{0} : 0) + $data->{1};
                print "$shown shown, $data->{1} converted (first $data->{first}, last $data->{last}";
                print "\n";
            }
           print "\n";
        }
    }
}
