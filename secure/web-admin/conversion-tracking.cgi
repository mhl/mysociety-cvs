#!/usr/bin/perl -w

use strict;
use FindBin;
use lib "$FindBin::Bin/../../perllib";
use lib "$FindBin::Bin/../../track/perllib";
use mySociety::CGIFast qw(-no_xhtml);
use POSIX qw(mktime strftime);

use Track::Stats;
use Track;

while (my $q = new mySociety::CGIFast()) {
    my %out = Track::Stats::generate();

    my @lt = localtime();
    $lt[5]--;
    my $lastyear = strftime('%Y-%m-%d', @lt);
    open FP, '../../../trackstats.log';
    while (<FP>) {
        chomp;
        my ($date, $site, $ad, $shown_week, $shown_month, $conv_week, $conv_month) = split /;/;
        next if $date le $lastyear;
        $out{$site}{$ad}{year}{0} += $shown_week;
        $out{$site}{$ad}{year}{1} += $conv_week;
    }
    close FP;

    my %current;
    $current{writetothem}{'advert=cheltenhamhfyc0'} = "<h2>Cool! You live in Cheltenham!</h2> <p>We&rsquo;ve got an exciting new free service that works exclusively for people in Cheltenham. Please sign up to help the charity that runs WriteToThem, and to get a sneak preview of our new service.</p>";
    $current{writetothem}{'advert=cheltenhamhfyc1'} = "<h2>Get to know your councillors.</h2> <p>Local councillors are really important, but hardly anyone knows them.  Use our new free service to build a low-effort, long term relationship with your councillor.</p>";
    $current{fixmystreet}{'advert=cheltenhamhfyc0'} = "<h2>Cool! You're interested in Cheltenham!</h2> <p>We've got an exciting new free service that works exclusively for people in Cheltenham. Please sign up to help the charity that runs WriteToThem, and to get a sneak preview of our new service.</p>";
    $current{fixmystreet}{'advert=cheltenhamhfyc1'} = "<h2>Get to know your councillors.</h2> <p>Local councillors are really important, but hardly anyone knows them.  Use our new free service to build a low-effort, long term relationship with your councillor.</p>";

    $current{theyworkforyou}{'advert=twfy-alert-word'} = "<p>Did you know that TheyWorkForYou can also email you when a certain word or phrases is mentioned in parliament? For example, it could mail you when your town is mentioned, or an issue you care about. Don&rsquo;t rely on the newspapers to keep you informed about your interests - find out what&rsquo;s happening straight from the horse&rsquo;s mouth. <a href=\"/alert/\"><strong>Sign up for an email alert</strong></a></p>";
    $current{theyworkforyou}{'advert=twfy-alert-person'} = "<p>Did you know that TheyWorkForYou can also email you when a certain MP or Lord contributes in parliament? Don&rsquo;t rely on the newspapers to keep you informed about someone you&rsquo;re interested in - find out what&rsquo;s happening straight from the horse&rsquo;s mouth. <a href=\"/alert/\"><strong>Sign up for an email alert</strong></a></p>";

    # Find out current WTT ads, bit yucky...
    open (FP, '/data/vhost/www.writetothem.com/mysociety/fyr/phplib/fyr.php');
    my $in_ad = 0;
    while (<FP>) {
        $in_ad = 1 if /\$adverts = array\(/;
        next unless $in_ad;
        last if /^\s*\);\s*$/;
        next unless /^\s*array\('(.*?)', '(.*?)'\),\s*$/;
        $current{writetothem}{"advert=$1"} = $2;
    }
    close FP;
    
    # FixMyStreet
    open (FP, '/data/vhost/www.fixmystreet.com/mysociety/bci/perllib/CrossSell.pm');
    $in_ad = 0;
    while (<FP>) {
        $in_ad = 1 if /\@adverts = /;
        next unless $in_ad;
        last if /^\s*\);\s*$/;
        next unless /^\s*\[\s*'(.*?)', '(.*?)'\s*\],\s*$/;
        $current{fixmystreet}{"advert=$1"} = $2;
    }
    close FP;

    # TheyWorkForYou
    open (FP, '/data/mysociety/twfy/www/includes/easyparliament/alert.php');
    $in_ad = 0;
    while (<FP>) {
        $in_ad = 1 if /\$adverts = array\(/;
        next unless $in_ad;
        last if /^\s*\);\s*$/;
        next unless /^\s*array\('(.*?)', '(.*?)'\),\s*$/;
        $current{theyworkforyou}{"advert=$1"} = $2;
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
    print "<table>\n";
    foreach my $site (sort keys %out) {
        my $adverts = $out{$site};
        my $rowspan = scalar (keys %$adverts) + 2;
        print "<tr><th rowspan=$rowspan valign='top'><h4>$site</h4></th>\n";
        print "<th rowspan=2 valign='bottom' scope='col'>Advert</th>";
        print '<th colspan=3>Shown</th><th colspan=3>Converted</th><th colspan=3>Percentage Conversion</th>';
        print "</tr>\n<tr>" . ('<th>Week</th><th>Month</th><th>Year</th>' x 3) . "</tr>\n";
        foreach my $ad (sort keys %$adverts) {
            my %periods = %{$adverts->{$ad}};
            $periods{week}{1} = 0 unless defined $periods{week}{1};
            $periods{month}{1} = 0 unless defined $periods{month}{1};
            $periods{year}{1} = 0 unless defined $periods{year}{1};
            my $shown_week = (defined($periods{week}{0}) ? $periods{week}{0} : 0) + $periods{week}{1};
            my $shown_month = (defined($periods{month}{0}) ? $periods{month}{0} : 0) + $periods{month}{1};
            my $shown_year = (defined($periods{year}{0}) ? $periods{year}{0} : 0);
            my $pc_week = $shown_week ? int($periods{week}{1}/$shown_week*10000+0.5)/100 : '-';
            my $pc_month = $shown_month ? int($periods{month}{1}/$shown_month*10000+0.5)/100 : '-';
            my $pc_year = $shown_year ? int($periods{year}{1}/$shown_year*10000+0.5)/100 : '-';
            print "<tr><th scope='row' align='right'>";
            if ($current{$site}{$ad}) {
                (my $a = $current{$site}{$ad}) =~ s/'/&apos;/g;
                print "<span title='$a'>";
            }
            print $ad;
            print '</span>' if $current{$site}{$ad};
            print "</th>";
            print "<td align='right'>$shown_week</td><td align='right'>$shown_month</td><td align='right'>$shown_year</td>";
            print "<td align='right'>$periods{week}{1}</td><td align='right'>$periods{month}{1}</td><td align='right'>$periods{year}{1}</td>";
            print "<td align='right'>$pc_week%</td><td align='right'>$pc_month%</td><td align='right'>$pc_year%</td>";
            print "</tr>\n";
        }
    }
    print "</table>\n";
}
