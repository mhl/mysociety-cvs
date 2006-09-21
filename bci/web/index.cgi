#!/usr/bin/perl -w

# index.pl:
# Main code for BCI - not really.
#
# Copyright (c) 2006 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org. WWW: http://www.mysociety.org
#
# $Id: index.cgi,v 1.13 2006-09-21 18:09:20 matthew Exp $

use strict;
require 5.8.0;

# Horrible boilerplate to set up appropriate library paths.
use FindBin;
use lib "$FindBin::Bin/../perllib";
use lib "$FindBin::Bin/../../perllib";
use Error qw(:try);
use LWP::Simple;
use RABX;

use Page;
use mySociety::Config;
BEGIN {
    mySociety::Config::set_file("$FindBin::Bin/../conf/general");
}
use mySociety::MaPit;
mySociety::MaPit::configure();
use mySociety::Web qw(ent NewURL);

# Main code for index.cgi
sub main {
    my $q = shift;

    my $out = '';
    if ($q->param('submit_form')) {
        $out = submit_form($q);
    } elsif ($q->param('map')) {
        $out = display_form($q);
    } elsif ($q->param('pc')) {
        $out = display($q);
    } elsif ($q->param('id')) {
        $out = display_problem($q);
    } else {
        $out = front_page();
    }

    print Page::header($q, '');
    print $out;
    print Page::footer($q);
}
Page::do_fastcgi(\&main);

# Display front page
sub front_page {
    my $error = shift;
    my $out = '';
    $out .= '<p id="error">' . $error . '</p>' if ($error);
    $out .= <<EOF;
<p>Report a problem with refuse, recycling, fly tipping, pest control,
abandoned vechicles, street lighting, graffiti, street cleaning, litter or
similar to your local council. Or view reports other people have made.</p>

<p><strong>This is currently only for Newham and Lewisham Councils</strong></p>

<p>It&rsquo;s very simple:</p>

<ol>
<li>Enter a postcode;
<li>Locate the problem on a high-scale map;
<li>Enter details of the problem;
<li>Submit to your council.
</ol>

<form action="./" method="get">
<p>Enter your postcode: <input type="text" name="pc" value="">
<input type="submit" value="Go">
</form>
EOF
    return $out;
}

sub submit_form {
    my $q = shift;
    return 'foo';
}

sub display_form {
    my $q = shift;
    my ($pin_x, $pin_y, $pin_tile_x, $pin_tile_y);
    my $pc = $q->param('pc');
    my $x_tile = $q->param('x');
    my $y_tile = $q->param('y');
    my $skipped = $q->param('skipped');
    my @ps = $q->param;
    foreach (@ps) {
        ($pin_tile_x, $pin_tile_y, $pin_x) = ($1, $2, $q->param($_)) if /^tile_(\d+)\.(\d+)\.x$/;
        $pin_y = 254 - $q->param($_) if /\.y$/;
    }
    return display($q) unless defined($skipped) || (defined($pin_x) && defined($pin_y));

    my $out = '';
    my $hidden = '';
    $out .= '<h2>Reporting a problem</h2>';
    if ($skipped) {
        $out .= '<p>Please fill in the form below with details of the problem:</p>';
    } else {
        my $py = 508 - ($pin_tile_y - $y_tile)*254 - $pin_y;
        my $px = 508 - ($pin_tile_x - $x_tile)*254 - $pin_x;
        my $easting = 5000/31 * $pin_tile_x + $pin_x/254;
        my $northing = 5000/31 * $pin_tile_y + $pin_y/254;
        $hidden .= '<input type="hidden" name="easting" value="' . $easting . '">
<input type="hidden" name="northing" value="' . $northing . '">';
        $out .= '<p>You have located the problem at the location marked with a yellow pin on the map. If this is not the correct location, simply click on the map again. Please fill in details of the problem below:</p>';
        $out .= display_map($q, $x_tile, $y_tile, 0, 0);
        $out .= display_pin($px, $py, 'yellow');
        $out .= '</p></div>';
    }
    $out .= <<EOF;
<form action="./" method="post" id="report_form">
<input type="hidden" name="submit_form" value="1">
<input type="hidden" name="pc" value="$pc">
$hidden
<div><label for="form_title">Title:</label> <input type="text" value="" name="title" id="form_title" size="30">
<div><label for="form_detail">Details:</label>
<textarea name="detail" id="form_detail" rows="7" cols="30"></textarea>
<div><label for="form_name">Name:</label> <input type="text" value="" name="name" id="form_name" size="30">
<div><label for="form_email">Email:</label> <input type="text" value="" name="email" id="form_email" size="30">
<input type="submit" value="Submit">
</form>
EOF
    return $out;
}

