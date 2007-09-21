<?php
require_once('init.php');

class index_page extends pagebase {

	//load
	protected function load (){

	}


	//setup
	protected function setup (){

	}

	//Bind
	protected function bind() {

		//show postcode hint?
		$show_postcode_hint == false;
		
		//groups
		$search = factory::create('search');
		$groups = $search->search_cached('group', array(array('group_id', '>', 0), array('confirmed', '=', 1)),  
			'AND',
			array(array('created_date', 'DESC')),
			3);

		//page vars
		$this->onloadscript = "";	
	    $this->page_title = "meet your neighbours";
	    $this->menu_item = "search";	
	    $this->set_focus_control = "";			
		$this->assign('groups', $groups);
		$this->assign('search_hint', 'enter a place, postcode or zip code');
	
		$this->display_template();
					
	}

	//Unbind
	protected function unbind (){

	}

	//Validate
	protected function validate (){
		
		if($this->data['txtSearch'] ==''){
			$this->add_warning('Please enter a post code, zip code or place name');
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