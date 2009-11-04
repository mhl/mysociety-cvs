#!/usr/bin/perl -w -I../perllib

# confirm.cgi:
# Confirmation code for FixMyStreet
#
# Copyright (c) 2006 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org. WWW: http://www.mysociety.org
#
# $Id: confirm.cgi,v 1.59 2009-11-04 16:28:16 matthew Exp $

use strict;
use Standard;
use Digest::SHA1 qw(sha1_hex);
use CrossSell;
use mySociety::Alert;
use mySociety::AuthToken;
use mySociety::Random qw(random_bytes);

sub main {
    my $q = shift;

    my $out = '';
    my $extra;
    my $token = $q->param('token');
    my $type = $q->param('type') || '';
    my $tokentype = $type eq 'questionnaire' ? 'update' : $type;
    my $data = mySociety::AuthToken::retrieve($tokentype, $token);
    if ($data) {
        if ($type eq 'update') {
            $out = confirm_update($q, $data);
        } elsif ($type eq 'problem') {
            $out = confirm_problem($q, $data);
            $extra = 'added-problem';
        } elsif ($type eq 'questionnaire') {
            $out = add_questionnaire($q, $data, $token);
        }
        dbh()->commit();
    } else {
        $out = $q->p(_(<<EOF));
Thank you for trying to confirm your update or problem. We seem to have an
error ourselves though, so <a href="/contact">please let us know what went on</a>
and we'll look into it.
EOF
    }

    print Page::header($q, title=>_('Confirmation'));
    print $out;
    print Page::footer($q, extra => $extra);
}
Page::do_fastcgi(\&main);

