<?php
require_once('../includes/init.php');

class map_page extends pagebase {

	//properties
	private $group_id = 0;
	
	public function __construct(){
		parent::__construct();
	}

	//load
	protected function load(){

	}
	
	//setup
	protected function setup (){
		$this->group_id = get_http_var('url_id');
		if(!isset($this->group_id) || $this->group_id == ''){
			throw_404();
		}
	}

	//Bind
	protected function bind() {

		$search = factory::create('search');
		$results = $search->search_cached('group', array(array('url_id', '=', $this->group_id)),1);
		if(sizeof($results) != 1){
			throw_404();			
		}
		$group = $results[0];

		//page vars
		$this->onloadscript = 'load(' . $group->long_centroid . ', ' .
		$group->lat_centroid .', ' . $group->zoom_level . ')';	
	    $this->page_title = "location of " . $group->name;
		$this->assign('map_js', true);
		$this->assign('google_maps_key', GOOGLE_MAPS_KEY);

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
			$this->add_warning('Something went wrong with google maps. Please try again');
			$valid = false;
		}
		if($this->group->zoom_level < MAX_MAP_ZOOM){
			$this->add_warning('The selected area for your group is too large. Please select a smaller area.');
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
$map_page = new map_page();

?>
