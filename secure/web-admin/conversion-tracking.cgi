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
    print "<table>\n";
    foreach my $site (sort keys %out) {
        my $adverts = $out{$site};
        my $rowspan = scalar (keys %$adverts) + 2;
        print "<tr><th rowspan=$rowspan valign='top'><h4>$site</h4></th>\n";
        print "<th rowspan=2 valign='bottom' scope='col'>Advert</th>";
        print '<th colspan=2>Shown</th><th colspan=2>Converted</th><th colspan=2>Percentage Conversion</th><th colspan=2>First</th><th colspan=2>Last</th>';
        print "</tr>\n<tr>" . ('<th>Week</th><th>Month</th>' x 5) . "</tr>\n";
        foreach my $ad (sort keys %$adverts) {
            my %periods = %{$adverts->{$ad}};
            $periods{week}{1} = 0 unless defined $periods{week}{1};
            $periods{month}{1} = 0 unless defined $periods{month}{1};
            my $shown_week = (defined($periods{week}{0}) ? $periods{week}{0} : 0) + $periods{week}{1};
            my $shown_month = (defined($periods{month}{0}) ? $periods{month}{0} : 0) + $periods{month}{1};
            print "<tr><th scope='row'>$ad</th>";
            print "<td>$shown_week</td><td>$shown_month</td>";
	    print "<td>$periods{week}{1}</td><td>$periods{month}{1}</td>";
	    print '<td>' . int($periods{week}{1}/$shown_week*10000+0.5)/100 . '%</td>';
	    print '<td>' . int($periods{month}{1}/$shown_month*10000+0.5)/100 . '%</td>';
	    print "<td>$periods{week}{first}</td><td>$periods{month}{first}</td>";
	    print "<td>$periods{week}{last}</td><td>$periods{month}{last}</td>";
            print "</tr>\n";
        }
    }
    print "</table>\n";
}
