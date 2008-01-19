<?php
require_once('../includes/init.php');

class edit_page extends pagebase {

	//load
	protected function load (){

	}

	//setup
	protected function setup (){
		if($_GET['group']){
			$this->viewstate['url_id'] = $_GET['group'];
		}else{
			throw_404();
		}

		//set show sent mode to false
		$this->viewstate['show_sent'] = false;
	}

	//Bind
	protected function bind() {

		$search = factory::create('search');
		$result = $search->search_cached('group', array(array('url_id', '=', $this->viewstate['url_id'])));

		if(sizeof($result) != 1){
			throw_404();			
		}
	
		//page vars
		$this->onloadscript = "";	
	    $this->page_title = "edit " . $result[0]->name;
	    $this->menu_item = "search";
	
		if(!$this->viewstate['show_sent']){
	    	$this->set_focus_control = "txtEmail";
		}
	
		$this->assign('show_sent', $this->viewstate['show_sent']);
		$this->assign('group', $result[0]);

		$this->display_template();
					
	}

	//Unbind
	protected function unbind (){

	}

	//Validate
	protected function validate (){
		$valid = true;
		//check valid email address
		if($this->data['txtEmail'] == '' || !valid_email($this->data['txtEmail'])){
			$this->add_warning('Please enter a valid email address');
			$this->add_warn_control('txtEmail');
			$valid = false;
		}else{
			//check the email address is the correct one for this group
			$search = factory::create('search');
			$result = $search->search_cached('group', array(array('url_id', '=', $this->viewstate['url_id']), array('created_email', '=', $this->data['txtEmail'])));						
			if(sizeof($result) != 1){
				$this->add_warning('Sorry, that is not the email address you used to create this group');
				$this->add_warn_control('txtEmail');
				$valid = false;				
			}
		}

		return $valid;
	}

	//Process page
	protected function process (){
		if($this->validate()){
			if($this->viewstate['show_sent']  == false){
				$this->send_email();
				$this->viewstate['show_sent'] = true;
			}
			$this->bind();
		}else{
			$this->bind();
		}
	}

	private function send_email(){
		$search = factory::create('search');
		$result = $search->search_cached('group', array(array('url_id', '=', $this->viewstate['url_id'])));

		if(sizeof($result) != 1){
			trigger_error("unable to find group when sending edit email");
		}
		$group = $result[0];
		$confirmation = factory::create('confirmation');
		$confirmation->send($group->created_email, 
			EMAIL_PREFIX . "Edit the page for '" . $group->name . "'  on " . SITE_NAME,
			"Click on the link below to start editing " . $group->name . ":",
			"groups", $group->group_id, 'edit');
	}
	

}

//create class instance
$edit_page = new edit_page();

?>
