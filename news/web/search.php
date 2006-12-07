<?php
/*
 * search.php:
 * newsdemo search page.
 * 
 * Copyright (c) 2006 UK Citizens Online Democracy. All rights reserved.
 * Email: louise.crow@gmail.com. WWW: http://www.mysociety.org
 *
 * $Id: search.php,v 1.2 2006-12-07 15:57:36 louise Exp $
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
if ($search == '') {
    header('Location: /');
    exit();
}

$heading = sprintf(_("Search results for '%s'"), htmlspecialchars($search));
page_header("NeWs - " . $heading);
print '<h2>' . $heading . '</h2>';
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
                                print "<ul>";
                    		print $newspaper_results;
				print "</ul>";
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
				$out .= "<li>". _("No nearby newspapers")."</li>";
			}
			print p(sprintf(_("Results for <strong>newspapers</strong> with coverage within %s of <strong>%s</strong>:"), news_pretty_distance($radius, false), htmlspecialchars($desc)));
			print "<ul>";
			print $out;
			print "</ul>";
		}
	} 

	
	//Search for the name of a newspaper? 
	$newspapers = news_get_newspapers_by_name($search);
	if (count($newspapers) > 0 ){
		$success = 1;
		$text = generate_newspaper_list($newspapers);
		print p(sprintf(_("Results for <strong>newspapers</strong> with names matching <strong>%s</strong>:"), htmlspecialchars($search)));
		print "<ul>";
		print $text;
		print "</ul>";
	}

	if ($success == 0){
		print "Sorry, we couldn't find anything matching ";
		print htmlspecialchars($search);
	}


    
}

/* get_location_results 
 * */
function get_location_results($lat, $lon){
	$radius = gaze_get_radius_containing_population($lat, $lon, OPTION_NEWS_SEARCH_POPULATION);
	
	$locations = news_get_locations_by_location($lat, $lon, $radius);
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
        return array(generate_newspaper_list($newspapers), $radius);
}

/* generate_newspaper_list
 * For an array of newspapers, generate an HTML listing with links to details pages*/ 
function generate_newspaper_list($newspapers){
	$ret = "";
        foreach($newspapers as $newspaper){
                $ret .= '<li><a href="/newspaper?id=';
                $ret .= $newspaper['id'];
                $ret .= '">';
                $ret .= $newspaper['name'];
                $ret .= '</a>'; 
		if (array_key_exists('coverage', $newspaper)){
			$ret .= ' (coverage in area: ';
                	$ret .= $newspaper['coverage'];
			$ret .= ')';
		}
                $ret .= '</li>';

        }
        return $ret;

}

?>