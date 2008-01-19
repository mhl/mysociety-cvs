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

		/*
		XX removing this for the moment, it seemed to be confusing people on next page
		// auto center group nbased on users last search
		if (is_longlat(get_http_var('q'))) {
			$parts = explode(',', get_http_var('q'));
			$this->group->long_centroid = $parts[0];
			$this->group->lat_centroid = $parts[1];
			$this->group->zoom_level = 13;
		}
		*/
	}
	
	//setup
	protected function setup (){

	}


	//Bind
	protected function bind() {

		//get group object out of the session
		$this->group = session_read('group');

		//get categories for dropdown
		$search = factory::create('search');
		$categories = $search->search_cached('category', array(array('category_id', '<>', 0)));
		
		if(sizeof($categories) == 0){
			trigger_error('No categories found');
		}

		//page vars
		$this->onloadscript = "";	
	    $this->page_title = "about your group";
	    $this->menu_item = "add";	
	    $this->show_tracker = true;		
	    $this->tracker_location = 2;			
	    $this->set_focus_control = "txtName";
		$this->assign('group', $this->group);
		$this->assign('categories', $categories);		
		
		$this->display_template();

	}

	//Unbind
	protected function unbind (){
		$this->group->name = strip_tags($this->data['txtName']);
		$this->group->byline = strip_tags($this->data['txtByline']);		
		$this->group->description = strip_tags($this->data['txtDescription'], '<a><em><strong>');				
		$this->group->tags = strip_tags($this->data['txtTags']);
		$this->group->category_id = $this->data['ddlCategory'];
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
		
		if($this->group->category_id == 0 || $this->group->category_id == ''){
			$this->add_warning('Please choose a category for this group');
			$this->add_warn_control('ddlCategory');
			$valid = false;
		}

		//if valid so far, check if this group already exists
		if($valid && $this->group->mode == 'user'){
			$search = factory::create('search');
			$result = $search->search_cached('group', array(array('name', '=', $this->group->name), array('confirmed', '=', true)));

			if(sizeof($result) > 0){
				$link = "javascript:newWindow('" . WWW_SERVER . "/groups/" . $result[0]->url_id . "');";
				$this->add_warning('Someone has already added a group with that name, <a href="' . $link . '">click here to see it</a> (new window)');				
				$valid = false;				
			}
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
