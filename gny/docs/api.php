<?php
require_once('../includes/init.php');

class api_page extends pagebase {

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
	    $this->page_title = "Feeds and API";
	    $this->menu_item = "";	
	    $this->set_focus_control = "";
	
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
$api_page = new api_page();

?>
