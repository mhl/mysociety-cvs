<?php
require_once('../includes/init.php');

//An alternate confirmed page for adding groups (this one has a form to email other people with groups)
class confirmed2_page extends pagebase {

	//Properties
	protected function load(){
	
	}

	//setup
	protected function setup (){

		//get the link key
		if($_GET['q']){
			$this->viewstate['link_key'] = $_GET['q'];
		}else{
           	throw_404();
		}
		
		//try and get the group, check it is a contact by web type
		$search = factory::create('search');
		$result = $search->search_cached('confirmation', array(array('link_key', '=', $this->viewstate['link_key'])),1);
		$confirmation = null; 
		
		//If we have something, find the group, update it, then delete from the confirmation table
		if(sizeof($result) == 1){
			$confirmation = $result[0];
			$confirmation->delete();
        
			if($confirmation->parent_table == 'groups'){

				//get the group
				$this->viewstate['group_id'] = $confirmation->parent_id;
				$search = factory::create('search');
				$result = $search->search('group', array(array('group_id', '=', $this->viewstate['group_id'])),1);
				$group = null;
				if(sizeof($result) == 1){
					$group = $result[0];
				}else{
					trigger_error("Couldent find group from confirmation ID (setup)");
				}
			
				//update group status to confirmed
				$group->confirmed = true;
				$group->update();

				if ($group->location_desc) {
					# XXX Send email to team@ as this one needs manual locating
					# Some sort of admin interface would be the next step!
				}

				//Update the stats table
				tableclass_stat::increment_stat("group.confirmed.count");
						
			}else{

				throw_404();						
			}
		}
		
		//setup the page to say that no emails have been sent
		$this->viewstate['show_sent'] = false;

	}

	//Bind
	protected function bind() {

		//get the group (we only have it avaliable on setup() otherwise)
		$search = factory::create('search');
		$result = $search->search('group', array(array('group_id', '=', $this->viewstate['group_id'])),1);
		$group = null;
		if(sizeof($result) == 1){
			$group = $result[0];
		}else{
			trigger_error("Couldent find group from confirmation ID (bind)");
		}

		//show the page
		if(!$this->viewstate['show_sent']){
			$this->page_title = "Your group has been added!";
			$this->set_focus_control = "txtEmails";	
			
			//work out the name of the person
			$name_split = explode(' ', $result[0]->created_name);			
			$name = '';
			if(sizeof($name_split) > 0){
				$name = $name_split[0];
			}else{
				$name = $result[0]->created_name;
			}
			$this->assign('name', $name);
			
		}else{
			$this->page_title = "Your email has been sent";
		}
		$this->menu_item = "add";
	
		$this->assign('group', $group);
		$this->assign('show_sent', $this->viewstate['show_sent']);
		$this->assign('organisers_group_url', GROUP_ORGANISERS_GROUP_URL);

		$this->display_template();

	}

	//Unbind
	protected function unbind (){

		
		
	}

	//Validate
	protected function validate (){
	
		$valid = true;
		
		//Emails
		if($this->data['txtEmails'] == ''){
			$this->add_warning($this->smarty->translate('Please enter one or more valid email address seperated by commas'));
			$this->add_warn_control('txtEmails');
			$valid = false;
		}else{
			//check if all the emails entered are valid.
			$emails = explode(",", trim($this->data['txtEmails']));
			$invalid_emails = false;
			foreach($emails as $email){
				if(!valid_email(trim($email))){
					$invalid_emails = true;
					$valid = false;					
				}
			}
			
			if($invalid_emails){
				$this->add_warning($this->smarty->translate('Please enter one or more valid email address seperated by commas'));
				$this->add_warn_control('txtEmails');
				$valid = false;				
			}
		
		}

		//Message
		if($this->data['txtContactMessage'] == ''){
			$this->add_warning('Please enter a message');
			$this->add_warn_control('txtContactMessage');
			$valid = false;
		}		
		
		return $valid;
	}

	//Process page
	protected function process (){

		//if valid, send the emails
		if($this->validate()){
			if($this->viewstate['show_sent'] == false){
				$this->send_emails();
			}
			$this->viewstate['show_sent'] = true;
		}

		$this->bind();
	}
	
	//send the emails
	private function send_emails(){
	
		//get the group (I know, again! none to efficiant this, but its late)
		$search = factory::create('search');
		$result = $search->search('group', array(array('group_id', '=', $this->viewstate['group_id'])),1);
	
		$emails = explode(",", trim($this->data['txtEmails']));
		$invalid_emails = false;
		$title = "Local online groups (" . SITE_NAME . ")";
		foreach($emails as $email){
		
			send_text_email($email, $result[0]->created_name, $result[0]->created_email, $title, $this->data['txtContactMessage']);
		
		}

		//Update the stats table
		tableclass_stat::increment_stat("group.forwarded.count");
			
	}

}

//create class instance
$confirmed2_page = new confirmed2_page();

?>
