#!/usr/bin/perl -w
#
# index.cgi
#
# Administration interface for Neighbourhood Fix-It
#
# Copyright (c) 2007 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: index.cgi,v 1.16 2007-03-26 16:14:03 matthew Exp $
#

my $rcsid = ''; $rcsid .= '$Id: index.cgi,v 1.16 2007-03-26 16:14:03 matthew Exp $';

use strict;

# Horrible boilerplate to set up appropriate library paths.
use FindBin;
use lib "$FindBin::Bin/../perllib";
use lib "$FindBin::Bin/../../perllib";

use CGI::Carp;
use Error qw(:try);
use POSIX;
use DBI;

use Page;
use mySociety::Config;
use mySociety::DBHandle qw(dbh select_all);
use mySociety::MaPit;
use mySociety::VotingArea;

BEGIN {
    mySociety::Config::set_file("$FindBin::Bin/../conf/general");
    mySociety::DBHandle::configure(
        Name => mySociety::Config::get('BCI_DB_NAME'),
        User => mySociety::Config::get('BCI_DB_USER'),
        Password => mySociety::Config::get('BCI_DB_PASS'),
        Host => mySociety::Config::get('BCI_DB_HOST', undef),
        Port => mySociety::Config::get('BCI_DB_PORT', undef)
    );
}

sub html_head($$) {
    my ($q, $title) = @_;
    my $ret = $q->header(-type => 'text/html', -charset => 'utf-8');
    $ret .= <<END;
<html>
<head>
<title>$title - Neighbourhood Fix-it administration</title>
<style type="text/css"><!--
input { font-size: 9pt; margin: 0px; padding: 0px  }
table { margin: 0px; padding: 0px }
tr { margin: 0px; padding: 0px }
td { margin: 0px; padding: 0px; padding-right: 2pt; }
//--></style>
</head>
<body>
END
    
    my $pages = {
        'summary' => 'Summary',
        'councilslist' => 'Council contacts'
    };
    $ret .= $q->p(
        $q->strong("Neighbourhood Fix-it admin:"), 
        map { $q->a( {href=>build_url($q, $q->url('relative'=>1), { page => $_ })}, $pages->{$_}) } keys %$pages
    ); 

    return $ret;
}

sub html_tail($) {
    my ($q) = @_;
    return <<END;
</body>
</html>
END
}

# build_url CGI BASE HASH AMPERSAND
# Makes an escaped URL, whose main part is BASE, and
# whose parameters are the key value pairs in the hash.
# AMPERSAND is optional, set to 1 to use & rather than ;.
sub build_url($$$;$) {
    my ($q, $base, $hash, $ampersand) = @_;
    my $url = $base;
    my $first = 1;
    foreach my $k (keys %$hash) {
        $url .= $first ? '?' : ($ampersand ? '&' : ';');
        $url .= $q->escape($k);
        $url .= "=";
        $url .= $q->escape($hash->{$k});
        $first = 0;
    }
    return $url;
}

# do_summary CGI
# Displays general summary of counts.
sub do_summary ($) {
    my ($q) = @_;

    print html_head($q, "Summary");
    print $q->h2("Summary");

    print $q->p(join($q->br(), 
        map { dbh()->selectrow_array($_->[0]) . " " . $_->[1] } ( 
            ['select count(*) from contacts', 'contacts'],
            ['select count(*) from problem', 'problems'],
            ['select count(*) from comment', 'comments'],
            ['select count(*) from alert', 'alerts']
    )));

    print $q->h3("Council contacts status");
    my $statuses = dbh()->selectall_arrayref("select count(*) as c, confirmed from contacts group by confirmed order by c desc");
    print $q->p(join($q->br(), 
        map { $_->[0] . " " . ($_->[1] ? 'confirmed' : 'unconfirmed') } @$statuses 
    ));

    print $q->h3("Problem status");
    $statuses = dbh()->selectall_arrayref("select count(*) as c, state from problem group by state order by c desc");
    print $q->p(join($q->br(), 
        map { $_->[0] . " " . $_->[1] } @$statuses 
    ));

    print $q->h3("Comment status");
    $statuses = dbh()->selectall_arrayref("select count(*) as c, state from comment group by state order by c desc");
    print $q->p(join($q->br(), 
        map { $_->[0] . " " . $_->[1] } @$statuses 
    ));

    print $q->h3("Alert status");
    $statuses = dbh()->selectall_arrayref("select count(*) as c, confirmed from alert group by confirmed order by c desc");
    print $q->p(join($q->br(), 
        map { $_->[0] . " " . ($_->[1] ? 'confirmed' : 'unconfirmed') } @$statuses 
    ));

    print html_tail($q);
}

