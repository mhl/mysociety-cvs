#!/usr/bin/perl -w

# about.cgi:
# About page for Neighbourhood Fix-It
#
# Copyright (c) 2006 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org. WWW: http://www.mysociety.org
#
# $Id: about.cgi,v 1.1 2006-09-25 18:12:56 matthew Exp $

use strict;
require 5.8.0;

# Horrible boilerplate to set up appropriate library paths.
use FindBin;
use lib "$FindBin::Bin/../perllib";
use lib "$FindBin::Bin/../../perllib";
use Page;

# Main code for index.cgi
sub main {
    my $q = shift;
    print Page::header($q, 'About');
    print about_page();
    print Page::footer();
}
Page::do_fastcgi(\&main);

sub about_page {
    my $out = '<div id="relativediv">';
    $out .= <<EOF;
<h1>About this site</h1>
<p>About stuff here</p>
</div>
EOF
    return $out;
}

