<?php
/*
 * search.php:
 * newsdemo search page.
 * 
 * Copyright (c) 2006 UK Citizens Online Democracy. All rights reserved.
 * Email: louise.crow@gmail.com. WWW: http://www.mysociety.org
 *
 * $Id: search.php,v 1.1 2006-12-05 13:27:44 louise Exp $
 * 
 */

require_once "../conf/general";
require_once "../../phplib/news.php";
require_once "../../phplib/utility.php";
require_once "../../phplib/validate.php";
require_once "../../phplib/mapit.php";
require_once "../../phplib/gaze.php";

require_once "../phplib/page.php";
require_once "../phplib/news.php";

$search = trim(get_http_var('q', true));
$heading = sprintf(_("Search results for '%s'"), htmlspecialchars($search));
page_header($heading);
news_general_heading();
search($search);
page_footer();

/* search SEARCH
 * Print a list of local newspapers close to the location entered */


function search($search){

	$success = 0;

	//Search for a postcode	
	$is_postcode = validate_postcode($search);
	$is_partial_postcode = validate_partial_postcode($search);
	

	if ($is_postcode || $is_partial_postcode)  {

		$success = 1;		
	        $location = mapit_get_location($search, $is_partial_postcode ? 1 : 0);
		if (mapit_get_error($location)) {
			print "<p>We couldn't find that postcode, please check it again.</p>";
        	} else {
			list($newspaper_results, $radius) = get_newspaper_results($location['wgs84_lat'], $location['wgs84_lon']);
			print sprintf('<p>Results for <strong>newspapers</strong> with coverage within %s of UK postcode <strong>%s</strong>:</p>', news_pretty_distance($radius, false),  htmlspecialchars(strtoupper($search)) );
                	if ($newspaper_results) {
                    		print $newspaper_results;
               	 } else {
                   		print "<ul><li>". _("No nearby newspapers.")."</li></ul>";
                	}
           	}
       	}

	//Search for a place
	$places = gaze_find_places("GB", null, $search, 5, 70);
	gaze_check_error($places);
	if (count($places) > 0) {
		$success = 1;
		foreach ($places as $p) {
			$out = '';
			list($name, $in, $near, $lat, $lon, $st, $score) = $p;
			$desc = $name;
			if ($in) $desc .= ", $in";
			if ($st) $desc .= ", $st";
			if ($near) $desc .= " (" . _('near') . " " . htmlspecialchars($near) . ")";
			list ($newspaper_results, $radius) = get_newspaper_results($lat, $lon);
			if ($newspaper_results) {
				$out .= $newspaper_results;
			} else {
				$out .= "<ul><li>". _("No nearby newspapers")."</li></ul>";
			}
			print p(sprintf(_("Results for <strong>newspapers</strong> with coverage within %s of <strong>%s</strong>:"), news_pretty_distance($radius, false), htmlspecialchars($desc)));
				print "<ul>";
			print $out;
			print "</ul>";
		}
	} 

	
	//Search for the name of a newspaper? 

	if ($success == 0){
		print htmlspecialchars($search);
		print " not recognized as a place or postcode.";
	}


    
}

/* get_location_results 
 * */
function get_location_results($lat, $lon){
	$radius = gaze_get_radius_containing_population($lat, $lon, OPTION_NEWS_SEARCH_POPULATION);
	
	$locations = news_get_locations($lat, $lon, $radius);
	$ret = "";
	foreach($locations as $location){
	        $ret .= '<li>';
             	$distance_line = news_pretty_distance($location['distance']);
		$ret .= $location['name'];
		$ret .= preg_replace('#^(.*)( away)$#', ' <strong>$1</strong>$2: ', $distance_line);
		$ret .= '</li>';

	}
	return array($ret, $radius); 
}

/* get_newspaper_results
 * */

function get_newspaper_results($lat, $lon){
        $radius = gaze_get_radius_containing_population($lat, $lon, OPTION_NEWS_SEARCH_POPULATION);
        $newspapers = news_get_newspapers_by_location($lat, $lon, $radius);
	$ret = "";
        foreach($newspapers as $newspaper){
                $ret .= '<li><a href="/newspaper?id=';
                $ret .= $newspaper['id'];
                $ret .= '">';
                $ret .= $newspaper['name'];
                $ret .= '</a> (coverage in area: ';
		$ret .= $newspaper['coverage'];
                $ret .= ')</li>';

        }
        return array($ret, $radius);
}

?>