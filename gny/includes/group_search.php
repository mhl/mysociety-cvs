<?php

	require_once('init.php');
	require_once('table_classes/stat.php');

	class group_search{
	
		public $warnings = array();
		public $search_type = "";
	
		public function search($search_term){
			
			//set the search type
			$this->search_type = self::get_search_type($search_term);
			
			$long = 0;
			$lat = 0;			

			//postcode?
			if($this->search_type == 'postcode'){

				//if its a partial postcode, padd it
				$clean_postcode = clean_postcode($search_term);
				$longlat = get_postcode_location($clean_postcode, 'UK');

				if($longlat != false){
					$long = $longlat[0];
					$lat = $longlat[1];					
				}
			
				//Update the stats table
				tableclass_stat::increment_stat("search.type.ukpostcode");
			}
			
			//zipcode?
			if($this->search_type == 'zipcode'){
				$clean_postcode = trim($search_term);
				$longlat = get_postcode_location($clean_postcode, 'US');
				if($longlat == false){
					array_push($this->warnings, "A error occured when trying to find that zip code");
					trigger_error("Unable to get locaiton for zipcode: " . $search_term);
				}else{
					$long = $longlat[0];
					$lat = $longlat[1];					
				}
				
				//Update the stats table
				tableclass_stat::increment_stat("search.type.ukpostcode");				
			}

			//long lat?
			if($this->search_type == 'longlat'){
				$split = split(",", trim($search_term));
				$long = $split[0];
				$lat = $split[1];

				//Update the stats table
				tableclass_stat::increment_stat("search.type.longlat");				
			}

			//Do the search for groups directly covering this location
			$search = factory::create('search');
			$groups = $search->search('group', array(
				array('long_bottom_left', '<', $long),
				array('long_top_right', '>', $long),
				array('lat_bottom_left', '<', $lat),
				array('lat_top_right', '>', $lat),
				array('confirmed', '=', 1)				
				),
				'AND',
				array(array("zoom_level", 'DESC'))
			);
		
		/*	
			//Do another search with buffeering based on population density 
			$gaze = factory::create('gaze');
			$radius_km = $gaze->get_radius_containing_population($long, $lat, POPULATION_THRESHOLD, MAX_KM_DISTANCE_BUFFER);
			
			//if that worked, do the other search
			if($radius_km && $gaze->status !='service unavaliable'){
			
				//work out the buffered long / lat values
				$buffered_long = distance_to_longitude($radius_km);
				$buffered_lat = distance_to_latitude($radius_km);

				//make the bounding box
				$buffered_bottom_left_long = $long - $buffered_long;
				$buffered_bottom_left_lat = $lat - $buffered_lat;
				$buffered_top_right_long = $long + $buffered_long;
				$buffered_top_right_lat = $lat + $buffered_lat;

				//do the buffered searches (THIS IS REALY INEFFICANT BUT PEAR DATA OBJECTS DONT DO MIXED AND/OR SEARCHES)
				$groups_buffered = array();
				$groups_buffered1 = $search->search('group', array(
					array('long_bottom_left', '>', $buffered_bottom_left_long),
					array('long_bottom_left', '<', $buffered_top_right_long),
					array('lat_bottom_left', '>', $buffered_bottom_left_lat),
					array('lat_bottom_left', '<', $buffered_top_right_lat),
					array('confirmed', '=', 1)				
					),
					'AND',
					array(array("zoom_level", 'DESC'))
				);

				if($groups_buffered1){
					foreach ($groups_buffered1 as $group_buffered1){
						array_push($groups_buffered, $group_buffered1);
					}
				}
				
				$groups_buffered2 = $search->search('group', array(
					array('long_top_right', '<', $buffered_top_right_long),
					array('long_top_right', '>', $buffered_top_right_long),
					array('lat_top_right', '>', $buffered_bottom_left_lat),
					array('lat_top_right', '<', $buffered_top_right_lat),
					array('confirmed', '=', 1)				
					),
					'AND',
					array(array("zoom_level", 'DESC'))
				);
				if($groups_buffered2){
					foreach ($groups_buffered2 as $group_buffered2){
						array_push($groups_buffered, $group_buffered2);
					}
				}
				
				$groups_buffered3 = $search->search('group', array(
					array('long_bottom_left' + $buffered_long, '>', $buffered_bottom_left_long),
					array('long_bottom_left' + $buffered_long, '<', $buffered_top_right_long),
					array('lat_bottom_left' + $buffered_lat, '>', $buffered_bottom_left_lat),
					array('lat_bottom_left' + $buffered_lat, '<', $buffered_top_right_lat),
					array('confirmed', '=', 1)				
					),
					'AND',
					array(array("zoom_level", 'DESC'))
				);
				if($groups_buffered3){
					foreach ($groups_buffered3 as $group_buffered3){
						array_push($groups_buffered, $group_buffered3);
					}
				}
				
				$groups_buffered3 = $search->search('group', array(
					array('long_top_right' + $buffered_long, '>', $buffered_bottom_left_long),
					array('long_top_right' + $buffered_long, '<', $buffered_top_right_long),
					array('lat_top_right' + $buffered_lat, '>', $buffered_bottom_left_lat),
					array('lat_top_right' + $buffered_lat, '<', $buffered_top_right_lat),
					array('confirmed', '=', 1)				
					),
					'AND',
					array(array("zoom_level", 'DESC'))
				);
				if($groups_buffered4){
					foreach ($groups_buffered4 as $group_buffered4){
						array_push($groups_buffered, $group_buffered4);
					}
				}

				//if we have any buffered groups, add them in
				if($groups_buffered){
					foreach ($groups_buffered as $group_buffered){
						array_push($groups, $group_buffered);
					}
					
					//remove any duplicates (again should really be in the database call)
					$cleaned_groups = array();
					foreach ($groups as $group){
						$allready_added = false;
						foreach ($cleaned_groups as $cleaned_group){
							if($cleaned_group->group_id == $group->group_id){
								$allready_added = true;
							}
						}
						
						if(!$allready_added){
							array_push($cleaned_groups, $group);
						}
					}
					
					$groups = $cleaned_groups;
					
				}
			
			}
		*/	
			//Update the stats table
			tableclass_stat::increment_stat("search.count");
			
			//Return search result
			return $groups;
			
		}
		
		public static function get_search_type($search_term){
		
			$search_type = "placename";
			
			//check if is postcode
			if(is_postcode($search_term)){
				$search_type = "postcode";
			}
			
			//check if partial postcode
			if(is_partial_postcode($search_term)){
				$search_type = "postcode";
			}
			
			//check if is zipcode
			if(is_zipcode($search_term)){
				$search_type = "zipcode";
			}
			
			//check if long lat
			if(is_longlat($search_term)){
				$search_type = "longlat";
			}

			return $search_type;
		
		}
	
	
	}

?>