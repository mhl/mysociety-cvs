<?php
require_once('../includes/init.php');

class check_email_page extends pagebase {

	//load
	protected function load(){
	
	}

	//setup
	protected function setup (){
		
		if($_GET['type']){
			$this->viewstate['type'] = $_GET['type'];
		}else{
			throw_404();
		}
		
	}

	//Bind
	protected function bind() {

		//contact
		if($this->viewstate['type'] == 'contactemail'){
		    $this->page_title = "Now check your email";
		    $this->menu_item = "search";
			$this->assign('title', 'Now check your email!');
			$this->assign('confirm_type', 'your message');			
			$this->assign('action_result', 'to confirm your message');						
		}elseif($this->viewstate['type'] == 'group'){
		    $this->page_title = "Now check your email";
		    $this->menu_item = "add";
			$this->assign('title', 'Now check your email!');
			$this->assign('confirm_type', 'your group');			
			$this->assign('action_result', 'and your group will be added to ' . SITE_NAME);						
		}else{
			throw_404();
		}
	
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
$check_email_page = new check_email_page();

?>