sub canonicalise_council {
    my $c = shift;
    $c =~ s/City of //;
    $c =~ s/N\. /North /;
    $c =~ s/E\. /East /;
    $c =~ s/W\. /West /;
    $c =~ s/S\. /South /;
    return $c;
}

# do_councils_list CGI
sub do_councils_list ($) {
    my ($q) = @_;

    print html_head($q, "Council contacts");
    print $q->h2("Council contacts");

    # Table of editors
    print $q->h3("Diligency prize league table");
    my $edit_activity = dbh()->selectall_arrayref("select count(*) as c, editor from contacts_history group by editor order by c desc");
    print $q->p(join($q->br(), 
        map { $_->[0] . " edits by " . $_->[1] } @$edit_activity 
    ));

    # Table of councils
    print $q->h3("Councils");
    my @councils;
    foreach my $type (@$mySociety::VotingArea::council_parent_types) {
        my $areas = mySociety::MaPit::get_areas_by_type($type);
        push @councils, @$areas;
    }
    my $councils = mySociety::MaPit::get_voting_areas_info(\@councils);
    my @councils_ids = keys %$councils;
    @councils_ids = sort { canonicalise_council($councils->{$a}->{name}) cmp canonicalise_council($councils->{$b}->{name}) } @councils_ids;
    my $bci_info = dbh()->selectall_hashref("select area_id, max(email) as email, count(*) as c from contacts group by area_id", 'area_id');
    print $q->p(join($q->br(), 
        map { 
            $q->a({href=>build_url($q, $q->url('relative'=>1), 
              {'area_id' => $_, 'page' => 'councilcontacts',})}, 
              canonicalise_council($councils->{$_}->{name})) . " " .
                ($bci_info->{$_} ?
                    ($bci_info->{$_}->{c} > 1 ? $bci_info->{$_}->{c} . ' addresses'
                    : "1 address (" . $bci_info->{$_}->{email} . ")")
                : $q->strong('no info at all') )
        } @councils_ids));

    print html_tail($q);
}

