<?php



	//the this a page to be called via ajax. it does its best to work out what people are searching for and 
	// then does a geo lookup

	require_once('../../includes/init.php');
	require_once('group_search.php');

	$search = trim(get_http_var('q'));
	$result = false;
	$zoom_level = 0;

	//Work out the search type
	$search_type = group_search::get_search_type($search);

	if ($search_type == 'postcode') {
		//UK postcode search
		$clean_postcode = clean_postcode($search);
		$result = get_postcode_location($clean_postcode, 'UK');
		$zoom_level = 14;
	} elseif ($search_type == 'zipcode') {
		//US zipcode search
		$clean_postcode = trim($search);
		$result = get_postcode_location($clean_postcode, 'US');	
		$zoom_level = 14;
	} else {
		//Place name search
		$parts = get_place_parts($search);
		
		if (!$parts['country']) {
			$gaze = factory::create('gaze');
			$gaze_country_code = $gaze->get_country_from_ip($_SERVER['REMOTE_ADDR']);
			if ($gaze_country_code != false && $gaze->status != 'service unavaliable') {
				$parts['country'] = $gaze_country_code;
			} else {
				$parts['country'] = 'GB'; //if no country then assume GB
			}
		}

		$result = get_place_location($parts);
		$zoom_level = 13;
	}

	//Add the zoom level into the return var
	$return = false;
	if($result != false){
		$return = array();
		$return['zoom'] = $zoom_level;
		$return['location'] = $result;
	}

	//convert the resposne to JSON format and print it
	$json = factory::create('json');
	print $json->encode($return);

?>
