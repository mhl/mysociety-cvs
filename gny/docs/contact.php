<?php
require_once('init.php');
require_once('table_classes/stat.php');
	
class contact_page extends pagebase {

	//Properties
	private $contact_email = null;

	//load
	protected function load(){
		
	}
	
	//setup
	protected function setup (){
		
		if($_GET['group']){
			$this->viewstate['url_id'] = $_GET['group'];
		}else{
			throw_404();
		}
		
	}

	//Bind
	protected function bind() {

		//try and get the group, check it is a contact by web type
		$search = factory::create('search');
		$result = $search->search_cached('group', array(array('url_id', '=', $this->viewstate['url_id'])),1);
		if(sizeof($result) != 1){
			throw_404();			
		}
		if($result[0]->involved_type != 'email'){
			throw_404();						
		}

		//put name in viewstate for later (cant do this with email as its crackable)
		$this->viewstate['group_name'] = $result[0]->name;

		//page vars
	    $this->page_title = "contact " . $result[0]->name;
	    $this->menu_item = "search";	
	    $this->set_focus_control = "txtName";
		$this->assign('group', $result[0]);

		$this->display_template();

	}

	//Unbind
	protected function unbind (){

		//need to get the group again so we can get their email (safer than putting in viewstate for privacy reasons)
		$search = factory::create('search');
		$result = $search->search_cached('group', array(array('url_id', '=', $this->viewstate['url_id'])),1);
		if(sizeof($result) !=1){
			report_error('tried to retrieve email address for ' . $this->viewstate['url_id'] . ' but failed');
		}

		$group = $result[0];

		//populate contact email object
		$this->contact_email = factory::create('contact_email');
		$this->contact_email->to_email = $group->involved_email;
		$this->contact_email->from_email = $this->data['txtEmail'];
		$this->contact_email->from_name = $this->data['txtName'];			
		$this->contact_email->subject = EMAIL_PREFIX . $group->name;
		$this->contact_email->message = $this->data['txtContactMessage'];
		
	}

	//Validate
	protected function validate (){

		$valid = true;
		if(!valid_email($this->contact_email->from_email)){
			$this->add_warning('Please enter a valid email address');
			$this->add_warn_control('txtEmail');
			$valid = false;
		}
		if($this->contact_email->from_name == ''){
			$this->add_warning('Please enter your name');
			$this->add_warn_control('txtName');
			$valid = false;
		}
		if($this->contact_email->message == ''){
			$this->add_warning('Please a message');
			$this->add_warn_control('txtContactMessage');
			$valid = false;
		}

		return $valid;
	}

	//Process page
	protected function process (){
		if($this->validate()){
			
			//save data
			if(!$this->contact_email->insert()){
				report_error('Error saving contact email');
			}
			
			//send confirmation email
			$confirmation = factory::create('confirmation');
			$confirmation->send($this->contact_email->from_email, 
				EMAIL_PREFIX . "Confirm your message to " . $this->viewstate['group_name'],
				"Click on the link below to confirm your message:",
				"contact_email", $this->contact_email->contact_email_id);
			
			//Update the stats table
			tableclass_stat::increment_stat("contactemail.sent.count");
			
			//send to check email page
			redirect(WWW_SERVER . '/checkemail.php?type=contactemail');
			
		}else{
			$this->bind();		
		}

	}

}

//create class instance
$contact_page = new contact_page();

?>