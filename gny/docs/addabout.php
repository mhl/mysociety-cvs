<?php
require_once('../includes/init.php');
require_once('table_classes/group.php');
				
class addabout_page extends pagebase {

	//properties
	private $group = null;
	
	public function __construct(){
		parent::__construct();
	}
	
	//load
	protected function load(){
		if(session_read('group') == ''){
			$group = factory::create('group');			
			session_write('group', $group);
		}else{
			$this->group = session_read('group');
		}
		if (is_longlat(get_http_var('q'))) {
			$parts = explode(',', get_http_var('q'));
			$this->group->long_centroid = $parts[0];
			$this->group->lat_centroid = $parts[1];
			$this->group->zoom_level = 13;
		}
	}
	
	//setup
	protected function setup (){

	}


	//Bind
	protected function bind() {

		//get group object out of the session
		$this->group = session_read('group');

		//page vars
		$this->onloadscript = "";	
	    $this->page_title = "about your group";
	    $this->menu_item = "add";	
	    $this->show_tracker = true;		
	    $this->tracker_location = 2;			
	    $this->set_focus_control = "txtName";
		$this->assign('group', $this->group);
		
		$this->display_template();

	}

	//Unbind
	protected function unbind (){
		$this->group->name = strip_tags($this->data['txtName']);
		$this->group->byline = strip_tags($this->data['txtByline']);		
		$this->group->description = strip_tags($this->data['txtDescription'], '<a><em><strong>');				
		$this->group->tags = strip_tags($this->data['txtTags']);				
	}

	//Validate
	protected function validate (){
	
		$valid = true;
		
		if($this->group->name == ''){
			$this->add_warning('Please enter the name of the group');
			$this->add_warn_control('txtName');
			$valid = false;
		}
		if($this->group->byline == ''){
			$this->add_warning('Please enter a one line description of the group e.g. "a residents email group for Hackney, UK"');
			$this->add_warn_control('txtByline');
			$valid = false;
		}
		
		/*
		removed this bit of validation as people couldent think what to write
		if($this->group->description == ''){
			$this->add_warning('Please enter some more information about your group e.g. size, purpose and aims"');
			$this->add_warn_control('txtDescription');
			$valid = false;
		}
		*/
		
		return $valid;
	}

	//Process page
	protected function process (){

		//save data to session
		session_write('group', $this->group);	
				
		if($this->validate()){
			redirect(WWW_SERVER . "/add/location/");
		}else{
			//something's missing, show the errors
			$this->bind();	
		}

	}

}

//create class instance
$addabout_page = new addabout_page();

?>