sub display {
    my $q = shift;

    my $pc = $q->param('pc');
    my($error, $lbo, $x, $y, $name);
    try {
        ($lbo, $name, $x, $y) = postcode_check($q, $pc);
    } catch RABX::Error with {
        my $e = shift;
        if ($e->value() == mySociety::MaPit::BAD_POSTCODE
           || $e->value() == mySociety::MaPit::POSTCODE_NOT_FOUND) {
            $error = 'That postcode was not recognised, sorry.';
        } else {
            $error = $e;
        }
    };
    return front_page($error) if ($error);

    my $out = <<EOF;
<h2>$name</h2>
<p>To report a problem, please select the location of it on the map below.
Use the arrows to the left of the map to scroll around.</p>
<p>Or just view existing problems that have already been reported.</p>
EOF

    my $pc_enc = ent($pc);
    $out .= <<EOF;
<form action"=./" method="get">
<input type="hidden" name="map" value="1">
<input type="hidden" name="x" value="$x">
<input type="hidden" name="y" value="$y">
<input type="hidden" name="pc" value="$pc_enc">
<input type="hidden" name="lbo" value="$lbo">
EOF
    $out .= display_map($q, $x, $y, 1, 1);
    $out .= <<EOF;
    <div>
    <h2>Current problems</h2>
    <ul id="current">
EOF
    my %current = (
        1 => 'Broken lamppost',
        2 => 'Shards of glass',
        3 => 'Abandoned car',
    );
    my %fixed = (
        4 => 'Broken lamppost',
        5 => 'Shards of glass',
        6 => 'Abandoned car',
    );
    foreach (sort keys %current) {
        my $px = int(rand(508));
        my $py = int(rand(508));
        $out .= '<li><a href="/?id=' . $_ . '">';
        $out .= display_pin($px, $py);
        $out .= $current{$_};
        $out .= '</a></li>';
    }
    $out .= <<EOF;
    </ul>
    <h2>Recently fixed problems</h2>
    <ul>
EOF
    foreach (sort keys %fixed) {
        $out .= '<li><a href="/?id=' . $_ . '">';
        $out .= $fixed{$_};
        $out .= '</a></li>';
    }
    my $skipurl = NewURL($q, 'map'=>1, skipped=>1);
    $out .= <<EOF;
    </ul>
    </div>
</div>
</form>

<p>If you cannot see a map &ndash; if you have images turned off,
or are using a text only browser, for example &ndash; please
<a href="$skipurl">skip this step</a> and we will ask you
to describe the location of your problem instead.</p>
EOF
    return $out;
}

sub display_pin {
    my ($px, $py, $col) = @_;
    $col = 'red' unless $col;
    return '' if ($px<0 || $px>508 || $py<0 || $py>508);
    return '<img src="/i/pin_'.$col.'.png" alt="Problem" style="top:' . ($py-20) . 'px; right:' . ($px-6) . 'px; position: absolute;">';
}

