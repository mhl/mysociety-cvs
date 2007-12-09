<?php
require_once('../../includes/init.php');

class searchgroups_page extends pagebase {

	//load
	protected function load (){
		$this->reset_smarty("admin/searchgroups.tpl");
	}

	//setup
	protected function setup (){
		if($_GET['q']){
			$this->viewstate['search'] = $_GET['q'];			
		}
		if($_GET['mode'] && $_GET['mode'] == "saved"){
			$this->add_warning("Changes saved!");
		}
		
	}

	//Bind
	protected function bind() {
		//get any data
		$groups = null;
		if(isset($this->viewstate['search']) && $this->viewstate['search'] != ""){
			
			$search = factory::create('search');
			$groups = $search->search('group', array(
				array('name', 'like', "%"  . $this->viewstate['search'] . "%")),
				'AND',
				array(array("zoom_level", 'DESC'))
				);
		}

		//page vars
		$this->onloadscript = "";	
	    $this->page_title = "Manage groups";
	    $this->menu_item = "edit";
	    $this->set_focus_control = "txtSearch";
		$this->assign("groups", $groups);
		if(isset($this->viewstate['search'])){		
			$this->assign("search", $this->viewstate['search']);
		}

		$this->display_template();
					
	}

	//Unbind
	protected function unbind (){

		if (isset($this->data['txtSearch'])){
			$this->viewstate['search'] = $this->data['txtSearch'];
		}
	}

	//Validate
	protected function validate (){

	}

	//Process page
	protected function process (){
	
		//delete
		if($this->command == "delete" || $this->command == "enable" ||  $this->command == "disable" 
			|| $this->command == "edit"){
			
			//get the group
			$group_id = $this->argument;
			$search = factory::create('search');
			$groups = $search->search('group', array(array('group_id', '=', $group_id)));
			
			//edit, disable or delete the group
			if(sizeof($groups) != 1){
				$this->add_warning("Error deleting group");
			}else{
			
				//delete
				if($this->command == "delete"){
					$groups[0]->delete();
				}

				//disable
				if($this->command == "disable"){
					$groups[0]->confirmed = false;
					$groups[0]->update();
				}
				
				//enable
				if($this->command == "enable"){
					$groups[0]->confirmed = true;
					$groups[0]->update();
				}
				//edit
				if($this->command == "edit"){
				 	$groups[0]->mode = "admin"; // this saves the group without an email confirmation
					session_write('group', $groups[0]);
					redirect(WWW_SERVER . "/add/about/");
				}
			}
		}
	
		$this->bind();
	}

}

//create class instance
$searchgroups_page = new searchgroups_page();

?>

