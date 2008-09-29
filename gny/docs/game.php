<?php
require_once('../includes/init.php');

class game_page extends pagebase {

	//load
	protected function load (){

	}


	//setup
	protected function setup (){

	}

	//Bind
	protected function bind() {
	
		//get categories for dropdown
		$search = factory::create('search');
		$categories = $search->search_cached('category', array(array('category_id', '<>', 0)));
		
		if(sizeof($categories) == 0){
			trigger_error('No categories found');
		}
		
		// user count, name & email
		$added_count = 0;
		$game_name = session_read('game_name');
		$game_email = session_read('game_email');
		if($game_name == '' || $game_email == ''){
			$game_name = "Anonymous";
			$game_email = "anonymous@groupsnearyou.com";				
		}else{
			
			//get user
			$game_users = $search->search('game_user', array(array('email', '=', $game_email)));

			//get count for this user
			$added_groups = $search->search('game_user', array(array('game_user_id', '=', $game_users[0]->game_user_id)));
			
			$added_count = sizeof($added_groups);
			
		}
		
		
		//page vars
		$this->onloadscript = "setupGame();";	
	    $this->page_title = "Add a group";
	    $this->menu_item = "add";	
	    $this->set_focus_control = "";
		$this->assign('map_js', true);
		$this->assign('google_maps_key', GOOGLE_MAPS_KEY);
		$this->assign('categories', $categories);
		$this->assign('max_map_zoom', MAX_MAP_ZOOM);
		$this->assign('game_name', $game_name);		
		$this->assign('game_email', $game_email);				
		$this->assign('added_count', $added_count);						
		
	
		$this->display_template();
					
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
$game_page = new game_page();

?>
