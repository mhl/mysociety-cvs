<?php
require_once('../../includes/init.php');

class index_page extends pagebase {

	//load
	protected function load (){
		$this->reset_smarty("admin/index.tpl");
	}


	//setup
	protected function setup (){

	}

	//Bind
	protected function bind() {
		//get any data

		//page vars
		$this->onloadscript = "";	
	    $this->page_title = "about us";
	    $this->menu_item = "about";	
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
$index_page = new index_page();

?>

