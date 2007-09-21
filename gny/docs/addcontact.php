<?php
require_once('../includes/init.php');
require_once('table_classes/group.php');

class addcontact_page extends pagebase {

	//properties
	private $group = null;
	
	public function __construct(){
		parent::__construct();
	}
	
	//load
	protected function load(){
		if(session_read('group') == ''){
			redirect(WWW_SERVER . "/add/about/");
		}else{
			$this->group = session_read('group');
		}
	}
	
	//setup
	protected function setup (){
	
		//set the default contact mode
		if(!isset($this->group->involved_type) || $this->group->involved_type == ''){
			$this->group->involved_type = 'email';
			session_write('group', $this->group);
		}	

	}

	//Bind
	protected function bind() {

		//page vars
	    $this->page_title = "how do you want to be contacted?";
	    $this->menu_item = "add";	
	    $this->show_tracker = true;		
	    $this->tracker_location = 4;			
		$this->onloadscript = 'changeInvolvedType()';
		if($this->group->involved_type == 'email'){
	    	$this->set_focus_control = "txtInvolvedEmail";
		}else{
	    	$this->set_focus_control = "txtInvolvedLink";		
		}
		$this->assign('group', $this->group);
		
		$this->display_template();
					
	}

	//Unbind
	protected function unbind (){
		$this->group->involved_type = $this->data['radInvolvedType'];

		if($this->group->involved_type == 'email'){
			$this->group->involved_link = '';		
			$this->group->involved_email = $this->data['txtInvolvedEmail'];
		}else{
			$this->group->involved_link = $this->data['txtInvolvedLink'];		
			$this->group->involved_email = '';
		}
		$this->group->created_name = $this->data['txtCreatedName'];				
		$this->group->created_email = $this->data['txtCreatedEmail'];	
					
	}

	//Validate
	protected function validate (){

		$valid = true;
		if($this->group->involved_type == 'email'){
			if($this->group->involved_email == '' || !valid_email($this->group->involved_email)){
				$this->add_warning('Please enter a valid email address people can use to contact your group');
				$this->add_warn_control('txtInvolvedEmail');
				$valid = false;				
			}
		}
		
		if($this->group->involved_type == 'link'){
			if($this->group->involved_link == '' || !valid_url($this->group->involved_link)){
				$this->add_warning('Please enter a valid web address people can visit to get involved with your group');
				$this->add_warn_control('txtInvolvedLink');
				$valid = false;				
			}
		}
		
		if($this->group->created_email == ''){
			$this->add_warning('Please enter your email address');
			$this->add_warn_control('txtCreatedEmail');
			$valid = false;				
		}elseif(!valid_email($this->group->created_email)){
			$this->add_warning('Your email address is invalid, please check it and try again');
			$this->add_warn_control('txtCreatedEmail');
			$valid = false;				
		}
		
		if($this->group->created_name == ''){
			$this->add_warning('Please enter your name');
			$this->add_warn_control('txtCreatedName');
			$valid = false;				
		}
	
		return $valid;
	
	}

	//Process page
	protected function process (){

		//save data to session
		session_write('group', $this->group);
		
		if($this->validate()){
			redirect(WWW_SERVER . "/add/preview/");
		}else{
			//something's missing, show the errors
			$this->bind();	
		}
	}

}

//create class instance
$addcontact_page = new addcontact_page();

?>
