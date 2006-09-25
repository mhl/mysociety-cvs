#!/usr/bin/perl -w

# contact.cgi:
# Contact page for Neighbourhood Fix-It
#
# Copyright (c) 2006 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org. WWW: http://www.mysociety.org
#
# $Id: contact.cgi,v 1.1 2006-09-25 18:12:56 matthew Exp $

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
    print Page::header($q, 'Contact');
    my $out = '';
    if ($q->param('submit_form')) {
    	$out = contact_submit($q);
    } else {
    	$out = contact_page($q);
    }
    print $out;
    print Page::footer();
}
Page::do_fastcgi(\&main);

sub contact_submit {
    my $q = shift;
    my @vars = qw(name email message);
    my %input = map { $_ => $q->param($_) } @vars;
    my @errors;
    push(@errors, 'Please give your name') unless $input{name};
    push(@errors, 'Please give your name') unless $input{email};
    push(@errors, 'Please write a message') unless $input{message};
    return contact_page($q, @errors) if @errors;

}

sub contact_page {
    my ($q, @errors) = @_;
    my @vars = qw(name email message);
    my %input = map { $_ => $q->param($_) } @vars;
    my %input_h = map { $_ => $q->param($_) ? ent($q->param($_)) : '' } @vars;

    my $out = '<div id="relativediv"> <h1>Contact</h1>';
    if (@errors) {
        $out .= '<ul id="error"><li>' . join('</li><li>', @errors) . '</li></ul>';
    }
    $out .= <<EOF;
<p>We'd love to hear what you think about this site. Just fill in the form:</p>
<form method="post">
<fieldset>
<input type="hidden" name="submit_form" value="1">
<div><label for="form_name">Name:</label>
<input type="text" name="name" id="form_name" value="$input_h{name}" size="30"></div>
<div><label for="form_email">Email:</label>
<input type="text" name="email" id="form_email" value="$input_h{email}" size="30"></div>
<div><label for="form_message">Message:</label>
<textarea name="message" id="form_message" rows="7" cols="30">$input_h{message}</textarea></div>
<div class="checkbox"><input type="submit" value="Post"></div>
</fieldset>
</form>
</div>
EOF
    return $out;
}

