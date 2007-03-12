#!/usr/bin/perl -w

# contact.cgi:
# Contact page for Neighbourhood Fix-It
#
# Copyright (c) 2006 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org. WWW: http://www.mysociety.org
#
# $Id: contact.cgi,v 1.10 2007-03-12 16:42:20 matthew Exp $

use strict;
require 5.8.0;

# Horrible boilerplate to set up appropriate library paths.
use FindBin;
use lib "$FindBin::Bin/../perllib";
use lib "$FindBin::Bin/../../perllib";
use Page;
use mySociety::Config;
use mySociety::Email;
use mySociety::Util;
use mySociety::Web qw(ent);

BEGIN {
    mySociety::Config::set_file("$FindBin::Bin/../conf/general");
}

# Main code for index.cgi
sub main {
    my $q = shift;
    print Page::header($q, 'Contact Us');
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
    my @vars = qw(name email subject message);
    my %input = map { $_ => $q->param($_) || '' } @vars;
    my @errors;
    push(@errors, 'Please give your name') unless $input{name} =~ /\S/;
    if ($input{email} !~ /\S/) {
        push(@errors, 'Please give your email');
    } elsif (!mySociety::Util::is_valid_email($input{email})) {
        push(@errors, 'Please give a valid email address');
    }
    push(@errors, 'Please give a subject') unless $input{subject} =~ /\S/;
    push(@errors, 'Please write a message') unless $input{message} =~ /\S/;
    return contact_page($q, @errors) if @errors;

    (my $message = $input{message}) =~ s/\r\n/\n/g;
    (my $subject = $input{subject}) =~ s/\r|\n/ /g;
    my $postfix = '[ Sent by contact.cgi on ' .
        $ENV{'HTTP_HOST'} . '. ' .
        "IP address " . $ENV{'REMOTE_ADDR'} .
        ($ENV{'HTTP_X_FORWARDED_FOR'} ? ' (forwarded from '.$ENV{'HTTP_X_FORWARDED_FOR'}.')' : '') . '. ' .
        ' ]';
    my $email = mySociety::Email::construct_email({
        _body_ => "$message\n\n$postfix",
        From => [$input{email}, $input{name}],
        To => [[mySociety::Config::get('CONTACT_EMAIL'), 'Neighbourhood Fix-It']],
        Subject => 'NFI message: ' . $subject
    });
    my $result = mySociety::Util::send_email($email, $input{email}, mySociety::Config::get('CONTACT_EMAIL'));
    if ($result == mySociety::Util::EMAIL_SUCCESS) {
        return $q->p("Thanks for your feedback.  We'll get back to you as soon as we can!");
    } else {
        return $q->p('Failed to send message.  Please try again, or <a href="mailto:' . mySociety::Config::get('CONTACT_EMAIL') . '">email us</a>.');
    }
}

sub contact_page {
    my ($q, @errors) = @_;
    my @vars = qw(name email subject message);
    my %input = map { $_ => $q->param($_) || '' } @vars;
    my %input_h = map { $_ => $q->param($_) ? ent($q->param($_)) : '' } @vars;

    my $out = $q->h1('Contact the team');
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
<div><label for="form_subject">Subject:</label>
<input type="text" name="subject" id="form_subject" value="$input_h{subject}" size="30"></div>
<div><label for="form_message">Message:</label>
<textarea name="message" id="form_message" rows="7" cols="30">$input_h{message}</textarea></div>
<div class="checkbox"><input type="submit" value="Post"></div>
</fieldset>
</form>
</div>
EOF
    return $out;
}

