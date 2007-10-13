<?php
require_once('../includes/init.php');

class confirmed_page extends pagebase {

	//Properties
	private $contact_email = null;

	protected function load(){
	
	}

	//setup
	protected function setup (){

		if($_GET['q']){
			$this->viewstate['link_key'] = $_GET['q'];
		}else{
                	throw_404();
		}

	}

	//Bind
	protected function bind() {

		//try and get the group, check it is a contact by web type
		$search = factory::create('search');
		$result = $search->search('confirmation', array(array('link_key', '=', $this->viewstate['link_key'])),1);
		$confirmation = null; 
		if(sizeof($result) == 1){
			$confirmation = $result[0];
		}else{
			throw_404();
        }

		//handle different confirmation types
		if($confirmation->parent_table == 'contact_email'){
		
			//send the email
			$contact_email = factory::create('contact_email');
			$contact_email->get($confirmation->parent_id);
			$contact_email->send();
			$contact_email->delete();

			//show page
	    	$this->page_title = "your email has been sent";					
	    	$this->menu_item = "search";				
			$this->assign('title', "Your email has been sent");			
			$this->assign('text', "Hopefully someone from that group will contact you soon.");						
			$this->assign('link', WWW_SERVER);
			$this->assign('link_text', "Want to search for another group?");

			//Update the stats table
			tableclass_stat::increment_stat("contactemail.confirmed.count");

		}elseif($confirmation->parent_table == 'groups'){

			/* REDIRECT TO USE ALTERNATE CONFIRMED PAGE */
			/* have left the code below incase we want to treat it as normal at a later date */
			redirect(WWW_SERVER . "/confirmed2.php?q=" . $this->viewstate['link_key']);
			
			/*
			//get the group
			$group_id = $confirmation->parent_id;
			$search = factory::create('search');
			$result = $search->search('group', array(array('group_id', '=', $group_id)),1);
			$group = null;
			if(sizeof($result) == 1){
				$group = $result[0];
			}else{
				trigger_error("Couldent find group from confirmation ID");
			}
			
			//update group status to confirmed
			$group->confirmed = true;
			$group->update();

			//show the page
	    	$this->page_title = "your group has been added";					
	    	$this->menu_item = "add";
	    	$this->set_focus_control = "txtEmails";	

			$this->assign('show_forward', true);			
			$this->assign('title', "Your group has been added!");			
			$this->assign('text', "We have set up an email group for people who organise groups like yours.");						
			$this->assign('link', GROUP_ORGANISERS_GROUP_URL);
			$this->assign('link_text', "Click here to join the group organisers email group.");

			//Update the stats table
			tableclass_stat::increment_stat("group.confirmed.count");
			*/			
		}else{
			throw_404();						
		}

		$this->display_template();

		$confirmation->delete();		

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
$confirmed_page = new confirmed_page();

?>
