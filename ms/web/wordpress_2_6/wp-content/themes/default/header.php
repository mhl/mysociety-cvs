<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" <?php language_attributes(); ?>>

<head profile="http://gmpg.org/xfn/11">
<meta http-equiv="Content-Type" content="<?php bloginfo('html_type'); ?>; charset=<?php bloginfo('charset'); ?>" />

<title><?php bloginfo('name'); ?> <?php if ( is_single() ) { ?> &raquo; Blog Archive <?php } ?> <?php wp_title(); ?></title>

<link rel="stylesheet" href="/wp/wp-content/themes/default/memespring.css" type="text/css" media="screen" />
<link rel="stylesheet" href="<?php bloginfo('stylesheet_url'); ?>" type="text/css" media="screen" />
<link rel="alternate" type="application/rss+xml" title="<?php bloginfo('name'); ?> RSS Feed" href="<?php bloginfo('rss2_url'); ?>" />
<link rel="pingback" href="<?php bloginfo('pingback_url'); ?>" />

<?php wp_head(); ?>
</head>
<body>
<div id="divPage">

	<a href="#divContent" class="hide">Skip navigation</a>
	
	<!--Header-->
	<div id="divHeader">
		<div id="imgLogo">
			<a href="/" title="mySociety.org homepage">
				<img src="/contimg/logo.png" alt="mySociety.org" width="297" height="62" />
			</a>
		</div>

		<p id="pHeaderDontate" >
			<a id="aPiggy" href="/dotate/" title="Dontate to mySociety" >
				&nbsp;
			</a>
			Help us to keep making<br/> useful things!
			<br/>
			<a href="/dotate/">Donate to mySociety</a>
		</p>
	</div>

	<!-- Menu -->
	<div id="divMenu">
	<?php print file_get_contents($_SERVER['DOCUMENT_ROOT'] . "/nav.html"); ?>
	<?php include (TEMPLATEPATH . '/searchform.php'); ?>
	</div>


	<div id="divContent">