<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head profile="http://gmpg.org/xfn/11">
	<meta http-equiv="Content-Type" content="<?php bloginfo('html_type'); ?>; charset=<?php bloginfo('charset'); ?>" />

	<title><?php bloginfo('name'); ?> <?php if ( is_single() ) { ?> &raquo; Blog Archive <?php } ?> <?php wp_title(); ?></title>
	
	<meta name="generator" content="WordPress <?php bloginfo('version'); ?>" /> <!-- leave this for stats -->

	<link rel="stylesheet" href="/global.css" type="text/css" media="screen" />
	<link rel="alternate" type="application/rss+xml" title="RSS 2.0"
    href="<?php bloginfo('rss2_url'); ?>?cat=<?=$cat?>" />
	<link rel="alternate" type="text/xml" title="RSS .92" href="<?php
    bloginfo('rss_url'); ?>?cat=<?=$cat?>" />
	<link rel="alternate" type="application/atom+xml" title="Atom 0.3"
    href="<?php bloginfo('atom_url'); ?>?cat=<?=$cat?>" />
	<link rel="pingback" href="<?php bloginfo('pingback_url'); ?>" />

	<?php wp_get_archives('type=monthly&format=link'); ?>

	<?php wp_head(); ?>
</head>

<body>
<?php
if ($_SERVER['HTTP_HOST'] != 'www.mysociety.org') {
	print '<p align="center">This is a test site, the real site is <a href="http://www.mysociety.org">over here</a>.<br>mySociety developers test new things here, you can <a href="http://www.mysociety.org/volunteertasks">join us</a> if you like.';
}
?>

<div class="top">
<div class="masthead"><a href="/"><img border="0" src="/mslogo.gif" alt="mySociety.org"/></a></div>
</div>

<div class="page-body">

<?
global $menu_proposals2006;
if ($menu_proposals2006) {
    print '<div class="menu">';
    print '<a href="/proposals2006/intro">About</a> | ';
    print '<a href="/proposals2006/guidelines">Guidelines</a> | ';
    print '<a href="/proposals2006/submit">Submit Your Proposal</a> | ';
    print '<a href="/proposals2006/view">Read All Proposals</a> | ';
    print '<a href="/">mySociety Homepage</a>';
    print '</div>';
} else 
    print file_get_contents("http://www.mysociety.org/menu.html"); 
?>


