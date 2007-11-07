<?php
require_once('../includes/init.php');

class location_page extends pagebase {

	//properties
	private $search_term = '';
	private $country_code = '';
	private $places = array();
	private $gaze_down = false;

	//load
	protected function load (){

		//setup gaze
		$gaze = factory::create('gaze');

		//get search term from the url
		$this->search_term = '';
		$search_term = get_http_var('q');
		if(isset($search_term) && $search_term != ''){
			$this->search_term = get_http_var('q');
			
			//if the search term is a postcode or zip code, send tthe to the proper search page
			if(is_postcode($this->search_term) || is_partial_postcode($this->search_term) || is_zipcode($this->search_term)){
				redirect(WWW_SERVER . "/search/" . $this->search_term . "/");
			}
		}else{
			throw_404(); // no search term, nothing to see here
		}

		//get country code
		$country_code = get_http_var('country_code');		
		if(isset($country_code) && $country_code != ''){
			$this->country_code = get_http_var('country_code');
		}

		//if no country code, do an IP lookup
		if($this->country_code == ''){
			$country_code = $gaze->get_country_from_ip($_SERVER['REMOTE_ADDR']);
			if($country_code){
				$this->country_code = $country_code;
			}elseif($gaze->status == 'service unavaliable'){
				$this->gaze_down  = true;
			}
		}

		//if we have a country and a search term, then we can do a search
		if($this->gaze_down == false && $this->country_code != '' && $this->search_term != ''){

			# XXX: Need to split off state name if given... :-/
			# XXX: Display County if there's more than one result in a state
			$places = $gaze->find_places($this->country_code, $this->search_term);
			if($places){
				function sort_places($a, $b) {
					if ($a['score'] > $b['score']) return -1;
					elseif ($a['score'] < $b['score']) return 1;
					if ($a['state'] > $b['state']) return 1;
					elseif ($a['state'] < $b['state']) return -1;
					return 0;
				}
				usort($places, 'sort_places');
				$this->places = $places;
			}elseif($gaze->status == 'service unavaliable'){
				$this->gaze_down  = true;
			}
			
		}	
	
	}
	
	function check_single_match(){
		
		
		
	}


	//setup
	protected function setup (){

	}

	//Bind
	protected function bind() {

		//get countries
		$search = factory::create('search');
		$countries = $search->search_cached('country', array(array('disabled', '<>', '1')));

		//page vars
		$this->onloadscript = "";	
	    $this->page_title = "Choose a location";
	    $this->menu_item = "search";	
	    $this->set_focus_control = "ddlCountry";
		$this->assign("found_places", sizeof($this->places) >0);
		$this->assign("places", $this->places);
		$this->assign("gaze_down", $this->gaze_down);
		$this->assign("search_term", $this->search_term);
		$this->assign("country_code", $this->country_code);					
		$this->assign("countries", $countries);								

		$this->display_template();
					
	}

	//Unbind
	protected function unbind (){

	}

	//Validate
	protected function validate (){
		return true;
	}

	//Process
	protected function process (){
		$this->bind();
	}

}

//create class instance
$location_page = new location_page();

?>
