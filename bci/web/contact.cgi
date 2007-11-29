#!/usr/bin/perl -w -I../perllib

# contact.cgi:
# Contact page for FixMyStreet
#
# Copyright (c) 2006 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org. WWW: http://www.mysociety.org
#
# $Id: contact.cgi,v 1.25 2007-11-29 15:56:41 matthew Exp $

use strict;
use Standard;
use CrossSell;
use mySociety::Email;
use mySociety::EmailUtil;
use mySociety::Web qw(ent);
use mySociety::Random qw(random_bytes);

# Main code for index.cgi
sub main {
    my $q = shift;
    print Page::header($q, title=>'Contact Us');
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
    my @vars = qw(name em subject message id);
    my %input = map { $_ => $q->param($_) || '' } @vars;
    my @errors;
    push(@errors, 'Please give your name') unless $input{name} =~ /\S/;
    if ($input{em} !~ /\S/) {
        push(@errors, 'Please give your email');
    } elsif (!mySociety::EmailUtil::is_valid_email($input{em})) {
        push(@errors, 'Please give a valid email address');
    }
    push(@errors, 'Please give a subject') unless $input{subject} =~ /\S/;
    push(@errors, 'Please write a message') unless $input{message} =~ /\S/;
    push(@errors, 'Illegal ID') if $input{id} && $input{id} !~ /^[1-9]\d*$/;
    return contact_page($q, @errors) if @errors;

    (my $message = $input{message}) =~ s/\r\n/\n/g;
    (my $subject = $input{subject}) =~ s/\r|\n/ /g;
    $message .= "\n\n[ Complaint about report $input{id} - "
        . mySociety::Config::get('BASE_URL') . "/?id=$input{id} ]"
        if $input{id};
    my $postfix = '[ Sent by contact.cgi on ' .
        $ENV{'HTTP_HOST'} . '. ' .
        "IP address " . $ENV{'REMOTE_ADDR'} .
        ($ENV{'HTTP_X_FORWARDED_FOR'} ? ' (forwarded from '.$ENV{'HTTP_X_FORWARDED_FOR'}.')' : '') . '. ' .
        ' ]';
    my $email = mySociety::Email::construct_email({
        _body_ => "$message\n\n$postfix",
        From => [$input{em}, $input{name}],
        To => [[mySociety::Config::get('CONTACT_EMAIL'), 'FixMyStreet']],
        Subject => 'FMS message: ' . $subject,
        'Message-ID' => sprintf('<contact-%s-%s@mysociety.org>', time(), unpack('h*', random_bytes(5))),
    });
    my $result = mySociety::EmailUtil::send_email($email, $input{em}, mySociety::Config::get('CONTACT_EMAIL'));
    if ($result == mySociety::EmailUtil::EMAIL_SUCCESS) {
        my $out = $q->p("Thanks for your feedback.  We'll get back to you as soon as we can!");
        $out .= CrossSell::display_advert($input{em}, $input{name});
        return $out;
    } else {
        return $q->p('Failed to send message.  Please try again, or <a href="mailto:' . mySociety::Config::get('CONTACT_EMAIL') . '">email us</a>.');
    }
}

sub contact_page {
    my ($q, @errors) = @_;
    my @vars = qw(name em subject message);
    my %input = map { $_ => $q->param($_) || '' } @vars;
    my %input_h = map { $_ => $q->param($_) ? ent($q->param($_)) : '' } @vars;

    my $out = $q->h1('Contact the team');
    if (@errors) {
        $out .= '<ul id="error"><li>' . join('</li><li>', @errors) . '</li></ul>';
    }
    $out .= '<form method="post">';

    my $id = $q->param('id');
    $id = undef unless $id && $id =~ /^[1-9]\d*$/;
    if ($id) {
        mySociety::DBHandle::configure(
            Name => mySociety::Config::get('BCI_DB_NAME'),
            User => mySociety::Config::get('BCI_DB_USER'),
            Password => mySociety::Config::get('BCI_DB_PASS'),
            Host => mySociety::Config::get('BCI_DB_HOST', undef),
            Port => mySociety::Config::get('BCI_DB_PORT', undef)
        );
        my $p = dbh()->selectrow_hashref(
            'select title,detail,name,anonymous,extract(epoch from created) as created
            from problem where id=?', {}, $id);
        $out .= $q->p('You are reporting the following problem report for being abusive, containing personal information, or similar:');
        $out .= $q->blockquote(
            $q->h2(ent($p->{title})),
            $q->p($q->em(
         'Reported ',
         ($p->{anonymous}) ? 'anonymously' : "by " . ent($p->{name}),
         ' at ' . Page::prettify_epoch($p->{created}),
            )),
            $q->p(ent($p->{detail}))
        );
        $out .= '<input type="hidden" name="id" value="' . $id . '">';
    } else {
        $out .= <<EOF;
<p>Please do <strong>not</strong> report problems through this form; messages go to
the team behind FixMyStreet, not a council. To report a problem,
please <a href="/">go to the front page</a> and follow the instructions.</p>

<p>We'd love to hear what you think about this site. Just fill in the form:</p>
EOF
    }
    $out .= <<EOF;
<fieldset>
<input type="hidden" name="submit_form" value="1">
<div><label for="form_name">Your name:</label>
<input type="text" name="name" id="form_name" value="$input_h{name}" size="30"></div>
<div><label for="form_email">Your&nbsp;email:</label>
<input type="text" name="em" id="form_email" value="$input_h{em}" size="30"></div>
<div><label for="form_subject">Subject:</label>
<input type="text" name="subject" id="form_subject" value="$input_h{subject}" size="30"></div>
<div><label for="form_message">Message:</label>
<textarea name="message" id="form_message" rows="7" cols="60">$input_h{message}</textarea></div>
<div class="checkbox"><input type="submit" value="Post"></div>
</fieldset>
</form>
</div>
EOF
    return $out;
}

