#!/usr/bin/perl
#
# do-nptdr.pl:
# Generate diagram of time travel to arrive by a certain time by public
# transport using NPTDR.
#
# Copyright (c) 2008 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#

use warnings;
use strict;
use FindBin;
use lib "$FindBin::Bin/../../perllib";
use mySociety::Config;
use mySociety::MaPit;
BEGIN {
	mySociety::Config::set_file("$FindBin::Bin/../conf/general");
}

# Parameters
my $postcode = 'BS16QF';
my $destination = '9100BRSPKWY';
#my $postcode = 'HP224LY';
my $size_m = 80000; # length in metres of sides of rectangle round postcode
my $size_px = 400;
my $dir = '/home/matthew/toobig/nptdr/gen';
#BANDSIZE=60; bandcount=200; bandcolsep=1
my $bandsize = 2400;
my $bandcount = 5;
my $bandcolsep = 40;
my $walkspeed = 1; # m/s (1)
my $walktime = 3600; # sec (900)

my $f = mySociety::MaPit::get_location($postcode);
my $N = $f->{northing};
my $E = $f->{easting};

my $WW = $E - $size_m / 2;
my $EE = $E + $size_m / 2;
my $SS = $N - $size_m / 2;
my $NN = $N + $size_m / 2;

my $rect = "$WW $EE $SS $NN";
my $results = "nptdr-$postcode-$size_m";

#./nptdr-plan 210021422650 /library/transport/nptdr/sample-bucks/ATCO_040_*.CIF >$dir/$results
`$FindBin::Bin/nptdr-plan $destination /home/matthew/ATCO_010_*.CIF >$dir/$results`;

`cat $dir/$results | $FindBin::Bin/transportdirect-journeys-to-grid grid $rect $size_px $size_px $walkspeed $walktime > $dir/$results-grid`;
`cat $dir/$results-grid | $FindBin::Bin/grid-to-ppm field $rect $size_px $size_px $bandsize $bandcount $bandcolsep > $dir/$results.ppm`;

`convert $dir/$results.ppm $dir/$results.png`;
#eog $dir/$results.png

