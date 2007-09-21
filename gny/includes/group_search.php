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
				$clean_postcode = clean_postcode($search_term);
				$longlat = get_postcode_location($clean_postcode, 'UK');
				if($longlat == false){
					array_push($this->warnings, "A error occured when trying to find that post code");
					trigger_error("Unable to get locaiton for postcode: " . $search_term);
				}else{
					$long = $longlat[0];
					$lat = $longlat[1];					
				}
			
				//Update the stats table
				tableclass_stat::increment_stat("search.type.ukpostcode");
			}
			
			//zipcode?
			if($this->search_type == 'zipcode'){
				$clean_postcode = clean_postcode($search_term);
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

			//Do the search
			$search = factory::create('search');
			$result = $search->search_cached('group', array(
				array('long_bottom_left', '<', $long),
				array('long_top_right', '>', $long),
				array('lat_bottom_left', '<', $lat),
				array('lat_top_right', '>', $lat),
				array('confirmed', '=', 1)				
				),
				'AND',
				array(array("zoom_level", 'DESC'))
			);
			
			//Update the stats table
			tableclass_stat::increment_stat("search.count");
			
			//Return search result
			return $result;
			
		}
		
		public static function get_search_type($search_term){
		
			$search_type = "placename";
			
			//check if is postcode
			if(is_postcode($search_term)){
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