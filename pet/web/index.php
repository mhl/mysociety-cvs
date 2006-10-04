<?
// index.php:
// Main code for PledgeBank website.
//
// Copyright (c) 2005 UK Citizens Online Democracy. All rights reserved.
// Email: matthew@mysociety.org. WWW: http://www.mysociety.org
//
// $Id: index.php,v 1.19 2006-10-04 21:41:06 francis Exp $

// Load configuration file
require_once "../phplib/pet.php";

header('Cache-Control: max-age=5');
page_header('Introduction to e-petitions');
?>

<h1><span dir="ltr">E-Petitions</span></h1>

<div id="content_clipboard">

<div id="petition_actions">
<ul>
<li id="action_create"><a href="/new"><img src="/images/clipboard-add.gif" alt="" class="noborder"
/><br />Create a Petition</a></li>
<li id="action_view"><a href="/list"><img src="/images/clipboard-write.gif" alt="" class="noborder"
/><br />View Petitions</a></li>
</ul>
</div>

<p>Petitions have long been sent to the Prime Minister by post or delivered to
the Number 10 door in person. You can now both create and sign petitions on
this website, giving you the opportunity to reach a potentially wider audience
and to deliver your petition directly to Downing Street.</p>

<blockquote>"Petitioning the Prime Minister via the web allows for petitions
to spread in ways not possible before."</blockquote>
<p align="right">&mdash; Tom, UK</p>

</div>

<div style="clear: both; float: left; width: 45%;">
<h2><span class="ltr">Five most recent petitions</span></h2>
<p>We the undersigned petition the Prime Minister to&hellip;</p>
<ul>
<?
$recent = db_getAll("select ref, content from petition
    where status = 'live'
    order by creationtime desc limit 5");
# XXX: Creation time is order of creation, not order of going live...
foreach ($recent as $petition) {
    print '<li><a href="/' . $petition['ref'] . '">';
    print htmlspecialchars($petition['content']) . '</a></li>';
}
if (!count($recent)) {
    print '<li>None, you can <a href="/new">create a petition</a>.</li>';
}
?>
</ul>
</div>

<div style="float: right; width: 45%;">
<h2><span class="ltr">Five most popular petitions</span></h2>
<p>We the undersigned petition the Prime Minister to&hellip;</p>
<ul>
<?
$recent = db_getAll("
    select ref, content,
        (select count(id) from signer
            where showname
            and petition_id = petition.id
            and emailsent = 'confirmed') as signers
    from petition
    where status = 'live'
    order by signers desc limit 5");
# XXX: Creation time is order of creation, not order of going live...
foreach ($recent as $petition) {
    print '<li><a href="/' . $petition['ref'] . '">';
    print htmlspecialchars($petition['content']) . '</a> <small>(';
    print $petition['signers'] . ' signature';
    print ($petition['signers'] == 1 ? '' : 's') . ')</small></li>';
}
if (!count($recent)) {
    print '<li>None, you can <a href="/new">create a petition</a>.</li>';
}
?>
</ul>
<? ?>
</div>

<h2 style="clear: both"><span class="ltr">How it works</span></h2>

<!-- <p>This service has been set up in partnership with <a
href="http://www.mysociety.org/">mySociety</a>, a non-partisan charitable
project that runs various democracy focussed websites in the UK, such as
<a href="http://www.hearfromyourmp.com/">HearFromYourMP.com</a>.
</p>
-->

<p>You can view and sign any <a href="/list">current petitions</a>, and see the
Government response to any <a href="/list/finished">completed petitions</a>.
If you have signed a petition, you will be sent a
response from the Government by email once the petition is closed.
</p>

<p>All petitions that are submitted to this website will be accepted, as long as
they are in accordance with our <a href="/terms">terms and conditions</a>.
The aim is to enable as many people as possible to make their views known.
</p>

<p>To ensure transparency, any petition that cannot be accepted will be listed,
along with the reasons why. A list of <a href="/list/rejected">rejected petitions</a>
is available on this website.</p>

<?  page_footer();

