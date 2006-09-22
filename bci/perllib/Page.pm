#!/usr/bin/perl
#
# Page.pm:
# Various HTML stuff for the BCI site.
#
# Copyright (c) 2006 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: Page.pm,v 1.13 2006-09-22 17:21:36 matthew Exp $
#

package Page;

use strict;
use Carp;
use CGI::Fast qw(-no_xhtml);
use Error qw(:try);
use mySociety::WatchUpdate;
use mySociety::Web qw(ent NewURL);

sub do_fastcgi {
    my $func = shift;

    try {
        my $W = new mySociety::WatchUpdate();
        while (my $q = new CGI::Fast()) {
            &$func($q);
            $W->exit_if_changed();
        }
    } catch Error::Simple with {
        my $E = shift;
        my $msg = sprintf('%s:%d: %s', $E->file(), $E->line(), $E->text());
        warn "caught fatal exception: $msg";
        warn "aborting";
        ent($msg);
        print "Status: 500\nContent-Type: text/html; charset=iso-8859-1\n\n",
                q(<html><head><title>Sorry! Something's gone wrong.</title></head></html>),
                q(<body>),
                q(<h1>Sorry! Something's gone wrong.</h1>),
                q(<p>Please try again later, or <a href="mailto:team@neighbourhoodfixit.com">email us</a> to let us know.</p>),
                q(<hr>),
                q(<p>The text of the error was:</p>),
                qq(<blockquote class="errortext">$msg</blockquote>),
                q(</body></html);
    };
}

=item header Q TITLE [PARAM VALUE ...]

Return HTML for the top of the page, given the TITLE text and optional PARAMs.

=cut
sub header ($$%) {
    my ($q, $title, %params) = @_;
    
    my %permitted_params = map { $_ => 1 } qw();
    foreach (keys %params) {
        croak "bad parameter '$_'" if (!exists($permitted_params{$_}));
    }

    print $q->header(-charset=>'utf-8');
    my $html = <<EOF;
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="en-gb">
    <head>
        <!--[if lt IE 7.]>
        <script defer type="text/javascript" src="pngfix.js"></script>
	<![endif]-->
        <title>Neighbourhood Fix-It</title>
        <style type="text/css">\@import url("css.css");</style>
    </head>
    <body>
        <h1>Neighbourhood Fix-It</h1>
EOF
    return $html;
}

=item footer Q

=cut
sub footer ($) {
    my ($q) = @_;
    return <<EOF;
<h2 class="v">Navigation</h2>
<ul id="navigation">
<li><a href="/contact">Contact</a>
<li><a href="/faq">FAQ</a>
<li><a href="/about">About</a>
<li><a href="/">Home</a>
</ul>

<p id="footer"></p>

</body>
</html>
EOF
}

=item error_page Q MESSAGE

=cut
sub error_page ($$) {
    my ($q, $message);
    my $html = header($q, "Error")
            . $q->p($message)
            . footer($q);
    print $q->header(-content_length => length($html)), $html;
}

sub compass ($$$) {
    my ($q, $x, $y) = @_;
    my @compass;
    for (my $i=$x-1; $i<=$x+1; $i++) {
        for (my $j=$y-1; $j<=$y+1; $j++) {
            $compass[$i][$j] = NewURL($q, x=>$i, y=>$j);
        }
    }
    return <<EOF;
<table cellpadding="0" cellspacing="0" border="0" id="compass">
<tr valign="bottom">
<td align="right"><a href="${compass[$x-1][$y+1]}"><img src="i/arrow-northwest.gif" alt="NW"></a></td>
<td align="center"><a href="${compass[$x][$y+1]}"><img src="i/arrow-north.gif" vspace="3" alt="N"></a></td>
<td><a href="${compass[$x+1][$y+1]}"><img src="i/arrow-northeast.gif" alt="NE"></a></td>
</tr>
<tr>
<td><a href="${compass[$x-1][$y]}"><img src="i/arrow-west.gif" hspace="3" alt="W"></a></td>
<td align="center"><img src="i/rose.gif" alt=""></a></td>
<td><a href="${compass[$x+1][$y]}"><img src="i/arrow-east.gif" hspace="3" alt="E"></a></td>
</tr>
<tr valign="top">
<td align="right"><a href="${compass[$x-1][$y-1]}"><img src="i/arrow-southwest.gif" alt="SW"></a></td>
<td align="center"><a href="${compass[$x][$y-1]}"><img src="i/arrow-south.gif" vspace="3" alt="S"></a></td>
<td><a href="${compass[$x+1][$y-1]}"><img src="i/arrow-southeast.gif" alt="SE"></a></td>
</tr>
</table>
EOF
}

1;
