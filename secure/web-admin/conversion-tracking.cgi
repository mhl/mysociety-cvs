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
        print "<h3>$period</h3>\n";
        foreach my $site (sort keys %$sites) {
            my $adverts = $sites->{$site};
            print "<h4>$site</h4>\n<table><tr><th scope='col'>Advert</th><th>Shown</th><th>Converted</th><th>First</th><th>Last</th></tr>\n";
            foreach my $ad (sort keys %$adverts) {
                my $data = $adverts->{$ad};
                print "<tr><th scope='row'>$ad</th>";
                $data->{1} = 0 unless defined $data->{1};
                my $shown = (defined($data->{0}) ? $data->{0} : 0) + $data->{1};
                print "<td>$shown</td><td>$data->{1}</td><td>$data->{first}</td><td>$data->{last}</td>";
                print "</tr>\n";
            }
            print "</table>\n";
        }
    }
}
