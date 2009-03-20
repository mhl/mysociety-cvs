#!/usr/bin/perl -w

use strict;
use LWP::Simple;
use CGI;

my $url = $q->param('u');
my $file = get($url);
print "Content-Type: image/png\r\n\r\n$file";

