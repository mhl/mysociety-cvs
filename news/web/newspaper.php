<?php
/*
 * newspaper.php:
 * newsdemo newspaper info page.
 * 
 * Copyright (c) 2006 UK Citizens Online Democracy. All rights reserved.
 * Email: louise.crow@gmail.com. WWW: http://www.mysociety.org
 *
 * $Id: newspaper.php,v 1.2 2006-12-07 15:56:32 louise Exp $
 * 
 */

require_once "../conf/general";
require_once "../../phplib/news.php";
require_once "../../phplib/utility.php";
require_once "../../phplib/validate.php";

require_once "../phplib/page.php";
require_once "../phplib/news.php";

$newspaper_id = trim(get_http_var('id', true));

if ($newspaper_id == '') {
    header('Location: /');
    exit();
}

$newspaper = news_get_newspaper($newspaper_id);

if (!$newspaper['name']){
	page_header("NeWs - Newspaper not found");
	print '<h2>Newspaper not found</h2>';
	print 'This newspaper could not be found';
	exit();
}

$heading = $newspaper['name'];
page_header("NeWs - " . $heading);
print '<h2>' . $heading . '</h2>';
print '<h3>Contact information</h3>';
$text = newspaper_info($newspaper);
print $text;
$text = newspaper_journalists($newspaper_id);
print $text;
$text = newspaper_coverage($newspaper_id);
print $text;
page_footer();

/* newspaper_info
 * Generate some HTML for info about a newspaper */ 

function newspaper_info($newspaper){
       
	$ret = '<div id="newspaper-info-box">';
	$ret .= '<b>Address:</b><br /> ';
	$ret .= str_replace("\n", '<br />', trim($newspaper['address']));
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
        $ret .= '<b>Weekly?</b> ';
        $ret .= ( $newspaper['isweekly'] ? "yes" : "no");
        $ret .= '<br />';
	$ret .= '<b>Evening?</b> ';
        $ret .= ( $newspaper['isevening'] ? "yes" : "no");
        $ret .= '<br />';
        $ret .= '<b>Free?</b> ';
	$ret .= ( $newspaper['free'] ? "yes" : "no");
	$ret .= '</div>';
	return $ret;
}

/* newspaper_journalists
 * Generate some HTML for the journalists associated with a newspaper */
function newspaper_journalists($newspaper_id){

	$ret = '<h3>Journalists (<a href="../journalist?nid=';
	$ret .= $newspaper_id;
	$ret .= '">add journalist information</a>)</h3>';
	#get the journalist info
	$journalists = news_get_newspaper_journalists($newspaper_id);
	
	if (count($journalists) > 0){
		$ret .= '<div id="journalist-info-box">';
		$ret .= "<table>";
		$ret .= "<tr>";
		$journalist_headings = array('Name', 'Story Interests', 'Email', 'Phone', 'Fax');
		foreach ($journalist_headings as $heading){
			$ret .= "<th>";
			$ret .= "$heading";
			$ret .= "</th>";
		}
		$ret .= "<th></th>";
		$ret .= "</tr>";

		$journalist_keys = array('name', 'interests', 'email', 'telephone', 'fax');
		foreach ($journalists as $journalist ){
			$ret .= "<tr>";
			foreach ($journalist_keys as $key){
				$ret .= "<td>";
				$ret .= "$journalist[$key]";
				$ret .= "</td>";
			}
			$ret .= '<td><a href="journalist?id=' . $journalist['id'] . '&nid=' . $newspaper_id;
			$ret .= '">update</a>';
			$ret .= '</tr>';
		}
	
		$ret .= '</table>';
		$ret .= '</div>';

	}
	return $ret;
	
}

/* newspaper_coverage
 * Generate some HTML for the newspaper coverage */
function newspaper_coverage($newspaper_id){

	$ret = '<h3>Coverage</h3>';
	#get the coverage info
	$coverage = news_get_newspaper_coverage($newspaper_id);

	$ret .= '<div id="coverage-info-box">';
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
			if ($key == 'lat' or $key == 'lon'){
				$ret .= round($location[$key],3);
			}else{
				$ret .= "$location[$key]";
			}
			$ret .="</td>";
		}
		$ret .= "</tr>";
	}

	$ret .= "</table>";
	$ret .= '</div>';
	return $ret; 
}
?>