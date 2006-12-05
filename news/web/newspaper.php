<?php
/*
 * newspaper.php:
 * newsdemo newspaper info page.
 * 
 * Copyright (c) 2006 UK Citizens Online Democracy. All rights reserved.
 * Email: louise.crow@gmail.com. WWW: http://www.mysociety.org
 *
 * $Id: newspaper.php,v 1.1 2006-12-05 13:28:17 louise Exp $
 * 
 */

require_once "../conf/general";
require_once "../../phplib/news.php";
require_once "../../phplib/utility.php";
require_once "../../phplib/validate.php";

require_once "../phplib/page.php";
require_once "../phplib/news.php";

$newspaper_id = trim(get_http_var('id', true));
page_header("Newspaper Information");
news_general_heading();
$text = newspaper_info($newspaper_id);
print $text;
$text = newspaper_coverage($newspaper_id);
print $text;
page_footer();

/* newspaper_info
 * Show the info about a newspaper */ 

function newspaper_info($newspaper_id){

	$newspaper = news_get_newspaper($newspaper_id);
	$ret = '<b>';
	$ret .= $newspaper['name'];
	$ret .= '</b><br/>';
        $ret .= '<b>Address:</b><br />';
	$ret .= $newspaper['address'];
	$ret .= '<br />';
	$ret .= '<b>Editor:</b> ';
        $ret .= $newspaper['editor'];
        $ret .= '<br />';
	$ret .= '<b>Website:</b> ';
        $ret .= $newspaper['website'];
        $ret .= '<br />';
	$ret .= '<b>Email:</b> ';
        $ret .= $newspaper['email'];
        $ret .= '<br />';
	$ret .= '<b>Phone:</b> ';
	$ret .= $newspaper['telephone'];
        $ret .= '<br />';
	$ret .= '<b>Fax:</b> ';
	$ret .= $newspaper['fax'];
        $ret .= '<br />';
        $ret .= '<b>Weekly?:</b> ';
        $ret .= ( $newspaper['isweekly'] ? "yes" : "no");
        $ret .= '<br />';
	$ret .= '<b>Evening?:</b> ';
        $ret .= ( $newspaper['isevening'] ? "yes" : "no");
        $ret .= '<br />';
        $ret .= '<b>Free?:</b> ';
	$ret .= ( $newspaper['free'] ? "yes" : "no");

	return $ret;
}

function newspaper_coverage($newspaper_id){

	$ret = '<h2>Coverage</h2>';
	#get the coverage info
	$coverage = news_get_coverage($newspaper_id);

	$ret .= "<table>";
	$ret .= "<tr>";
	$coverage_headings = array('Location', 'Lat', 'Lon', 'Population', 'Coverage');
	foreach ($coverage_headings as $heading){
		$ret .= "<th>";
		$ret .= "$heading";
		$ret .= "</th>";
	}
	$ret .= "</tr>";

	$coverage_keys = array('name', 'lat', 'lon', 'population', 'coverage');
	foreach($coverage as $location){
		$ret .=	"<tr>";
		foreach ($coverage_keys as $key){
			$ret .= "<td>";
			$ret .= "$location[$key]";
			$ret .="</td>";
		}
		$ret .= "</tr>";
	}

	$ret .= "</table>";
	
	return $ret; 
}
?>