#!/usr/bin/perl

use strict;
use warnings;

sub say($) {
    print $_[0] . "\n";
}

my $dir = '/etc/exim4/virtual';

my (@cron, @clientsupport);

while (my $f = <$dir/*>) {
    (my $domain = $f) =~ s{^.*/}{};
    next unless (-f $f) && (! -l $f);
    open(FP, $f) or die $!;
    while (<FP>) {
        s/\@mysociety.org//g;
        s/([a-z]*)\@[a-z.]*/<abbr title="$&">$1<\/abbr>/g;
        push @cron, $_ if /^cron-/;
        if (/^clientsupport/) {
            s/^.*?: *//;
            push @clientsupport, "<strong>$domain</strong>: $_";
        }
    }
    close FP;
}

print <<EOF;
Content-type: text/html

<html>
<head><title>Support emails</title>
<style>
	\@import url('https://secure.mysociety.org/intranet/pub/TWiki/PatternSkin/style.css');
	\@import url('https://secure.mysociety.org/intranet/pub/TWiki/PatternSkin/colors.css');
	tr:hover { background-color: #ffff99; }
abbr { border-bottom: dotted 1px black; }
table { border-collapse: collapse; }
td, th { border: solid 1px #aa0000; border-width: 1px 0; padding: 0.25em; margin: 0; text-align: left; }
tr:first-child th, tr:first-child td { border-top: 0; }
table.cron td:nth-child(2) { background-color: #ff9999; }
tr:last-child td { border-bottom: 0; }
tr td:first-child, tr th:first-child { border-left: 0; }
tr td:last-child, tr th:last-child { border-right: 0; }
</style>
</head>
<body class="patternViewPage">
<div id="patternPage">
<div id="patternMainContents">
<div id="patternContent">
<div id="patternTopic">
<h3>clientsupport@</h3>
<table>
EOF

foreach (sort @clientsupport) {
    my @cols = split /[:,]/, $_, 4;
    say "<tr><td>" . join("</td><td>", @cols) . "</td></tr>";
}
print <<EOF;
</table>

<h3>cron-*@</h3>
<table class='cron'>
<tr><th>Email</th><th>Primary</th><th>Secondary</th><th>Others</th></tr>
EOF

foreach (sort @cron) {
    my @cols = split /[:,]/, $_, 4;
    @cols = (@cols, "", "")[0..3];
    say "<tr><td>" . join("</td><td>", @cols) . "</td></tr>";
}
say "</table>";

print "</div></div></div></div></body></html>";

