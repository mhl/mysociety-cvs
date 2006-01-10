#!/usr/bin/perl -w -I../../perllib
#
# volunteertasks.cgi:
# Simple interface for viewing volunteer tasks from the CVSTrac database.
#
# Copyright (c) 2005 UK Citizens Online Democracy. All rights reserved.
# Email: chris@mysociety.org; WWW: http://www.mysociety.org/
#

my $rcsid = ''; $rcsid .= '$Id: volunteertasks.cgi,v 1.5 2006-01-10 15:13:34 chris Exp $';

use strict;
require 5.8.0;

use CGI qw(-no_xhtml);
use CGI::Fast;
use DBI;
use HTML::Entities;
use POSIX;
use WWW::Mechanize;

use mySociety::Util;

my $dbh = DBI->connect(
                "dbi:SQLite2:dbname=/usr/local/cvs/mysociety/mysociety.db",
                "", "", { 
                    # We don't want to enter a transaction which would lock the
                    # database.
                    AutoCommit => 1,
                    RaiseError => 1,
                    PrintError => 0,
                    PrintWarn => 0
                });

my %skills = map { $_->[0] => $_->[1] }
                @{$dbh->selectall_arrayref(
                    "select name, value from enums where type = 'extra1'")
                };
my %times = map { $_->[0] => lc($_->[1]) }
                @{$dbh->selectall_arrayref(
                    "select name, value from enums where type = 'extra2'")
                };