# do_council_contacts CGI AREA_ID
sub do_council_contacts ($$) {
    my ($q, $area_id) = @_;

    # Submit form
    my $updated = '';
    if ($q->param('posted') eq 'new') {
        # History is automatically stored by a trigger in the database
        my $update = dbh()->do("update contacts set
            email = ?,
            confirmed = ?,
            deleted = ?,
            editor = ?,
            whenedited = ms_current_timestamp(),
            note = ?
            where area_id = ?
	    and category = ?
            ", {}, 
            $q->param('email'), ($q->param('confirmed') ? 1 : 0),
            ($q->param('deleted') ? 1 : 0),
            ($q->remote_user() || "*unknown*"), $q->param('note'),
            $area_id, $q->param('category')
            );
        $updated = $q->p($q->em("Values updated"));
        unless ($update > 0) {
            dbh()->do('insert into contacts
                (area_id, category, email, editor, whenedited, note, confirmed, deleted)
                values
                (?, ?, ?, ?, ms_current_timestamp(), ?, ?, ?)', {},
                $area_id, $q->param('category'), $q->param('email'),
                ($q->remote_user() || '*unknown*'), $q->param('note'),
                ($q->param('confirmed') ? 1 : 0), ($q->param('deleted') ? 1 : 0)
            );
            $updated = $q->p($q->em("New category contact added"));
        }
        dbh()->commit();
    } elsif ($q->param('posted') eq 'update') {
        $updated = $q->p($q->em(join('', $q->param('confirmed'))));
    }
 
    my $bci_data = select_all("select * from contacts where area_id = ? order by category", $area_id);
    my $mapit_data = mySociety::MaPit::get_voting_area_info($area_id);
    
    # Title
    my $title = 'Council contact for ' . $mapit_data->{name};
    print html_head($q, $title);
    print $q->h2($title);
    print $updated;

    # Example postcode
    my $example_postcode = mySociety::MaPit::get_example_postcode($area_id);
    if ($example_postcode) {
        print $q->p("Example postcode to test on NeighbourHoodFixit.com: ",
            $q->a({href => build_url($q, "http://www.neighbourhoodfixit.com/",
                    { 'pc' => $example_postcode}) }, 
                $example_postcode));
    }

    print $q->start_form(-method => 'POST', -action => $q->url('relative'=>1));
    print $q->start_table({border=>1});
    print $q->th({}, ["Category", "Email", "Confirmed", "Deleted", "Last editor", "Note", "When edited"]);
    foreach my $l (@$bci_data) {
        print $q->Tr($q->td([
            $q->a({href=>build_url($q, $q->url('relative'=>1),
                { 'area_id' => $area_id, 'category' => $l->{category}, 'page' => 'counciledit'})},
                $l->{category}), $l->{email}, $l->{confirmed} ? 'Yes' : 'No',
            $l->{deleted} ? 'Yes' : 'No', $l->{editor}, $l->{note},
            $l->{whenedited} =~ m/^(.+)\.\d+$/,
	    $q->checkbox(-name => 'confirmed', -checked => $l->{confirmed}, -value => $l->{category}, -label => '')
        ]));
    }
    print $q->end_table();
    print $q->p(
        $q->hidden('area_id'),
        $q->hidden('posted', 'update'),
        $q->hidden('page', 'councilcontacts'),
        $q->submit('Update statuses')
    );
    print $q->end_form();

    # Display form for adding new category
    print $q->h3('Add new category');
    print $q->start_form(-method => 'POST', -action => $q->url('relative'=>1));
    print $q->p($q->strong("Category: "),
        $q->textfield(-name => "category", -size => 30));
    print $q->p($q->strong("Email: "),
        $q->textfield(-name => "email", -size => 30));
    print $q->p(
        $q->checkbox(-name => "confirmed", -value => 1, -label => "Confirmed"), " ",
        $q->checkbox(-name => "deleted", -value => 1, -label => "Deleted")
    );
    print $q->p($q->strong("Note: "),
        $q->textarea(-name => "note", -rows => 3, -columns=>40));
    print $q->p(
        $q->hidden('area_id'),
        $q->hidden('posted', 'new'),
        $q->hidden('page', 'councilcontacts'),
        $q->submit('Create category')
    );
    print $q->end_form();

    print html_tail($q);
}

