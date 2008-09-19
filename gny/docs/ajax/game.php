<?php

	require_once('../../includes/init.php');

	//get mode
	$mode = get_http_var('mode');
	
	if($mode == 'get'){
		get_group();
	}
	
	if($mode == 'save'){
		save_group();
	}
	
	if($mode == 'notlocal'){
		not_local();
	}
	
	//make as non local
	function not_local(){
		$hash = get_http_var('hash');
		
		if(isset($hash) && $hash != ''){

			$search = factory::create('search');
			$game_groups = $search->search('gamegroup', 
				array(
					array('guid', '=', $hash), 
					array('matched', '=', 0)
				));

			if(sizeof($game_groups) == 1){
				$game_group = $game_groups[0];
				$game_group->notlocal = true;
				$game_group->update();
			}else{
				$success = false;
				error_log('couldent frind game group from guid');
			}			
		}
	}
	
	//get a random group
	function get_group(){

		//get a random group
		$search = factory::create('search');
		$game_groups = $search->search('gamegroup', 
			array(
				array('notlocal', '=', 0), 
				array('matched', '=', 0)
			),
			'AND',
			array(array('RAND()', 'ASC')),
			1);

		//make into array for tidyness
		$return = array();
		$return['id'] = $game_groups[0]->guid;
		$return['name'] = $game_groups[0]->name;	
		$return['by_line'] = $game_groups[0]->by_line;			
		$return['link'] = $game_groups[0]->link;		
		$return['description'] = $game_groups[0]->description;
		$return['category'] = $game_groups[0]->category;	
	
		$json = factory::create('json');
		print $json->encode($return);

	}
	
	function save_group(){

		$success = true;

		//get the hash value and try and find the group for it
		$hash = get_http_var('hash');
		$game_group = null;
		
		if(isset($hash) && $hash != ''){

			$search = factory::create('search');
			$game_groups = $search->search('gamegroup', 
				array(
					array('guid', '=', $hash), 
					array('matched', '=', 0)
				));
				
			if(sizeof($game_groups) == 1){
				$game_group = $game_groups[0];
			}else{
				$success = false;
				error_log('couldent frind game group from guid');
			}			
		}else{
			$success = false;
				error_log('no guid passed');			
		}

		//validate we have all the data we need
		if($success){

			//get other http vars
			$category_id = get_http_var('category_id');
			$game_detail = get_http_var('game_detail');
			$game_tags = get_http_var('game_tags');			
			$lat_bottom_left = get_http_var('lat_bottom_left');						
			$lat_centroid = get_http_var('lat_centroid');						
			$lat_top_right = get_http_var('lat_top_right');						
			$long_bottom_left = get_http_var('long_bottom_left');						
			$long_centroid = get_http_var('long_centroid');																		
			$long_top_right = get_http_var('long_top_right');																								
			$zoom_level = get_http_var('zoom_level');
			$name = get_http_var('name');			
			$email = get_http_var('email');						

			//bit more valudation (shoudl really be in the group object I know ...)																							
			if(!is_numeric($long_bottom_left) || !is_numeric($lat_bottom_left) 
				|| !is_numeric($long_top_right) || !is_numeric($lat_top_right) 
				|| !is_numeric($long_centroid) || !is_numeric($lat_centroid ) 
				|| !is_numeric($zoom_level)){
					
					$success = false;
					error_log('location data not numeric');
			}
			
			//zoom level (already been checked in js)
			if($zoom_level < MAX_MAP_ZOOM){
				$success = false;
				error_log('zoom level too wide');				
			}
			
			//check if it already exists ion teh database
			$existing_group = $search->search('group', 
				array(array('involved_link', '=', $link)));
				
			if(sizeof($existing_group) != 0){
				$success = false;
				error_log('duplicate');				
			}
			
			//create new group
			if($success){
				$group = factory::create('group');
				$group->name = $game_group->name;
				$group->byline = $game_group->by_line;
				$group->description = raw_urls_to_links(new_lines_to_paragraphs($game_detail));
				$group->category_id = $category_id;
				$group->tags = $game_tags;
				$group->involved_type = "link";
				$group->involved_link = $game_group->link;
				$group->created_name = (isset($name) ? $name :"Anonymous");
				$group->created_email = (isset($email) ? $email : "anonymous@groupsnearyou.com");
				$group->confirmed = true;
				$group->long_bottom_left = $long_bottom_left;
				$group->lat_bottom_left = $lat_bottom_left;
				$group->long_top_right = $long_top_right;
				$group->lat_top_right = $lat_top_right;
				$group->zoom_level = $zoom_level;
				$group->long_centroid = $long_centroid;
				$group->lat_centroid = $lat_centroid;			
				$group->set_url_id();

				//save
				$success = $group->insert();
			
			}
		}

		//create / get user
		$users = factory::create('search');
		$game_users = $search->search('game_user', 
			array(
				array('email', '=', $email)
			));
			
		$game_user = null;
		if(sizeof($game_users) > 0){
			$game_user = $game_users[0];
		}else{
			$game_user	= factory::create('game_user');
			$game_user->name = $name;
			$game_user->email = $email;
			$game_user->insert();
		}

		//mark game group as done
		if($success){
			$game_group->matched = true;
			$game_group->game_user_id  = $game_user->game_user_id;
			$game_group->update();
		}
		

		if($success){
			print "true";
		}else{
			print "false";			
		}

	}
?>