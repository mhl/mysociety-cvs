<?php
require_once('../includes/init.php');

class browse_page extends pagebase {

	//load
	protected function load (){

	}


	//setup
	protected function setup (){

	}

	//Bind
	protected function bind() {
	
		//page vars
		$this->onloadscript = "";	
	    $this->page_title = "Browse groups";
	    $this->menu_item = "search";
	    $this->set_focus_control = "";
	
		$search = factory::create('search');
		$groups = $search->search_cached('group', array(
			array('group_id', '>', 0)),
			'AND',
			array(array("name", 'ASC')));
		$this->assign("groups", $groups);
	
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
$browse_page = new browse_page();

?>
