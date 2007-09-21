<?php

	//A test file for the gaze api class
	//to us it, just point your browser at it and specify a test_type
	//e.g. http://localhost/gaze_test.php?test_type=ip

	require_once('gaze.php');


	$test_type = $_GET['type'];
	
	$gaze = factory::create('gaze');
	$result = null;
	
	//IP
	if($test_type == 'ip'){
	
		$ip = '87.194.95.124'; //UK
//		$ip = '192.168.0.1'; //UK
		
		$result = $gaze->get_country_from_ip($ip);
	
	}
	
	//Country
	if($test_type == 'countries'){
		$result = $gaze->get_find_places_countries();
	}
	
	//Places
	if($test_type == 'places'){
		$result = $gaze->find_places("GB", "brixton");
	}
	
	//Country bounding coords
	if($test_type == 'countrybounds'){
		$result = $gaze->get_country_bounding_coords("NZ");
	}

	//Country centroid
	if($test_type == 'countrycentroid'){
		$result = $gaze->get_country_centroid('NZ');
	}
		
	//Population density
	if($test_type == 'populationdensity'){
		$result = $gaze->get_population_density(51.462391, -0.114293);
	}
	
	//Radius for population
	if($test_type == 'radiuspopulation'){
		$result = $gaze->get_radius_containing_population(51.462391, -0.114293, 1000);
	}
	
	
	
	print "STATUS: " . $gaze->status . "<br/>";
	print "RESULT";
	print_r($result);

?>