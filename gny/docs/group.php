<?php
require_once('../includes/init.php');

class group_page extends pagebase {

	//load
	protected function load(){

	}

	//setup
	protected function setup (){
		
		if($_GET['group']){
			$this->viewstate['url_id'] = $_GET['group'];
		}else{
			throw_404();
		}
		
		$refering_url = getenv("HTTP_REFERER");
		if(isset($refering_url) && $refering_url != ''){
			$this->viewstate['refering_url'] = $refering_url;			
		}else{
			$this->viewstate['refering_url'] = '';			
		}
	}

	//Bind
	protected function bind() {

		//try and get the group
		$search = factory::create('search');
		$result = $search->search_cached('group', array(array('url_id', '=', $this->viewstate['url_id']),
                array('confirmed', '=', 1)));
	
		if(sizeof($result) != 1){
			throw_404();			
		}
		
		$group = $result[0];

		//page vars
		$this->onloadscript = "";	
	    $this->page_title = $result[0]->name;
	    $this->menu_item = "search";	
	    $this->set_focus_control = "";
		$this->assign('group', $group);
		$this->assign('show_return', strpos($this->viewstate['refering_url'], 'results.php') > -1);
		$this->assign('refering_url', $this->viewstate['refering_url']);		
		$this->assign('map_js', true);
		$this->assign('mini_map', 1);		
		$this->assign('google_maps_key', GOOGLE_MAPS_KEY);
		$this->onloadscript = 'load(' . $group->long_centroid . ', ' .
		$group->lat_centroid .', ' . $group->zoom_level . ')';
		$this->display_template();
					
	}

	//Unbind
	protected function unbind (){
			
	}

	//Validate
	protected function validate (){
	
		$valid = true;
		
		return $valid;
	}

	//Process page
	protected function process (){
		$this->bind();
	}

}

//create class instance
$group_page = new group_page();

?>
