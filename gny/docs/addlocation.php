<?php
require_once('../includes/init.php');
require_once('table_classes/group.php');

class addlocation_page extends pagebase {

	//properties
	private $group = null;
	
	public function __construct(){
		parent::__construct();
	}

	//load
	protected function load(){

		if(session_read('group') == ''){
			redirect(WWW_SERVER . "/add/about/");
		}else{
			$this->group = session_read('group');
		}
	}

	//setup
	protected function setup (){

		//try and get their country code from IP (if not, set then default to GB)
		$gaze = factory::create('gaze');
		$this->viewstate['country_code'] = $gaze->get_country_from_ip($_SERVER['REMOTE_ADDR']);
		if($this->viewstate['country_code'] == false){
			$this->viewstate['country_code'] = "GB";
		}

		//set the js for the map
		if(!isset($this->group->zoom_level) || $this->group->zoom_level == ''){

			$bounding_coords = $gaze->get_country_bounding_coords($this->viewstate['country_code']);

			//work out an oppropriate zoom level
			$zoom = approximate_gmap_zoom($bounding_coords['bottom_right_long'],
				$bounding_coords['top_left_long']);

			$centroid_long = ($bounding_coords['bottom_right_long'] + $bounding_coords['top_left_long'])/2;
			$centroid_lat = ($bounding_coords['top_left_lat'] + $bounding_coords['bottom_right_lat'])/2;

			// Overrides for countries crossing the dateline
			// XXX Not sure what to do in Gaze about it...
			if ($this->viewstate['country_code'] == 'US') {
				$this->group->long_centroid = -100;
				$this->group->lat_centroid =  40;
				$this->group->zoom_level = 3;
			} elseif ($this->viewstate['country_code'] == 'RU') {
				$this->group->long_centroid = 80;
				$this->group->lat_centroid = 60;
				$this->group->zoom_level = 3;
			} elseif ($this->viewstate['country_code'] == 'NZ') {
				$this->group->long_centroid = -171;
				$this->group->lat_centroid = -41;
				$this->group->zoom_level = 5;
			} elseif ($this->viewstate['country_code'] == 'FJ') {
				$this->group->long_centroid = -180;
				$this->group->lat_centroid = $centroid_lat;
				$this->group->zoom_level = 8;
			} elseif ($this->viewstate['country_code'] == 'KI') {
				$this->group->long_centroid = -178.85;
				$this->group->lat_centroid = $centroid_lat;
				$this->group->zoom_level = 5;
			} else {
				$this->group->long_centroid = $centroid_long;
				$this->group->lat_centroid =  $centroid_lat;
				$this->group->zoom_level = $zoom;
			}
		}

	}

	//Bind
	protected function bind() {

		//page vars
		$this->onloadscript = 'load(' . $this->group->long_centroid . ', ' .
		$this->group->lat_centroid .', ' . $this->group->zoom_level . ')';	
	    $this->page_title = "location of your group";
	    $this->menu_item = "add";	
	    $this->show_tracker = true;		
	    $this->tracker_location = 3;			
	    $this->set_focus_control = "txtSearchMap";
		$this->assign('group', $this->group);
		$this->assign('map_js', true);
		$this->assign('google_maps_key', GOOGLE_MAPS_KEY);
		$this->assign('country_code', $this->viewstate['country_code']);	
		$this->assign('mini_map', false);			
		
		$this->display_template();
					
	}

	//Unbind
	protected function unbind (){
		$this->group->long_bottom_left = $this->data['hidLongBottomLeft'];
		$this->group->lat_bottom_left = $this->data['hidLatBottomLeft'];
		$this->group->long_top_right = $this->data['hidLongTopRight'];
		$this->group->lat_top_right = $this->data['hidLatTopRight'];								
		$this->group->long_centroid = $this->data['hidLongCentroid'];
		$this->group->lat_centroid = $this->data['hidLatCentroid'];
		$this->group->zoom_level = $this->data['hidZoomLevel'];

	}

	//Validate
	protected function validate (){
	
		$valid = true;
		
		if(!is_numeric($this->group->long_bottom_left) || !is_numeric($this->group->lat_bottom_left) 
			|| !is_numeric($this->group->long_top_right) || !is_numeric($this->group->lat_top_right) 
			|| !is_numeric($this->group->long_centroid) || !is_numeric($this->group->lat_centroid ) 
			|| !is_numeric($this->group->zoom_level)){
			$this->add_warning($this->smarty->translate('Something went wrong with google maps. Please try again'));
			$valid = false;
		}
		if($this->group->zoom_level < MAX_MAP_ZOOM){
			$this->add_warning($this->smarty->translate('The selected area for your group is too big. <strong>Please use the zoom tool to select a smaller area</strong>.'));
			$valid = false;
		}
		
		return $valid;
	}

	//Process page
	protected function process (){

		//save data to session
		if($this->validate()){
			redirect(WWW_SERVER . "/add/contact/");
		}else{
			//something's missing, show the errors
			$this->bind();	
		}

	}

}

//create class instance
$addlocation_page = new addlocation_page();

?>
