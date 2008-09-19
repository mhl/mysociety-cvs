<?php
require_once('../includes/init.php');
require_once('table_classes/stat.php');
	
class addstart_page extends pagebase {

	//Bind
	protected function bind() {

		//get number mapped so far
		$search = factory::create('search');
		$game_groups = $search->search_cached('gamegroup', 
			array( 
				array('matched', '=', 1)
			));
		
		// count of users	
		$game_users = $search->search_cached('game_user', 
			array( 
				array('1', '=', 1)
			));			
		
		$game_name = session_read('game_name');
		$game_email = session_read('game_email');

		//page vars
	    $this->page_title = "Add a group";
	    $this->menu_item = "add";
		$this->assign("match_count", sizeof($game_groups));
		$this->assign("user_count", sizeof($game_users));	
		$this->assign("league_table", $this->get_league_table());			
		$this->assign('game_name', $game_name);		
		$this->assign('game_email', $game_email);
		
		$this->display_template();

	}
	
	protected function process (){

		//add email and name to seession if entered
		if(isset($this->data['txtName']) && $this->data['txtName'] != ''
			&& isset($this->data['txtEmail']) && $this->data['txtEmail'] != ''){			
			session_write("game_name", $this->data['txtName']);
			session_write("game_email", $this->data['txtEmail']);
		}
		
		redirect(WWW_SERVER . "/game.php");
		
	}
	
	//get top mappers
	private function get_league_table(){
		
		$return = null;
		$cache = cache::factory();
		$cached = $cache->get("league_table", "search");
		
		if (isset($cached) && $cached !== false) {
			$return = $cached;
		}else{

			//no cache, get from DB
			$game_user = factory::create('game_user');
			$game_user->query("select game_user.name, count(game_group_id) as mapped from game_user inner join game_group on game_user.game_user_id = game_group.game_user_id group by game_user.name order by count(game_group_id) DESC");

			$league_table = array();

			while($game_user->fetch()){

				array_push($league_table, array("name" => $game_user->name, "mapped" => $game_user->mapped));
			}
			
			$return = $league_table;
		}
		
		//return
		return $return;
	}

}

//create class instance
$addstart_page = new addstart_page();

?>