sub display_problem {
    my $q = shift;

    my $id = $q->param('id');

    my $q_x = $q->param('x') || 0; $q_x += 0;
    my $q_y = $q->param('y') || 0; $q_y += 0;

    # Get all information from database
    my $title = 'Broken lamppost';
    my $desc = 'The bulb has clearly gone. This is a shame, as there are no other lampposts nearby, so the whole area is dark.';
    my $easting = 541120;
    my $northing = 185450;
    my $x = $easting / (5000/31);
    my $y = $northing / (5000/31);
    my $x_tile = $q_x || int($x);
    my $y_tile = $q_y || int($y);

    my $py = 508 - 254 * ($y - $y_tile);
    my $px = 508 - 254 * ($x - $x_tile);

    my $out = '';
    $out .= "<h2>$title</h2>";
    $out .= display_map($q, $x_tile, $y_tile, 0, 1);

    # Display information about problem
    $out .= '<p>';
    $out .= display_pin($px, $py);
    $out .= ent($desc);
    $out .= '</p></div>';

    # Display comments
    $out .= '<h3>Comments</h3>';
    $out .= '<p>Will go here</p>';

    return $out;
}

# display_map Q X Y TYPE COMPASS
# X,Y is bottom left tile of 2x2 grid
# TYPE is 1 if the map is clickable, 0 if not
# COMPASS is 1 to show the compass, 0 to not
sub display_map {
    my ($q, $x, $y, $type, $compass) = @_;
    my $url = mySociety::Config::get('TILES_URL');
    my $tiles = $url . $x . '-' . ($x+1) . ',' . $y . '-' . ($y+1) . '/RABX';
    $tiles = LWP::Simple::get($tiles);
    my $tileids = RABX::unserialise($tiles);
    my $tl = $x . '.' . ($y+1);
    my $tr = ($x+1) . '.' . ($y+1);
    my $bl = $x . '.' . $y;
    my $br = ($x+1) . '.' . $y;
    my $tl_src = $url . $tileids->[0][0];
    my $tr_src = $url . $tileids->[0][1];
    my $bl_src = $url . $tileids->[1][0];
    my $br_src = $url . $tileids->[1][1];

    my $img_type = $type ? '<input type="image"' : '<img';
    my $out = <<EOF;
<div id="relativediv">
    <div id="map">
        $img_type id="2.2" name="tile_$tl" src="$tl_src" style="top:0px; left:0px;">$img_type id="3.2" name="tile_$tr" src="$tr_src" style="top:0px; left:254px;"><br>$img_type id="2.3" name="tile_$bl" src="$bl_src" style="top:254px; left:0px;">$img_type id="3.3" name="tile_$br" src="$br_src" style="top:254px; left:254px;">
    </div>
EOF
    $out .= Page::compass($q, $x, $y) if $compass;
    return $out;
}

# Checks the postcode is in one of the two London boroughs
# and sets default X/Y co-ordinates if not provided in the URI
sub postcode_check {
    my ($q, $pc) = @_;
    my $areas;
    $areas = mySociety::MaPit::get_voting_areas($pc);

    # Check for London Borough
    throw RABX::Error("I'm afraid that postcode isn't in our covered area.", 123456) if (!$areas || !$areas->{LBO});

    # Check for Lewisham or Newham
    my $lbo = $areas->{LBO};
    throw RABX::Error("I'm afraid that postcode isn't in our covered London boroughs.", 123457) unless ($lbo == 2510 || $lbo == 2492);

    my $area_info = mySociety::MaPit::get_voting_area_info($lbo);
    my $name = $area_info->{name};

    my $x = $q->param('x') || 0;
    my $y = $q->param('y') || 0;
    $x += 0;
    $y += 0;
    if (!$x && !$y) {
        my $location = mySociety::MaPit::get_location($pc);
        my $northing = $location->{northing};
        my $easting = $location->{easting};
        $x = int($easting / (5000/31));
        $y = int($northing/ (5000/31));
    }
    return ($lbo, $name, $x, $y);
}

