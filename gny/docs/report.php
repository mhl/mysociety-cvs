<?php
require_once('../includes/init.php');

class report_page extends pagebase {

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
	    $this->page_title = "report abuse";
	    $this->menu_item = "search";
	
		if($this->viewstate['show_sent']){
	    	$this->set_focus_control = "txtName";
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
	
		//Name
		if($this->data['txtName'] == ''){
			$this->add_warning('Please enter your name');
			$this->add_warn_control('txtName');
			$valid = false;
		}
		
		//Email
		if($this->data['txtEmail'] == '' || !valid_email($this->data['txtEmail'])){
			$this->add_warning('Please enter a valid email address');
			$this->add_warn_control('txtEmail');
			$valid = false;
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
		
		//build the title
		$subject = EMAIL_PREFIX . "Abuse Report: " . $group->name;
		
		//setup smarty
	    $smarty = new Smarty();
	    $smarty->compile_dir = SMARTY_PATH;
		$smarty->assign("group", $group);
		$smarty->assign("www_server", WWW_SERVER);		
		$smarty->assign("team_email", CONTACT_EMAIL);		
		$smarty->assign("message", $this->data['txtContactMessage']);
		$smarty->assign("user_data", print_r($_SERVER, true));
		
		
		$body = $smarty->fetch(TEMPLATE_DIR . "/emails/abuse.tpl"); 

		send_text_email(CONTACT_EMAIL, $this->data['txtName'], $this->data['txtEmail'], $subject, $body);

	}
	

}

//create class instance
$report_page = new report_page();

?>