# do_council_edit CGI AREA_ID CATEGORY
sub do_council_edit ($$$) {
    my ($q, $area_id, $category) = @_;

    # Get all the data
    my $bci_data = select_all("select * from contacts where area_id = ? and category = ?", $area_id, $category);
    $bci_data = $bci_data->[0];
    my $bci_history = select_all("select * from contacts_history where area_id = ? and category = ? order by contacts_history_id", $area_id, $category);
    my $mapit_data = mySociety::MaPit::get_voting_area_info($area_id);
    
    # Title
    my $title = 'Council contact for ' . $mapit_data->{name};
    print html_head($q, $title);
    print $q->h2($title);

    # Example postcode
    my $example_postcode = mySociety::MaPit::get_example_postcode($area_id);
    if ($example_postcode) {
        print $q->p("Example postcode to test on NeighbourHoodFixit.com: ",
            $q->a({href => build_url($q, "http://www.neighbourhoodfixit.com/",
                    { 'pc' => $example_postcode}) }, 
                $example_postcode));
    }

    # Display form for editing details
    print $q->start_form(-method => 'POST', -action => $q->url('relative'=>1));
    map { $q->param($_, $bci_data->{$_}) } qw/category email confirmed deleted/;
    $q->param('page', 'councilcontacts');
    print $q->strong("Category: ") . $bci_data->{category};
    print $q->hidden("category");
    print $q->strong(" Email: ");
    print $q->textfield(-name => "email", -size => 30) . " ";
    print $q->checkbox(-name => "confirmed", -value => 1, -label => "Confirmed") . " ";
    print $q->checkbox(-name => "deleted", -value => 1, -label => "Deleted");
    print $q->br();
    print $q->strong("Note: ");
    print $q->textarea(-name => "note", -rows => 3, -columns=>40) . " ";
    print $q->br();
    print $q->hidden('area_id');
    print $q->hidden('posted', 'true');
    print $q->hidden('page');
    print $q->submit('Save changes');
    print $q->end_form();

    # Display history of changes
    print $q->h3('History');
    print $q->start_table({border=>1});
    print $q->th({}, ["When edited", "Email", "Confirmed", "Deleted", "Editor", "Note"]);
    my $html = '';
    my $prev = undef;
    foreach my $h (@$bci_history) {
        $h->{confirmed} = $h->{confirmed} ? "yes" : "no",
        $h->{deleted} = $h->{deleted} ? "yes" : "no",
        my $emailchanged = ($prev && $h->{email} ne $prev->{email}) ? 1 : 0;
        my $confirmedchanged = ($prev && $h->{confirmed} ne $prev->{confirmed}) ? 1 : 0;
        my $deletedchanged = ($prev && $h->{deleted} ne $prev->{deleted}) ? 1 : 0;
        $html .= $q->Tr({}, $q->td([ 
                $h->{whenedited} =~ m/^(.+)\.\d+$/,
                $emailchanged ? $q->strong($h->{email}) : $h->{email},
                $confirmedchanged ? $q->strong($h->{confirmed}) : $h->{confirmed},
                $deletedchanged ? $q->strong($h->{deleted}) : $h->{deleted},
                $h->{editor},
                $h->{note}
            ]));
        $prev = $h;
    }
    print $html;
    print $q->end_table();

=comment
    # Google links
    print $q->p(
        $q->a({href => build_url($q, $q->url('relative'=>1), 
              {'area_id' => $area_id, 'page' => 'counciledit', 'r' => $q->url(-query=>1, -path=>1, -relative=>1)}) }, 
              "Edit councils and wards"),
        " |",
        $q->a({href => build_url($q, $q->url('relative'=>1), 
              {'area_id' => $area_id, 'page' => 'mapitnamesedit', 'r' => $q->url(-query=>1, -path=>1, -relative=>1)}) }, 
              "Edit ward aliases"),
        " |",
        map { ( $q->a({href => build_url($q, "http://www.google.com/search", 
                    {'q' => "$_"}, 1)},
                  "Google" . ($_ eq "" ? " alone" : " '$_'")),
            " (",
            $q->a({href => build_url($q, "http://www.google.com/search", 
                    {'q' => "$_",'btnI' => "I'm Feeling Lucky"}, 1)},
                  "IFL"),
            ")" ) } ("$name", "$name councillors ward", $name_data->{'name'} . " councillors")
    );
=cut

    print html_tail($q);
}

sub main {
    my $q = shift;
    my $page = $q->param('page');
    $page = "summary" if !$page;
    my $area_id = $q->param('area_id');
    my $category = $q->param('category');

    if ($page eq "councilslist") {
        do_councils_list($q);
    } elsif ($page eq "councilcontacts") {
        do_council_contacts($q, $area_id);
    } elsif ($page eq "counciledit") {
        do_council_edit($q, $area_id, $category);
    } else {
        do_summary($q);
    }
}
Page::do_fastcgi(\&main);
