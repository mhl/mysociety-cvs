<?php
require_once('init.php');

class report_page extends pagebase {

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
	    $this->page_title = "report abuse";
	    $this->menu_item = "search";	
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
$report_page = new report_page();

?>