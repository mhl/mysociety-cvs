<?php

require_once('cache.php');
	
//basic search wrapper for DB_DataObjects
class searcher {

	//search cached
	public function search_cached ($class_name, $where_clauses, $clause_join = 'AND', $order_clauses = null,
		$number=null, $start=null) {

		$return = false;

		//build up the cache key
		$key = $class_name . print_r($where_clauses, true) . $clause_join . 
			print_r($order_clauses, true) . $number . $start;

		//check the cache
		$cache = cache::factory();
		$cached = $cache->get($key, "search");
		//if we have something in the cache, grab that, if not do the query as normal
		if (isset($cached) && $cached !== false) {
			$return = $cached;
		}else{
			$return = $this->search($class_name, $where_clauses, $clause_join, $order_clauses, $number, $start);
		}

		//cache
		$cached = $cache->set($key, $return, "search");
		if($cached == false){
			trigger_error("Failed to cache database call");
		}

		//return
		return $return;
	}

	//search
	public function search ($class_name, $where_clauses, $clause_join = 'AND', $order_clauses = null,
		$number=null, $start=null) {

		$return = array();

		//create search object
		$search_object = factory::create($class_name);

		//create where clauses
		foreach($where_clauses as $where_clause) {
			
			$quote = "'";
			if(is_numeric($where_clause[2])){
				$quote = "";
			}

			$search_object->whereAdd($where_clause[0] . " " . $where_clause[1] . " " . $quote . 
				$search_object->escape($where_clause[2]) . $quote, $clause_join);
		}

		//create order by's
		if(isset($order_clauses)){
			foreach($order_clauses as $order_clause) {
				$search_object->orderBy($order_clause[0] . " " . $order_clause[1]);
			}		
		}

		//Limit / paging
		if (isset($number) && isset($start)) {
			$search_object->limit($number, $start);
		}elseif (isset($number)) {
			$search_object->limit($number);		
		}

		//get search count and grab any objects
		$search_count = $search_object->find();
		$found_objects = array();
		if($search_count > 0){
			while($search_object->fetch()){
				array_push($found_objects, clone($search_object));
			}
			$return = $found_objects;
		}

		
		return $return;
	}
	
}

?>