my %ticket_cache;  # id -> [date, heading, text]
my $M;
sub html_format_ticket ($) {
    my $ticket_num = shift;

    die "bad NUM '$ticket_num' in html_format_ticket"
        unless ($ticket_num =~ m#^(0|[1-9]\d*)$#);
    
    # Hideous. Cvstrac's formatting rules are quite complex, so better to
    # exploit the implementation that already exists.
    $M ||= new WWW::Mechanize();

    my $changetime = $dbh->selectrow_array('select changetime from ticket where tn = ?', {}, $ticket_num);

    return () if (!defined($changetime));

    if (exists($ticket_cache{$ticket_num})
        && $ticket_cache{$ticket_num}->[0] >= $changetime) {
        warn "using cached value for #$ticket_num\n";
        return ($ticket_cache{$ticket_num}->[1], $ticket_cache{$ticket_num}->[2]);
    }

    warn "grabbing #$ticket_num anew\n";
    my $url = "https://secure.mysociety.org/cvstrac/tktview?tn=$ticket_num";
    my $resp = $M->get($url) || die "GET $url: failed; system error = $!";
    die "GET $url: " . $resp->status_line() if (!$resp->is_success());

    # Have the response. We want the first <h2>...</h2> and the first
    # <blockquote>...</blockquote>

    my ($heading) = ($M->content() =~ m#<h2>Ticket \Q$ticket_num\E: (.*?)</h2>#s);
    die "GET $url: can't find ticket heading" if (!$heading);
    my ($content) = ($M->content() =~ m#<blockquote>(.*?)</blockquote>#s);
    die "GET $url: can't find ticket text" if (!$content);

    $ticket_cache{$ticket_num} = [ $changetime, $heading, $content ];
    return ($heading, $content);
}

sub start_html ($$) {
    my ($q, $title) = @_;
    return $q->start_html(
                -encoding => 'utf-8',
                -title => ($title ? "mySociety: $title" : "mySociety"),
                -style => {
                    -src => 'http://www.mysociety.org/global.css',
                    -media => 'screen',
                    -type => 'text/css'
                }
            ),
            $q->div({ -class => 'top' },
                $q->div({ -class => 'masthead' },
                    $q->img({
                        -src => 'http://www.mysociety.org/mslogo.gif',
                        -alt => 'mySociety.org'
                    })
                )
            ),
            $q->start_div({ -class => 'page-body' }),
            $q->div({ -class => 'menu' }, <<EOF
&nbsp;<a href="/">News</a>&nbsp;|
&nbsp;<a href="/faq.php">FAQ</a> &nbsp;|
&nbsp;<a href="/projects.php">Projects</a>&nbsp;|
&nbsp;<a href="/?cat=2">Developers' Blog</a>&nbsp;|
&nbsp;<a href="/moin.cgi">Wiki</a>&nbsp;|
&nbsp;<a href="">Volunteers</a>&nbsp;|
EOF
            ),
            $q->div({ -class => 'item_head' }, $title),
            $q->start_div({ -class => 'item' });
}

sub end_html ($) {
    my $q = shift;
    return $q->end_div(),
            $q->div({ -class => 'item_foot' }),
            $q->end_div(),
            $q->end_div(),
            $q->end_html();
}

sub do_list_page ($) {
    my $q = shift;
    my $pagelen = 20;

    my $skills_needed = $q->param('skills');
    $skills_needed = 'nontech' if (!$skills_needed || !exists($skills{$skills_needed}));

    my %skills_desc = (
            nontech => 'anyone',
            programmer => 'a programmer',
            designer => 'a graphic designer'
        );

    print $q->header(-type => 'text/html; charset=utf-8'),
            start_html($q, 'Tasks for Volunteers');

    my $choose = "Tasks for:";
    foreach (qw(nontech programmer designer)) {
        my $u = $q->url(-relative => 1) . "?skills=$_";
        $choose .= ($_ eq 'nontech' ? ' ' : '; ')
                    . $q->a({ -href => $u }, $skills_desc{$_});
    }
    
    print $q->h2("Tasks suitable for $skills_desc{$skills_needed}"),
            $q->p($choose);

    my $ntasks = $dbh->selectrow_array("
                    select count(tn) from ticket where extra1 = ?
                ", {}, $skills_needed);

    if ($ntasks == 0) {
        print $q->p("Unfortunately, there aren't any volunteer tasks suitable for $skills_desc{$skills_needed} at the moment. Please drop us a mail to", $q->a({ -href => 'mailto:team@mysociety.org' }, 'team@mysociety.org'), "to ask how you can get involved");
    } else {
        my %howlong_desc = (
                '30mins' => 'up to half an hour',
                '3hours' => 'up to three hours',
                'more' => 'longer than three hours'
            );

        foreach my $howlong (qw(30mins 3hours more dunno)) {
            my $desc = $howlong_desc{$howlong};
            if ($desc) {
                $desc = "Tasks which will take $desc";
            } else {
                $desc = "Tasks of unknown duration";
            }

            my $ntasks = $dbh->selectrow_array("
                            select count(tn) from ticket
                            where extra1 = ? and extra2 = ?
                        ", {}, $skills_needed, $howlong);
            next if ($ntasks == 0);
            print $q->h3($desc),
                    $q->start_ul({ -class => 'tasklist' });
            my $s = $dbh->prepare("
                            select tn, origtime, changetime, extra1, extra2
                            from ticket
                            where extra1 = ?
                                and extra2 = ?
                            order by max(origtime, changetime) desc
                        ");

            $s->execute($skills_needed, $howlong);
            while (my ($tn, $orig, $change, $extra1, $extra2) = $s->fetchrow_array()) {
                my ($heading, $content) = html_format_ticket($tn);
                my $timestamp = strftime('%A, %e %B %Y', localtime($orig));
                $timestamp .= " (changed "
                                . strftime('%A, %e %B %Y', localtime($change))
                                . ")"
                    if (strftime('%A, %e %B %Y', localtime($change)) ne $timestamp);
                print $q->li(
                        $q->h4($heading),
                        $q->span({ -class => 'when' }, $timestamp),
                        $q->div($content),
                        $q->div({ -class => 'signup' },
                            $q->start_form(-method => 'POST'),
                            $q->hidden(-name => 'tn', -value => $tn),
                            $q->hidden(-name => 'prevurl', -value => $q->url()),
                            $q->submit(-name => 'register', -value => "I'm interested >>>"),
                            $q->end_form()
                        ));
            }

            print $q->end_ul();
        }
    }

    print end_html($q);
}

sub do_register_page ($) {
    my $q = shift;

    my $tn = $q->param('tn');

    my ($orig, $change, $extra1, $extra2)
        = $dbh->selectrow_array("
                        select origtime, changetime, extra1, extra2
                        from ticket
                        where tn = ?", {}, $tn);
    my ($heading, $content) = html_format_ticket($tn);

    if (!$extra1 || $extra1 !~ /^(nontech|programmer|designer)$/
        || !$extra2 || $extra2 !~ /^(dunno|30mins|3hours|more)/
        || !$heading || !$content) {
        print $q->header(
                    -status => 400,
                    -type => 'text/html; charset=utf-8'),
                start_html($q, 'Oops'),
                $q->p("We couldn't find a volunteer task for the link you clicked on."),
                end_html($q);
        return;
    }

    my $name = $q->param('name');
    $name ||= $q->cookie('mysociety_volunteer_name');
    $name ||= '';
    $q->param('name', $name);
    my $email = $q->param('email');
    $email ||= $q->cookie('mysociety_volunteer_email');
    $email ||= '';
    $q->param('email', $email);

    my @errors = ( );
    push(@errors, "Please enter your name so that we know who you are") if (!$name);
    if ($email) {
        push(@errors, "The email address '$email' doesn't appear to be valid; please check it and try again")
            if (!mySociety::Util::is_valid_email($email))
    } else {
        push(@errors, "Please enter your email address so we can get in touch with you");
    }

    if ($q->param('edited') && !@errors) {
        # XXX should be in transaction.
        $dbh->do('
                delete from volunteer_interest
                where ticket_num = ? and email = ?', {},
                $tn, $email);
        $dbh->do('
                insert into volunteer_interest
                    (ticket_num, name, email, whenregistered)
                values (?, ?, ?, ?)', {},
                $tn, $name, $email, time());
        my $url = $q->param('prevurl');
        $url ||= 'http://www.mysociety.org/';
        print $q->header(
                -status => 302,
                -location => $url,
                -cookie => [
                    $q->cookie(
                        -name => 'mysociety_volunteer_name',
                        -value => $name,
                        -expires => '+1y',
                        -domain => 'mysociety.org'
                    ),
                    $q->cookie(
                        -name => 'mysociety_volunteer_email',
                        -value => $email,
                        -expires => '+1y',
                        -domain => 'mysociety.org'
                    ),
                ]
            );
    }

    print $q->header(-type => 'text/html; charset=utf-8'),
            start_html($q, "Express an interest in task #$tn");

    # Reproduce the task.
    my $timestamp = strftime('%A, %e %B %Y', localtime($orig));
    $timestamp .= " (changed "
                    . strftime('%A, %e %B %Y', localtime($change))
                    . ")"
        if (strftime('%A, %e %B %Y', localtime($change)) ne $timestamp);

    print $q->ul($q->li(
            $q->h4($heading),
            $q->span({ -class => 'when' }, $timestamp),
            $q->div($content)
        ));

    if (@errors) {
        print $q->ul($q->li([map { encode_entities($_) } @errors]));
    }

    print $q->start_form(-method => 'POST'),
            $q->hidden(-name => 'edited', -value => '1'),
            $q->hidden(-name => 'tn'),
            $q->hidden(-name => 'prevurl'),
            $q->start_table({ -id => 'volunteerform' }),
            $q->Tr(
                $q->th('Name'),
                $q->td($q->textfield(-name => 'name', -size => 30))
            ),
            $q->Tr(
                $q->th('Email'),
                $q->td($q->textfield(-name => 'email', -size => 30))
            ),
            $q->Tr(
                $q->th(),
                $q->td($q->submit(-name => 'register',
                        -value => 'Register my interest'))
            ),
            $q->end_table(),
            $q->end_form(),
            end_html($q);
}

while (my $q = new CGI::Fast()) {
#    $q->encoding('utf-8');
    $q->autoEscape(0);
    my $tn = $q->param('tn');
    if ($q->param('register') && defined($tn) && $tn =~ /^[1-9]\d*$/) {
        do_register_page($q);
    } else {
        do_list_page($q);
    }
}

$dbh->disconnect();
