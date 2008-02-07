#!/usr/bin/perl -w

use strict;
use FindBin;
use lib "$FindBin::Bin/../../perllib";
use lib "$FindBin::Bin/../../track/perllib";
use mySociety::CGIFast qw(-no_xhtml);

use Track::Stats;
use Track;

while (my $q = new mySociety::CGIFast()) {
    my %out = Track::Stats::generate();

    # Find out current WTT ads, bit yucky...
    open (FP, '/data/vhost/www.writetothem.com/mysociety/fyr/phplib/fyr.php');
    my $in_ad = 0;
    my $c = 0;
    my %current;
    while (<FP>) {
        $in_ad = 1 if /crosssell_display_advert\(/;
        next unless $in_ad;
        last if /^\s*\)\s*$/;
        next unless /^\s*array\('(.*?)', '(.*?)'\),\s*$/;
        $current{writetothem}{"advert=$1$c"} = $2;
        $c++;
    }
    close FP;
    
    # FixMyStreet
    open (FP, '/data/vhost/www.fixmystreet.com/mysociety/bci/perllib/CrossSell.pm');
    $in_ad = 0;
    $c = 0;
    while (<FP>) {
        $in_ad = 1 if /\@adverts = /;
        next unless $in_ad;
        last if /^\s*\);\s*$/;
        next unless /^\s*\[\s*'(.*?)', '(.*?)'\s*\],\s*$/;
        $current{fixmystreet}{"advert=$1$c"} = $2;
        $c++;
    }
    close FP;

    # TheyWorkForYou
    open (FP, '/data/mysociety/twfy/www/includes/easyparliament/alert.php');
    $in_ad = 0;
    $c = 0;
    while (<FP>) {
        $in_ad = 1 if /\$adverts = array\(/;
        next unless $in_ad;
        last if /^\s*\);\s*$/;
        next unless /^\s*array\('(.*?)', '(.*?)'\),\s*$/;
        $current{theyworkforyou}{"advert=$1$c"} = $2;
        $c++;
    }
    close FP;

    print $q->header;
    print $q->start_html(
        -title => 'mySociety Conversion tracking',
        -style => { src => '/track/track.css' },
        -encoding => 'utf-8'
    ) . <<EOF
<div id="masthead"><img src="/track/mslogo.gif" alt="mySociety.org"></div>
<div id="content">
EOF
        . $q->h1('Conversion tracking');
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
            my $pc_week = $shown_week ? int($periods{week}{1}/$shown_week*10000+0.5)/100 : '-';
            my $pc_month = $shown_month ? int($periods{month}{1}/$shown_month*10000+0.5)/100 : '-';
            print "<tr><th scope='row'>";
            print "<span title='$current{$site}{$ad}'>" if $current{$site}{$ad};
            print $ad;
            print '</span>' if $current{$site}{$ad};
            print "</th>";
            print "<td>$shown_week</td><td>$shown_month</td>";
            print "<td>$periods{week}{1}</td><td>$periods{month}{1}</td>";
            print '<td>' . $pc_week . '%</td>';
            print '<td>' . $pc_month . '%</td>';
            print $q->td(defined $periods{week}{first} ? $periods{week}{first} : '');
            print $q->td(defined $periods{month}{first} ? $periods{month}{first} : '');
            print $q->td(defined $periods{week}{last} ? $periods{week}{last} : '');
            print $q->td(defined $periods{month}{last} ? $periods{month}{last} : '');
            print "</tr>\n";
        }
    }
    print "</table>\n";
    print $q->h2('Historical');
    print $q->p('TODO');
}
