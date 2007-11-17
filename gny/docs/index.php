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
		$search = factory::create('search');
		$groups = $search->search_cached('group', array(array('group_id', '>', 0), array('confirmed', '=', 1)),  
			'AND',
			array(array('group_id', 'DESC')),
			3);

		//page vars
		$this->onloadscript = "";	
	    $this->page_title = "meet your neighbours";
	    $this->menu_item = "search";	
	    $this->set_focus_control = "";			
		$this->assign('groups', $groups);
		$this->assignLang('search_hint', 'enter a place, postcode or zip code');
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

}

//create class instance
$index_page = new index_page();

?>
