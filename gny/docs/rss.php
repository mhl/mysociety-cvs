<?php

require_once('../includes/init.php');
require_once('group_search.php');

class rss_page extends pagebase {

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

			//if a display version of the query has been passed in, use that
			$query_display_text = get_http_var('t');
			if(isset($query_display_text) && $query_display_text != ''){
				$this->query_display_text = $query_display_text;
				$this->place_name = $query_display_text;
			}else{
				$this->query_display_text = $this->query;
			}
			
			
			//if we are in placename mode, we need to 404, (sorry!)
			if($this->mode == 'placename'){
//				throw_404();
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

		//get categories
		$search = factory::create('search');
		$categories = $search->search_cached('category', array(array('category_id', '<>', 0)));

		if($this->mode == 'all'){
//			throw_404();
		}
		
		$groups = array();
		if($this->mode == 'postcode' || $this->mode == 'zipcode'|| $this->mode == 'longlat'){
			//do the search
			$group_search = factory::create('group_search');
			list($groups, $long, $lat) = $group_search->search($this->query);

			//copy over any warnings
			if(sizeof($group_search->warnings) > 0){
				$this->warnings = $group_search->warnings;
			}
		}

		foreach ($groups as $group) {
			$group->category = $categories[$group->category_id]->name;
		}

		//page vars
		$this->onloadscript = "";	
	    $this->page_title = "Search results for " . $this->query_display_text;
	    $this->menu_item = "search";
		$this->assign('groups', $groups);
		$this->assign('categories', $categories);
		$this->assign('query', $this->query);
		$this->assign('search_link', WWW_SERVER . '/search/' . urlencode($this->query));
		$this->assign('query_display_text', $this->query_display_text);
		$this->assign('place_name', $this->place_name);		
		
		header('Content-Type: application/xml; charset=utf-8');
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
$rss_page = new rss_page();

?>
