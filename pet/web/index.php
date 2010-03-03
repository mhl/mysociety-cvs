<?
// index.php:
// Main page for ePetitions website.
//
// Copyright (c) 2005 UK Citizens Online Democracy. All rights reserved.
// Email: matthew@mysociety.org. WWW: http://www.mysociety.org
//
// $Id: index.php,v 1.61 2010-03-03 12:35:19 matthew Exp $

// Load configuration file
require_once "../phplib/pet.php";
require_once "../../phplib/conditional.php";

if (OPTION_SITE_TYPE == 'multiple') {
    $recent = db_getAll("select petition.ref, content,
        body.ref as body_ref, body.name as body_name
    from petition, body
    where status = 'live' and body_id = body.id
    order by laststatuschange desc limit 5");
    $most = db_getAll("
    select petition.ref, content, cached_signers,
        body.ref as body_ref, body.name as body_name
    from petition, body
    where status = 'live' and body_id = body.id
    order by cached_signers desc limit 5");
} else {
    $recent = db_getAll("select ref, content from petition
    where status = 'live'
    order by laststatuschange desc limit 5");
    $most = db_getAll("
    select ref, content, cached_signers
    from petition
    where status = 'live'
    order by cached_signers desc limit 5");
}

// Lame: send last-modified now to encourage squid to cache us.
cond_headers(time());
header('Cache-Control: max-age=5');
page_header('Introduction to e-petitions', array(
    'rss' => array(
        'Latest Petitions' => '/rss/list'
    )
));

if (OPTION_SITE_NAME == 'sbdc') {
    echo '<h2>Make or sign petitions through this official Borsetshire District Council petitions website</h2>';
    front_actions();
    front_intro_text();
    front_most_popular($most);
    print '<div style="float: left; text-align: center; padding-top:0.5em; width: 45%; padding: 5px;">';
    pet_search_form(array('front'=>true));
    print '</div>';
    front_most_recent($recent);
    front_how_it_works();
} else {
    echo '<div id="content_clipboard">';
    front_actions();
    front_intro_text();
    pet_search_form(array('front'=>true));
    if (OPTION_CREATION_DISABLED) {
        page_closed_message(true);
    }
    echo '</div>';
    front_most_recent($recent);
    front_most_popular($most);
    front_how_it_works();
}
page_footer('Home');

# --- 

function front_actions() {
    echo '<div id="petition_actions"> <ul>';
    if (!OPTION_CREATION_DISABLED) {
        echo '<li id="action_create"><a href="/new"><img src="/images/clipboard-add.gif" alt="" class="noborder"
/><br />Create a Petition</a></li>';
    }

    echo '<li id="action_view"><a href="/list"><img src="/images/clipboard-write.gif" alt="" class="noborder"
/><br />View Petitions</a></li>
</ul>
</div>';
}

function front_intro_text() {
    if (OPTION_SITE_NAME == 'number10') {
        echo '<p>Petitions have long been sent to the Prime Minister by post or delivered to
the Number 10 door in person. You can now both create and sign petitions on
this website too, giving you the opportunity to reach a potentially wider audience
and to deliver your petition directly to Downing Street.</p>';
    } elseif (OPTION_SITE_NAME != 'sbdc') {
        echo '<p><em>You can now both create and sign petitions to ' . str_replace('the ', 'your ', OPTION_SITE_PETITIONED) . ' on this website,
giving you the opportunity to reach a potentially wider audience and to deliver your petition
directly to ' . OPTION_SITE_PETITIONED . '.</em></p>';
    }
}

function petition_row($petition, $c) {
    print '<li';
    if ($c%2) print ' class="a"';
    print '><a href="/';
    if (OPTION_SITE_TYPE == 'multiple') {
        print $petition['body_ref'] . '/">' . $petition['body_name'] . '</a> to <a href="/';
        print $petition['body_ref'] . '/';
    }
    print $petition['ref'] . '/">';
    print htmlspecialchars($petition['content']) . '</a>';
    if (isset($petition['cached_signers'])) {
        print ' <small>(';
        print $petition['cached_signers'] . ' signature';
        print ($petition['cached_signers'] == 1 ? '' : 's') . ')</small>';
    }
    print '</li>';
}

function front_most_recent($recent) {
    echo "<div id='most_recent'>
<h3 class='page_title_border'>Five most recent petitions</h3>
<p>We the undersigned petition";
    if (OPTION_SITE_TYPE == 'multiple') {
        echo ': <ul>';
    } else {
        echo ' ' . OPTION_SITE_PETITIONED . " to&hellip;</p> <ul>";
    }
    $c = 1;
    foreach ($recent as $petition) {
        petition_row($petition, $c++);
    }
    if (!count($recent)) {
        print '<li>None, you can <a href="/new">create a petition</a>.</li>';
    }
?>
</ul>
<p align="right"><a href="/list/open?sort=date" title="More recent petitions">More</a></p>
</div>
<?
}

function front_most_popular($most) {
?>
<div id="most_popular">
<h3 class="page_title_border">Five most popular open petitions</h3>
<p>We the undersigned petition <?=OPTION_SITE_PETITIONED?> to&hellip;</p>
<ul>
<?
    $c = 1;
    foreach ($most as $petition) {
        petition_row($petition, $c++);
    }
    if (!count($most)) {
        print '<li>None, you can <a href="/new">create a petition</a>.</li>';
    }
?>
</ul>
<p align="right"><a href="/list/open?sort=signers" title="More popular petitions">More</a></p>
</div>
<?
}

function front_how_it_works() {
?>

<div id="front_how">
<h3 class="page_title_border" style="clear: both">How it works</h3>

<p>You can view and sign any <a href="/list">current petitions</a>, and see
<?=OPTION_SITE_NAME=='number10'?'the Government':OPTION_SITE_PETITIONED."'s"?> response to any
<a href="/list/closed">completed petitions</a>.
<? if (OPTION_SITE_NAME != 'sbdc') { ?>
If you have signed a petition that has reached more than 500 signatures
by the time it closes, you will be sent a response from
<?=OPTION_SITE_NAME=='number10'?'the Government':OPTION_SITE_PETITIONED?> by email.
<? } ?>
</p>

<p>All petitions that are submitted to this website will be accepted, as long as
they are in accordance with our <a href="/terms">terms and conditions</a>.
The aim is to enable as many people as possible to make their views known.
</p>

<p>To ensure transparency, any petition that cannot be accepted will be listed,
along with the reasons why.
<?
    if (OPTION_SITE_NAME != 'sbdc') {
?>
A list of <a href="/list/rejected">rejected petitions</a>
is available on this website.</p>
<?
    }
    echo '</div>';
}

