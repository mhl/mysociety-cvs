<?php
require_once('../includes/init.php');

class index_page extends pagebase {

	//load
	protected function load (){

	}

	//setup
	protected function setup (){

		//get geo ip so we can put an appropriate search hint in
		$gaze = factory::create('gaze');
		$this->viewstate['country'] = $gaze->get_country_from_ip($_SERVER['REMOTE_ADDR']);

	}

	//Bind
	protected function bind() {

		//show postcode hint?
		$show_postcode_hint == false;

		//latest groups
		$latest_groups = $this->latest_groups();
		$map_groups = $this->get_representative_groups();

		//page vars
		$this->onloadscript = "loadLatest()";	
		$this->use_body_script = true;
	    $this->page_title = "Meet the neighbours";
	    $this->menu_item = "search";	
	    $this->set_focus_control = "";			
		$this->assign('latest_groups', $latest_groups);
		$this->assign('map_groups', $map_groups);		
		$this->assign('map_js', true);		
		$this->assignLang('search_hint', 'enter a place, postcode or zip');
		$this->assign('country', strtoupper($this->viewstate['country']));
	
		$this->display_template();
					
	}

	//Unbind
	protected function unbind (){

	}

	//Validate
	protected function validate (){
		
		if($this->data['txtSearch'] ==''){
			$this->add_warning($this->smarty->translate('Please enter a post code, zip code or place name'));
			$this->add_warn_control('txtSearch');			
		}
		
		return sizeof($this->warnings) == 0;
	}

	//Process page
	protected function process (){
		if($this->validate()){
			redirect(WWW_SERVER . "/search/" . urlencode($this->data['txtSearch']));
		}else{
			$this->bind();
		}
	}
	
	private function latest_groups(){
		$search = factory::create('search');
		$groups = $search->search('group', array(array('group_id', '>', 0), array('confirmed', '=', 1)),  
			'AND',
			array(array('group_id', 'DESC')),
			4);
			
		return $groups;
	}
	
	private function get_representative_groups(){

		//get a representative sample of new groups from round the world
		$americas_groups = $this->groups_by_box(array(-150, 60, -30, -50), 4);
		$european_groups = $this->groups_by_box(array(-5, 70, 50, 30), 1);
		$african_groups = $this->groups_by_box(array(-15, 25, 60, -40), 1);
		$asian_groups = $this->groups_by_box(array(60, 90, 170, -60), 2);			

		return array_merge($european_groups, $americas_groups, $african_groups, $asian_groups);	
	}
	
	private function groups_by_box($box, $count){
		$search = factory::create('search');
		$groups = $search->search_cached('group', 
			array(
				array('group_id', '>', 0), 
				array('confirmed', '=', 1),
				array('long_centroid', '>', $box[0]),
				array('long_centroid', '<', $box[2]),				 
				array('lat_centroid', '<', $box[1]),
				array('lat_centroid', '>', $box[3]),				
			),  
			'AND',
			array(array('group_id', 'DESC')),
			$count);
			
		return $groups;
	}

}

//create class instance
$index_page = new index_page();

?>
