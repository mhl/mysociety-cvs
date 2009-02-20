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
use Getopt::Long;
use mySociety::Config;
use mySociety::MaPit;
BEGIN {
	mySociety::Config::set_file("$FindBin::Bin/../conf/general");
}

# Parameters
# Can be specified on command line, or in a file passed with --config
# with each row of the form "variable: <data>"
# 
# Data needs to be in quotes as we don't want shell escaping at that stage.
#
# Examples
# --config ../conf/oxford-example
# --postcode HP224LY --destination 210021422650 --data "/library/transport/nptdr/sample-bucks/ATCO_040_*.CIF" --size 80000 --px 400 --bandsize 2400 --bandcount 5 --bandcolsep 40 --walkspeed 1 --walktime 3600 --output /home/matthew/public_html/iso
# --postcode BS16QF --destination 9100BRSTPWY --data "/library/transport/nptdr/October\ 2008/Timetable\ Data/CIF/Admin_Area_010/*.CIF" --size 200000 --px 800 --bandsize 2400 --bandcount 5 --bandcolsep 40 --walkspeed 1 --walktime 3600 --output /home/matthew/public_html/iso
# --postcode OX26DR --destination 340002054WES --data "/library/transport/nptdr/October\ 2008/Timetable\ Data/CIF/Admin_Area_340/*.CIF" --size 10000 --px 800 --bandsize 14 --bandcount 255 --bandcolsep 1 --walkspeed 1 --walktime 3600 --output /home/matthew/public_html/iso

my ($postcode, $destination, $size, $px, $data, $bandsize, $bandcount, $bandcolsep, $walkspeed, $walktime, $config, $output);
GetOptions(
    'postcode=s' => \$postcode,
    'destination=s' => \$destination,
    'data=s' => \$data,
    'size=i' => \$size,
    'px=i' => \$px,
    'bandsize=i' => \$bandsize,
    'bandcount=i' => \$bandcount,
    'bandcolsep=i' => \$bandcolsep,
    'walkspeed=i' => \$walkspeed,
    'walktime=i' => \$walktime,
    'config=s' => \$config,
    'output=s' => \$output,
);

if ($config) {
    open(FP, $config) or die "Could not read in config file $config: $!";
    while (<FP>) {
        chomp;
	my ($var, $val) = split /\s*:\s*/;
	eval "\$$var = '$val'";
    }
    close FP;
}

unless ($postcode && $destination && $data && $size && $px && $bandsize && $bandcount && $bandcolsep && $walkspeed && $walktime && $output) {
    print "All options need to be given (so I realise they're not really options, sorry!)\n";
    exit 1;
}

my $f = mySociety::MaPit::get_location($postcode);
my $N = $f->{northing};
my $E = $f->{easting};

my $WW = $E - $size / 2;
my $EE = $E + $size / 2;
my $SS = $N - $size / 2;
my $NN = $N + $size / 2;

my $rect = "$WW $EE $SS $NN";
my $results = "nptdr-$postcode-$size";

`$FindBin::Bin/nptdr-plan $destination $data >$output/$results.txt`;
`cat $output/$results.txt | $FindBin::Bin/transportdirect-journeys-to-grid grid $rect $px $px $walkspeed $walktime > $output/$results-grid`;
`cat $output/$results-grid | $FindBin::Bin/grid-to-ppm field $rect $px $px $bandsize $bandcount $bandcolsep > $output/$results.ppm`;

`convert $output/$results.ppm $output/$results.png`;
#eog $output/$results.png

