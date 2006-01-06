#!/usr/bin/perl -w
#
# volunteertasks.cgi:
# Simple interface for viewing volunteer tasks from the CVSTrac database.
#
# Copyright (c) 2005 UK Citizens Online Democracy. All rights reserved.
# Email: chris@mysociety.org; WWW: http://www.mysociety.org/
#

my $rcsid = ''; $rcsid .= '$Id: volunteertasks.cgi,v 1.2 2006-01-06 17:03:50 chris Exp $';

use strict;
require 5.8.0;

use CGI;
use CGI::Fast;
use DBI;
use POSIX;
use WWW::Mechanize;

my $dbh = DBI->connect(
                "dbi:SQLite2:dbname=/usr/local/cvs/mysociety/mysociety.db",
                "", "", { 
                    # Actually we're read-only, but we don't want to enter
                    # a transaction which would lock the database.
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

    return undef if (!defined($changetime));

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
    print $q->end_div(),
            $q->div({ -class => 'item_foot' }),
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
                                . ")" if (strftime('%A, %e %B %Y', localtime($change)) ne $timestamp);
                print $q->li(
                        $q->h4($heading),
                        $q->span({ -class => 'when' }, $timestamp),
                        $q->div($content));
            }

            print $q->end_ul();
        }
    }


    print end_html($q);
}

while (my $q = new CGI::Fast()) {
#    $q->encoding('utf-8');
    $q->autoEscape(0);
    do_list_page($q);
}

$dbh->disconnect();
