<?php
	require_once('../includes/init.php');

class the404_page extends pagebase {

	public function __construct(){
		parent::__construct();
	}

	protected function bind(){
	
		$this->page_title = "Page not found";
		$this->display_template();
	}

}

//create class instance
$the404_page = new the404_page();

?>
