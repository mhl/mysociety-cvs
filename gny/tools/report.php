#!/usr/bin/php5
<?php

	require_once(dirname(__FILE__) .'../../includes/init.php');

	$days = 7;
	
	//make thesearch object
	$search = factory::create('search');

	//work out date range (1 week)
	$date = mysql_date(time() - ($days * 24 * 60 * 60));
	
	$groups = $search->search('group', array(
			array('created_date', '>', $date)),
			'AND',
			array(array("name", 'ASC'))); 

	//get all time stats
	$stats = $search->search('stat', array(
		array('stat_id', '>', 1)),
		'AND',
		array(array("stat_key", 'ASC')));

	//setup smarty
    $smarty = new Smarty();
    $smarty->compile_dir = SMARTY_PATH;

	//assign data
	$smarty->assign("days", $days);
	$smarty->assign("groups", $groups);
	$smarty->assign("stats", $stats);		
	$smarty->assign("www_server", WWW_SERVER);
	$smarty->assign("team_email", CONTACT_EMAIL);
   	
	//render template
	$body = $smarty->fetch(TEMPLATE_DIR . "/emails/report.tpl"); 

	//send email
	$title = SITE_NAME . " stats (" . sizeof($groups) . " new groups in the past " . $days ." days)";
	send_text_email(CONTACT_EMAIL, "stats@" . DOMAIN, "stats@" . DOMAIN, $title, $body);

?>
