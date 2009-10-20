<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" <?php language_attributes(); ?>>

<head profile="http://gmpg.org/xfn/11">
<meta http-equiv="Content-Type" content="<?php bloginfo('html_type'); ?>; charset=<?php bloginfo('charset'); ?>" />

<title><?php bloginfo('name'); ?> <?php if ( is_single() ) { ?> &raquo; Blog Archive <?php } ?> <?php wp_title(); ?></title>

<link rel="stylesheet" href="<?php bloginfo('stylesheet_directory'); ?>/memespring.css" type="text/css" media="screen" />
<link rel="stylesheet" href="<?php bloginfo('stylesheet_url'); ?>" type="text/css" media="screen" />
<?php if (is_category()) {
	$cat = intval( get_query_var('cat') );
?>
<link rel="alternate" type="application/rss+xml" title="<?php single_cat_title(); ?> RSS feed, mySociety blog" href="<?php echo get_category_feed_link($cat); ?>" />
<?php } ?>
<link rel="alternate" type="application/rss+xml" title="<?php bloginfo('name'); ?> RSS feed" href="<?php bloginfo('rss2_url'); ?>" />
<link rel="pingback" href="<?php bloginfo('pingback_url'); ?>" />

<?php wp_head(); ?>
</head>
<body>
<div id="divPage">

	<a href="#divContent" class="hide">Skip navigation</a>

	<!--Header-->
<?
    if ($_SERVER['SERVER_NAME'] == 'cee.mysociety.org') {
        $logo = 'cee.png';
        $logo_w = 360;
        $logo_h = 62;
    } else {
        $logo = 'logo.png';
        $logo_w = 297;
        $logo_h = 62;
    }
?>
	<div id="divHeader">
		<div id="imgLogo">
			<a href="/" title="mySociety.org homepage">
				<img src="http://www.mysociety.org/contimg/<?=$logo ?>" alt="mySociety.org" width="<?=$logo_w?>" height="<?=$logo_h?>" />
			</a>
		</div>

<?php
    if ($_SERVER['SERVER_NAME'] != 'cee.mysociety.org') {
?>
		<p id="pHeaderDonate" >
			<a id="aPiggy" href="/donate/" title="Donate to mySociety" >
				&nbsp;
			</a>
			Help us to make more<br/> useful things.
			<br/>
			<a href="/donate/">Donate to mySociety</a>
		</p>
<?php
    }
?>
	</div>

	<!-- Menu -->
	<div id="divMenu">
<?php
        if ($_SERVER['SERVER_NAME'] == 'cee.mysociety.org') {
            echo '<ul class="collapse">
	<li><a href="http://cee.mysociety.org/">Home</a></li>
	<li><a href="http://cee.mysociety.org/cfp/">Submit a proposal</a></li>
	<li><a href="http://cee.mysociety.org/cfp/view/">View ideas</a></li>
	<li><a href="http://www.mysociety.org/">mySociety</a></li>
</ul>';
        } else {
            print file_get_contents(TEMPLATEPATH . '/nav.html');
    	    include (TEMPLATEPATH . '/searchform.php');
        }
?>
	</div>
	
	<div id="divContent">