sub confirm_update {
    my ($q, $data) = @_;
    my $cobrand = Page::get_cobrand($q);
    my $id = $data;
    my $add_alert = 0;
    if (ref($data)) {
        $id = $data->{id};
        $add_alert = $data->{add_alert};
    }

    my ($problem_id, $fixed, $email, $name, $cobrand_data) = dbh()->selectrow_array(
        "select problem_id, mark_fixed, email, name, cobrand_data from comment where id=?", {}, $id);
    $email = lc($email);

    (my $domain = $email) =~ s/^.*\@//;
    if (dbh()->selectrow_array('select email from abuse where lower(email)=? or lower(email)=?', {}, $email, $domain)) {
        dbh()->do("update comment set state='hidden' where id=?", {}, $id);
        return $q->p('Sorry, there has been an error confirming your update.');
    } else {
        dbh()->do("update comment set state='confirmed' where id=? and state='unconfirmed'", {}, $id);
    }

    my $creator_fixed = 0;
    if ($fixed) {
        dbh()->do("update problem set state='fixed', lastupdate = ms_current_timestamp()
            where id=? and state='confirmed'", {}, $problem_id);
        # If a problem reporter is marking their own problem as fixed, turn off questionnaire sending
        $creator_fixed = dbh()->do("update problem set send_questionnaire='f' where id=? and lower(email)=?
            and send_questionnaire='t'", {}, $problem_id, $email);
    } else { 
        # Only want to refresh problem if not already fixed
        dbh()->do("update problem set lastupdate = ms_current_timestamp()
            where id=? and state='confirmed'", {}, $problem_id);
    }

    my $out = '';
    if ($creator_fixed > 0 && $q->{site} ne 'emptyhomes') {
        my $answered_ever_reported = dbh()->selectrow_array(
            'select id from questionnaire where problem_id in (select id from problem where lower(email)=?) and ever_reported is not null', {}, $email);
        if (!$answered_ever_reported) {
            $out = ask_questionnaire($q->param('token'), $q);
        }
    }

    my $report_url = Cobrand::url($cobrand, "/report/$problem_id#update_$id", $q);
    if (!$out) {
        $out = $q->p({class => 'confirmed'}, sprintf(_('You have successfully confirmed your update and you can now <a href="%s">view it on the site</a>.'), $report_url));
        $out .= CrossSell::display_advert($q, $email, $name);
    }

    # Subscribe updater to email updates if requested
    if ($add_alert) {
        my $alert_id = mySociety::Alert::create($email, 'new_updates', $cobrand, $cobrand_data, $problem_id);
        mySociety::Alert::confirm($alert_id);
    }

    return $out;
}

sub confirm_problem {
    my ($q, $id) = @_;
    my $cobrand = Page::get_cobrand($q);
    my ($council, $email, $name, $cobrand_data) = dbh()->selectrow_array("select council, email, name, cobrand_data from problem where id=?", {}, $id);

    (my $domain = $email) =~ s/^.*\@//;
    if (dbh()->selectrow_array('select email from abuse where lower(email)=? or lower(email)=?', {}, lc($email), lc($domain))) {
        dbh()->do("update problem set state='hidden', lastupdate=ms_current_timestamp() where id=?", {}, $id);
        return $q->p(_('Sorry, there has been an error confirming your problem.'));
    } else {
        dbh()->do("update problem set state='confirmed', confirmed=ms_current_timestamp(), lastupdate=ms_current_timestamp()
            where id=? and state='unconfirmed'", {}, $id);
    }
    my $out;
    if ($q->{site} eq 'emptyhomes') {
        if ($council) {
            $out = $q->p(_('Thank you for reporting an empty property on
ReportEmptyHomes.com. We have emailed the empty property officer in the council
responsible with the details and asked them to do whatever they can to get the
empty property back into use as soon as possible.')) .
$q->p(_('Most councils are quite good at bringing empty properties back into use. Even
so the process can sometimes be slow, especially if the property is in very poor
repair or the owner is unwilling to act. In most cases it takes six months
before you can expect to see anything change. This doesn&rsquo;t mean the council
isn&rsquo;t doing anything. We encourage councils to update the website so you can
see what is happening.')) . 
$q->p(_('We will contact you again in a month and again after six months to ask what has
happened. Hopefully the property will be well on the way to being brought back
into use by then, but if not we can offer advice on what you can do next.')) .
$q->p(_('Thank you for using ReportEmptyHomes.com. Your action is already helping
to resolve the UK&rsquo;s empty homes crisis.')) .
$q->p('<a href="/report/' . $id . '">' . _('View your report') . '</a>.');
        } else {
            $out = $q->p(_('Thank you for reporting an empty property on ReportEmptyHomes.com.')) .
$q->p('<a href="/report/' . $id . '">' . _('View your report') . '</a>.');
        }
    } else {
        my $report_url = Cobrand::url($cobrand, "/report/$id", $q);
        $out = $q->p({class => 'confirmed'},
            _('You have successfully confirmed your problem')
            . ($council ? _(' and <strong>we will now send it to the council</strong>') : '')
            . sprintf(_('. You can <a href="%s">view the problem on this site</a>.'), $report_url)
        );
        $out .= CrossSell::display_advert($q, $email, $name);
        my %vars = (
            url_report => $report_url,
            url_home => Cobrand::url($cobrand, '/', $q),
        );
        my $cobrand_page = Page::template_include('confirmed-problem', $q, Page::template_root($q), %vars);
        $out = $cobrand_page if $cobrand_page;
    }

    # Subscribe problem reporter to email updates
    my $alert_id = mySociety::Alert::create($email, 'new_updates', $cobrand, $cobrand_data, $id);
    mySociety::Alert::confirm($alert_id);

    return $out;
}

sub ask_questionnaire {
    my ($token, $q) = @_;
    my $cobrand = Page::get_cobrand($q);
    my $qn_thanks = _("Thanks, glad to hear it's been fixed! Could we just ask if you have ever reported a problem to a council before?");
    my $yes = _('Yes');
    my $no = _('No');
    my $go = _('Go');
    my $form_action = Cobrand::url($cobrand, "/confirm", $q);
    my $out = <<EOF;
<form action="$form_action" method="post" id="questionnaire">
<input type="hidden" name="type" value="questionnaire">
<input type="hidden" name="token" value="$token">
<p>$qn_thanks</p>
<p align="center">
<input type="radio" name="reported" id="reported_yes" value="Yes">
<label for="reported_yes">$yes</label>
<input type="radio" name="reported" id="reported_no" value="No">
<label for="reported_no">$no</label>
<input type="submit" value="$go">
</p>
</form>
EOF
    return $out;
}

sub add_questionnaire {
    my ($q, $data, $token) = @_;

    my $id = $data;
    if (ref($data)) {
        $id = $data->{id};
    }
    my $cobrand = Page::get_cobrand($q);
    my ($problem_id, $email, $name) = dbh()->selectrow_array("select problem_id, email, name from comment where id=?", {}, $id);
    my $reported = $q->param('reported') || '';
    $reported = $reported eq 'Yes' ? 't' : ($reported eq 'No' ? 'f' : undef);
    return ask_questionnaire($token, $q) unless $reported;
    my $already = dbh()->selectrow_array("select id from questionnaire
        where problem_id=? and old_state='confirmed' and new_state='fixed'",
        {}, $problem_id);
    dbh()->do("insert into questionnaire (problem_id, whensent, whenanswered,
        ever_reported, old_state, new_state) values (?, ms_current_timestamp(),
        ms_current_timestamp(), ?, 'confirmed', 'fixed');", {}, $problem_id, $reported)
        unless $already;
    my $report_url = Cobrand::url($cobrand, "/report/$problem_id", $q);
    my $out = $q->p({class => 'confirmed'}, sprintf(_('Thank you &mdash; you can <a href="%s">view your updated problem</a> on the site.'), $report_url));
    $out .= CrossSell::display_advert($q, $email, $name);
    return $out;
}

