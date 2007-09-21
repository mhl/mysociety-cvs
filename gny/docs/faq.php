<?php
require_once('init.php');

class faq_page extends pagebase {

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
	    $this->page_title = "frequently asked questions";
	    $this->menu_item = "faq";	
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
$faq_page = new faq_page();

?>