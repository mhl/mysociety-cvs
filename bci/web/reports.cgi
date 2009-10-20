#!/usr/bin/perl -w -I../perllib

# report.cgi:
# Display summary reports for FixMyStreet
# And RSS feeds for those reports etc.
#
# Copyright (c) 2007 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org. WWW: http://www.mysociety.org
#
# $Id: reports.cgi,v 1.34 2009-10-20 14:37:46 louise Exp $

use strict;
use Standard;
use URI::Escape;
use mySociety::Alert;
use mySociety::DBHandle qw(select_all);
use mySociety::MaPit;
use mySociety::Web qw(ent NewURL);
use mySociety::VotingArea;

sub main {
    my $q = shift;
    my $all = $q->param('all') || 0;
    my $rss = $q->param('rss') || '';
    my $cobrand = Page::get_cobrand($q);
    # Look up council name, if given
    my $q_council = $q->param('council') || '';

    # Manual misspelling redirect
    if ($q_council =~ /^rhondda cynon taff$/i) {
        print $q->redirect('/reports/Rhondda+Cynon+Taf');
        return;
    }

    my ($one_council, $area_type, $area_name);
    if ($q_council =~ /\D/) {
        (my $qc = $q_council) =~ s/ and / & /;
        my $areas = mySociety::MaPit::get_voting_area_by_name($qc, $mySociety::VotingArea::council_parent_types, 10);
        if (keys %$areas == 1) {
            ($one_council) = keys %$areas;
            $area_type = $areas->{$one_council}->{type};
            $area_name = $areas->{$one_council}->{name};
        } else {
            foreach (keys %$areas) {
                if ($areas->{$_}->{name} =~ /^\Q$qc\E (Borough|City|District|County) Council$/) {
                    $one_council = $_;
                    $area_type = $areas->{$_}->{type};
                    $area_name = $qc;
                }
            }
        }
        if (!$one_council) { # Given a false council name
            print $q->redirect('/reports');
            return;
        }
    } elsif ($q_council =~ /^\d+$/) {
        $one_council = $q_council;
        my $va_info = mySociety::MaPit::get_voting_area_info($q_council);
        $area_name = $va_info->{name};
    }
    $all = 0 unless $one_council;

    # Look up ward name, if given
    my $q_ward = $q->param('ward') || '';
    my $ward;
    if ($one_council && $q_ward) {
        my $qw = mySociety::MaPit::get_voting_area_by_name($q_ward, $mySociety::VotingArea::council_child_types, 10);
        foreach my $id (sort keys %$qw) {
            if ($qw->{$id}->{parent_area_id} == $one_council) {
                $ward = $id;
                last;
            }
        }
        if (!$ward) { # Given a false ward name
            print $q->redirect('/reports/' . Page::short_name($q_council));
            return;
        }
    }

    # RSS - reports for sent reports, area for all problems in area
    if ($rss && $one_council) {
        my $url = Page::short_name($q_council);
        $url .= '/' . Page::short_name($q_ward) if $ward;
        if ($rss eq 'area' && $area_type ne 'DIS' && $area_type ne 'CTY') {
            # Two possibilites are the same for one-tier councils, so redirect one to the other
            print $q->redirect('/rss/reports/' . $url);
            return;
        }
        my $type = 'council_problems'; # Problems sent to a council
        my (@params, %title_params);
        $title_params{COUNCIL} = $area_name;
        push @params, $one_council if $rss eq 'reports';
        push @params, $ward ? $ward : $one_council;
        if ($ward && $rss eq 'reports') {
            $type = 'ward_problems'; # Problems sent to a council, restricted to a ward
            $title_params{WARD} = $q_ward;
        } elsif ($rss eq 'area') {
            $title_params{NAME} = $ward ? $q_ward : $q_council;
            $type = 'area_problems'; # Problems within an area
        }
        print $q->header( -type => 'application/xml; charset=utf-8' );
        my $xsl = Cobrand::feed_xsl($cobrand);
        my $out = mySociety::Alert::generate_rss($type, $xsl, "/$url", \@params, \%title_params, $cobrand);
        $out =~ s/matthew.fixmystreet/emptyhomes.matthew.fixmystreet/g if $q->{site} eq 'emptyhomes';
        print $out;
        return;
    }

    my %councils;
    if ($one_council) {
        %councils = ( $one_council => 1 );
    } else {
        # Show all councils on main report page
        my $ignore = 'LGD';
        $ignore .= '|CTY' if $q->{site} eq 'emptyhomes';
        my @types = grep { !/$ignore/ } @$mySociety::VotingArea::council_parent_types;
        %councils = map { $_ => 1 } @{mySociety::MaPit::get_areas_by_type(\@types, 10)};
    }

    my @params;
    my $where_extra = '';
    if ($ward) {
        push @params, $ward;
        $where_extra = "and areas like '%,'||?||',%'";
    } elsif ($one_council) {
        push @params, $one_council;
        $where_extra = "and areas like '%,'||?||',%'";
    }
    my $problem = select_all(
        "select id, title, detail, council, state, areas,
        extract(epoch from ms_current_timestamp()-lastupdate) as duration,
        extract(epoch from ms_current_timestamp()-confirmed) as age
        from problem
        where state in ('confirmed', 'fixed')
        $where_extra
        order by id desc
    ", @params);

    my (%fixed, %open);
    my $re_councils = join('|', keys %councils);
    foreach my $row (@$problem) {
        if (!$row->{council}) {
            # Problem was not sent to any council, add to possible councils
            while ($row->{areas} =~ /,($re_councils)(?=,)/g) {
                add_row($row, 0, $1, \%fixed, \%open);
            }
        } else {
            # Add to councils it was sent to
            $row->{council} =~ s/\|.*$//;
            my @council = split /,/, $row->{council};
            foreach (@council) {
                next if $one_council && $_ != $one_council;
                add_row($row, scalar @council, $_, \%fixed, \%open);
            }
        }
    }

    my $areas_info = mySociety::MaPit::get_voting_areas_info([keys %councils]);
    if (!$one_council) {
        print Page::header($q, title=>_('Summary reports'), expires=>'+1h');
        print $q->p(
            _('This is a summary of all reports on this site; select a particular council to see the reports sent there.'), ' ',
            _('Greyed-out lines are councils that no longer exist.')
        );
        my $c = 0;
        print '<table cellpadding="3" cellspacing="1" border="0">';
        print '<tr><th>' . _('Name') . '</th><th>' . _('New problems') . '</th><th>' . _('Older problems') . '</th>';
        if ($q->{site} ne 'emptyhomes') {
            print '<th>' . _('Old problems,<br>state unknown') . '</th>';
        }
        print '<th>' . _('Recently fixed') . '</th><th>' . _('Older fixed') . '</th></tr>';
        foreach (sort { $areas_info->{$a}->{name} cmp $areas_info->{$b}->{name} } keys %councils) {
            print '<tr align="center"';
            ++$c;
            if ($areas_info->{$_}->{generation_high}==10) {
                print ' class="gone"';
            } elsif ($c%2) {
                print ' class="a"';
            }
            my $url = Page::short_name($areas_info->{$_}->{name});
            print '><td align="left"><a href="/reports/' . $url . '">' .
                $areas_info->{$_}->{name} . '</a></td>';
            summary_cell(\@{$open{$_}{new}});
            if ($q->{site} eq 'emptyhomes') {
                my $c = 0;
                $c += @{$open{$_}{older}} if $open{$_}{older};
                $c += @{$open{$_}{unknown}} if $open{$_}{unknown};
                summary_cell($c);
            } else {
                summary_cell(\@{$open{$_}{older}});
                summary_cell(\@{$open{$_}{unknown}});
            }
            summary_cell(\@{$fixed{$_}{new}});
            summary_cell(\@{$fixed{$_}{old}});
            print "</tr>\n";
        }
        print '</table>';
    } else {
        my $name = $areas_info->{$one_council}->{name};
        if (!$name) {
            print Page::header($q, title=>_("Summary reports"));
            print "Council with identifier " . ent($one_council). " not found. ";
            print $q->a({href => '/reports' }, 'Show all councils');
            print ".";
        } else {
            my $rss_url = '/rss/reports/' . Page::short_name($name);
            my $thing = _('council');
            if ($ward) {
                $rss_url .= '/' . Page::short_name($q_ward);
                $thing = 'ward';
                $name = ent($q_ward) . ", $name";
            }
            print Page::header($q, title=>sprintf(_('%s - Summary reports'), $name), rss => [ sprintf(_('Problems within %s, FixMyStreet'), $name), $rss_url ]);
            my $rss_title = _('RSS feed');
            my $rss_alt = _('RSS feed of problems in this %s');
            my $summary_line;
            if ($all && $q->{site} eq 'scambs') {
                $summary_line = sprintf(_('You can <a href="%s">see less detail</a>.'), NewURL($q));
            } elsif ($q->{site} eq 'scambs') {
                $summary_line = sprintf(_('You can <a href="%s">see more details</a>.'), NewURL($q, all=>1));
            } elsif ($all) {
                $summary_line = sprintf(_('You can <a href="%s">see less detail</a> or go back and <a href="/reports">show all councils</a>.'), NewURL($q));
            } else {
                $summary_line = sprintf(_('You can <a href="%s">see more details</a> or go back and <a href="/reports">show all councils</a>.'), NewURL($q, all=>1));
            }
            print $q->p(
                $q->a({ href => $rss_url }, '<img align="right" src="/i/feed.png" width="16" height="16" title="' . $rss_title . '" alt="' . sprintf($rss_alt, $thing) . '" border="0" hspace="4">'),
                sprintf(_('This is a summary of all reports for one %s.'), $thing) . ' ' . $summary_line);
            print "<h2>$name</h2>\n";
            if ($open{$one_council}) {
                print '<div id="col_problems">';
                list_problems($q, _('New problems'), $open{$one_council}{new}, $all);
                my $old = [];
                if ($q->{site} eq 'emptyhomes') {
                    push @$old, @{$open{$one_council}{older}} if $open{$one_council}{older};
                    push @$old, @{$open{$one_council}{unknown}} if $open{$one_council}{unknown};
                } else {
                    $old = $open{$one_council}{older};
                }
                list_problems($q, _('Older problems'), $old, $all);
                if ($q->{site} ne 'emptyhomes') {
                    list_problems($q, _('Old problems, state unknown'), $open{$one_council}{unknown}, $all);
                }
                print '</div>';
            }
            if ($fixed{$one_council}) {
                print '<div id="col_fixed">';
                list_problems($q, _('Recently fixed'), $fixed{$one_council}{new}, $all);
                list_problems($q, _('Old fixed'), $fixed{$one_council}{old}, $all);
                print '</div>';
            }
        }
    }
    print Page::footer($q);
}
Page::do_fastcgi(\&main);

sub add_row {
    my ($row, $councils, $council, $fixed, $open) = @_;
    my $fourweeks = 4*7*24*60*60;
    my $duration = ($row->{duration} > 2 * $fourweeks) ? 'old' : 'new';
    my $type = ($row->{duration} > 2 * $fourweeks)
        ? 'unknown'
        : ($row->{age} > $fourweeks ? 'older' : 'new');
    my $entry = [ $row->{id}, $row->{title}, $row->{detail}, $councils ];
    #Fixed problems are either old or new
    push @{$fixed->{$council}{$duration}}, $entry if $row->{state} eq 'fixed';
    # Open problems are either unknown, older, or new
    push @{$open->{$council}{$type}}, $entry if $row->{state} eq 'confirmed';
}

sub summary_cell {
    my $c = shift;
    $c = 0 unless defined $c;
    $c = @$c if ref($c) eq 'ARRAY';
    print '<td>' . $c . '</td>';
}

sub list_problems {
    my ($q, $title, $problems, $all) = @_;
    return unless $problems;
    print "<h3>$title</h3>\n<ul>";
    foreach (@$problems) {
        print '<li><a href="/report/' . $_->[0] . '">';
        print ent($_->[1]);
        print '</a>';
        print ' <small>(sent to both)</small>' if $_->[3]>1;
        print ' <small>(not sent to council)</small>' if $_->[3]==0 && $q->{site} ne 'emptyhomes';
        print '<br><small>' . ent($_->[2]) . '</small>' if $all;
        print '</li>';
    }
    print '</ul>';
}

