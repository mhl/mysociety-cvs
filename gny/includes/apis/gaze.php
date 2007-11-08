<?php

	require_once('init.php');

	//Implements calls to http://gaze.mysociety.org/. (excludes get_places_near)
	//for help contact richard pope at memespring.co.uk
	class gaze {

		//properties
		public $status = '';
		private $base_url = "http://gaze.mysociety.org/gaze-rest?";
		
	
		//Get country from IP (returns a country code)
		// Uses Squid-added accelerator header if it's present,
		// rather than call out to Gaze
		public function get_country_from_ip($ip){

			if (array_key_exists('HTTP_X_GEOIP_COUNTRY', $_SERVER)) {
				$ip_country = $_SERVER['HTTP_X_GEOIP_COUNTRY'];
				if ($ip_country != 'none')
					return $ip_country;
			}
	
			return $this->make_call($this->base_url . "f=get_country_from_ip&ip=" . urlencode($ip));
	
		}
		
		//Get countries (returns array of country codes)
		public function get_find_places_countries(){
	
			$return = $this->make_call($this->base_url . "f=get_find_places_countries");
			if($return != false){
				$return = explode("\n", $return);
			}
			
			return $return;
	
		}
		
		//Get country bounding coordinates
		public function get_country_bounding_coords($country_code){
	
			//get the results
			$result = $this->make_call($this->base_url . "f=get_country_bounding_coords&country=" . urlencode($country_code));
			$result = explode(" ", trim($result));

			//make into an indexxed array
			$bounding_coords = array();
			$bounding_coords['top_left_long'] = $result[2];				
			$bounding_coords['top_left_lat'] = $result[0];			
			$bounding_coords['bottom_right_long'] = $result[3];			
			$bounding_coords['bottom_right_lat'] = $result[1];					

			//return
			return $bounding_coords;

		}
		
		public function get_country_centroid($country_code){
			
			$bounding_coords = $this->get_country_bounding_coords($country_code);

			if($bounding_coords == false){
				trigger_error("Error getting bounding coords for " . $country_code);
			}
			
			$return = array();
			
			$return['long'] = $bounding_coords['top_left_long'] + 
				(($bounding_coords['bottom_right_long'] - $bounding_coords['top_left_long'])/2);

			$return['lat'] = $bounding_coords['bottom_right_lat'] + 
				(($bounding_coords['top_left_lat'] - $bounding_coords['bottom_right_lat'])/2);
								
			return $return;
		}
		
		//Population density
		public function get_population_density($long, $lat){

			//make query string
			$query_string = "f=get_population_density&lat=%s&lon=%s";
			$query_string = sprintf($query_string, urlencode($long), urlencode($lat));

			//get result
			$return = $this->make_call($this->base_url . $query_string);
			
			//return
			return trim($return);

		}
		
		//Rdius containing population
		public function get_radius_containing_population($long, $lat, $number, $maximum = 150){

			//make query string
			$query_string = "f=get_radius_containing_population&lat=%s&lon=%s&number=%s&maximum=%s";
			$query_string = sprintf($query_string, urlencode($lat), urlencode($long),
				urlencode($number), urlencode($maximum));

			//get result
			$return = $this->make_call($this->base_url . $query_string);

			//return
			return trim($return);

		}
		
		//Find places
		public function find_places($country_code, $query, $state = '', $maxresults = 10, $minscore = 1){
	
			//build up the query string
			$query_string = "f=find_places&country=%s&query=%s&maxresults=%s&minscore=%s";
			$query_string = sprintf($query_string, urlencode($country_code), urlencode($query),
				urlencode($maxresults), urlencode($minscore));
			
			if($state !=''){
				$query_string .= ("&state=" . urlencode($state));
			}
				
			//make the call	
			$return = $this->make_call($this->base_url . $query_string);
			
			if($return != false){
			
				//remove any "'s and turn into an array
				$explode = explode("\n", $return);
				
				if(sizeof($explode) > 1){
					//titles are in the first line of the array
					$titles = explode('",', $explode[0]);

					//get any results
					$places = array();
					for($i=1; $i < sizeof($explode); $i++) { 
					
						//create a new array for each place, using the titles array to index it
						$place_explode = explode('",', $explode[$i]);
						$place = array();
						for($ii=0; $ii < sizeof($titles); $ii++) { 
							$key = str_replace('"', '', $titles[$ii]);
							$key = strtolower($key);
							$place[$key] = str_replace('"', '', $place_explode[$ii]);
						}
					
						//add to palces array
						array_push($places, $place);
					}
					$return = $places;	
				}else{
					$return = false;
				}
			}
			
			return $return;
	
		}
		
		private function make_call($url){

			//grab the data
			$data = safe_scrape_cached($url);
			$return = false;
			
			if($data !=''){
				// gaze uses a single line feed for false
				if($data != "\n"){
					$return = trim($data);
					$this->status = 'sucess';
				}else{
					$this->status = 'not found';			
				}
			}else{
				$this->status = 'service unavaliable';
			}
			return $return;
	
		}
	}
	
	//Suport functions  - you might want to copy these to you central fucntions file

?>
