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

	if($search_type == 'postcode'){
	
		//UK postcode search
		if(is_partial_postcode($search)){
			$search = pad_partial_postcode($search);
		}

		$clean_postcode = clean_postcode($search);
		$result = get_postcode_location($clean_postcode, 'UK');
		$zoom_level = 14;
	}elseif($search_type == 'zipcode'){
		//US zipcode search
		$clean_postcode = trim($search);
		$result = get_postcode_location($clean_postcode, 'US');	
		$zoom_level = 14;
	}else{
		//Place name search
		$street = '';
		$place = '';
		$country = '';
		
		//split search by commas. assume: 1 = single palce, 2 = city & country, 3= street, city, country
		$explode = explode(",", $search);
		
		//single palce
		if(sizeof($explode) == 3){

			$street = trim($explode[0]);
			$place = trim($explode[1]);			
			$country = trim($explode[2]);	
			$result = get_place_location($place, $country, $street);
			$zoom_level = 14;
		}

		//place + country
		if(sizeof($explode) >= 2 && $result == false){

			if($place == ''){
				$place = trim($explode[0]);			
			}
			if($country == ''){
				$country = trim($explode[1]);	
			}

			$result = get_place_location($place, $country);
			$zoom_level = 11;
		}

		// place
		if(sizeof($explode) >= 1 && $result == false){
			//try and get their country from IP
			$place = $search;			
			if($country == ''){
				$gaze = factory::create('gaze');
				$gaze_country_code = $gaze->get_country_from_ip($_SERVER['REMOTE_ADDR']);
				if($gaze_country_code != false && $gaze->status != 'service unavaliable'){
					$country = $gaze_country_code;
				}else{
					//if no country then assume US
					$country = 'GB';
				}
			}
			
			$result = get_place_location($place, $country);
			$zoom_level = 11;	
		}
		
		//$result = get_place_location($place, $country);
		
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
