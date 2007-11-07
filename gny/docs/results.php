<?php

require_once('../includes/init.php');
require_once('group_search.php');

class results_page extends pagebase {

	//Properties
	private $mode = "";
	private $query = "";
	private $query_display_text = "";
	private $place_name = "";

	//load
	protected function load(){

		$query = get_http_var('q');
		if(isset($query) && $query != ''){
			$this->query = get_http_var('q');
			$this->mode = group_search::get_search_type($this->query);
			
			//if we are in placename mode, we need to send them to the gaze pge to verify they get the right place
			if ($this->mode == 'placename') {
				redirect('/location/' . urlencode($this->query));
				exit;
			} elseif ($_SERVER['SCRIPT_NAME'] == '/results.php') {
				redirect('/search/' . urlencode($this->query));
				exit;
			}

			//if a display version of the query has been passed in, use that
			$query_display_text = get_http_var('t');
			if(isset($query_display_text) && $query_display_text != ''){
				$this->query_display_text = $query_display_text;
				$this->place_name = $query_display_text;
			}else{
				$this->query_display_text = $this->query;
			}
			
		}else{
			$this->mode = "all";
		}
	
	}

	//setup
	protected function setup (){
		
	}

	//Bind
	protected function bind() {

		if($this->mode == 'all'){
			//everntually we need to display everything and do paging. for teh moment just throw a 404
			throw_404();
		}
		
		
		if($this->mode == 'postcode' || $this->mode == 'zipcode'|| $this->mode == 'longlat'){
			//do the search
			$group_search = factory::create('group_search');
			$groups = $group_search->search($this->query);
			
			//copy over any warnings
			if(sizeof($group_search->warnings) > 0){
				$this->warnings = $group_search->warnings;
			}
		}

		//page vars
		$this->onloadscript = "";	
	    $this->page_title = "Search results for " . $this->query_display_text;
	    $this->menu_item = "search";	
	    $this->set_focus_control = "txtSearch";
		$this->rss_link = WWW_SERVER . "/rss.php?" . $_SERVER["QUERY_STRING"];
			
		$this->assign('groups', $groups);
		$this->assign('query', $this->query);
		$this->assign('query_display_text', $this->query_display_text);
		$this->assign('place_name', $this->place_name);

		$this->display_template();
		
	}

	//Unbind
	protected function unbind (){
			
	}

	//Validate
	protected function validate (){
	
		$valid = true;
		
		return $valid;
	}

	//Process page
	protected function process (){
		$this->bind();
	}

}

//create class instance
$results_page = new results_page();

?>
