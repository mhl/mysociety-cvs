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
		$this->assign('mini_map', 1);		
		$this->assign('google_maps_key', GOOGLE_MAPS_KEY);

		$this->display_template();
					
	}

	//Unbind
	protected function unbind (){
	
	}

	//Validate
	protected function validate (){
	
	}

	//Process page
	protected function process (){

	
	}

}

//create class instance
$map_page = new map_page();

?>
