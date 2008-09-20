#!/usr/bin/php5
<?php

	require_once(dirname(__FILE__) .'/../conf/general');  
	require_once(dirname(__FILE__) .'/../includes/init.php');


    //get keyword
    $swiches = getopt('q:');

	$keyword = isset($swiches['q']) ? $swiches['q'] : null;	
	if($keyword == null){
	    print "Please specify a keyword to import groups for. e.g. -q residents \n";
	    exit;
    }


    //grab first page and figure out how many pages there are
    print "cheking number of pages for this keyword \n";
    $html = safe_scrape("http://groups.yahoo.com/search?query=" . urlencode($keyword));

    $count_regex = "/<em>1 - 10<\/em> of ([0-9]*?) &nbsp;/";

	preg_match_all($count_regex, $html, $count_matches, PREG_PATTERN_ORDER);
	$count = 0;
	if($count_matches[1][0]){
	    $count = $count_matches[1][0];
	}else{
	    print "Something went wrong counting number of pages \n";
	    exit;
    }

    //loop through pages
    for ($i=0; $i <= $count; $i += 10) { 
        
        //sleepy time
        $sleep_time = get_random_numbers(1, 1, 60);
        sleep($sleep_time[0]);
        
        
        $url = "http://groups.yahoo.com/search?query=" . urlencode($keyword) . "&sc=-1&sg=" . $i . "&ss=1";
        
        $html = safe_scrape($url);
        $link_regex = "/<em><a href=\"\/group\/(.*?)?.*?\">(.*?)<\/a><\/em>/";
	    preg_match_all($link_regex, $html, $link_matches, PREG_PATTERN_ORDER);        
        
        //get the group pages
        foreach ($link_matches[2] as $link_match) {
            
            print "Scraping " . $link_match . "\n";
            
            $url = "http://groups.yahoo.com/group/" . $link_match;
            
            $group_html = safe_scrape($url);
            
            //Title
            $title_regex = "/<span class=\"ygrp-grdescr\">&middot; (.*?)<\/span>/";
	        preg_match_all($title_regex, $group_html, $title_matches, PREG_PATTERN_ORDER); 
	        
	        $title = html_entity_decode($title_matches[1][0]);
	        
	        //Description
	        $description_regex = "/<div id=\"ygr_desc\" class=\"group-description\">(.*?)<\/div>/s";
	        preg_match_all($description_regex, $group_html, $description_matches, PREG_PATTERN_ORDER);             

	        $description = $description_matches[1][0];
	        $description = strip_tags($description);
	        $description = trim($description);
	        $description = html_entity_decode($description);

            //Category
            $category_regex = "/Category: <a href=\".*?\">(.*?)<\/a>/";
            preg_match_all($category_regex, $group_html, $category_matches, PREG_PATTERN_ORDER);
            
            $category = $category_matches[1][0];

            //Save group
            $game_group = factory::create('gamegroup');
            $success = $game_group->insert();
            $game_group->name =  $title; //str_replace("_", "", $link_match);
            $game_group->by_line = $title;            
            $game_group->link = $url;
            $game_group->description = $description;
            $game_group->category = $category;
          
            if($game_group->name != '' && $game_group->by_line != '' && $game_group->description != ''){
                $success = $game_group->insert();
                if($success){
                    print "Saved: " . $title . "\n";
                }else{
                    print "Failed: " . $title . "\n";   
                }
            }else{
                    print "Failed: " . $title . "\n";                   
            }
            
        }
        

    }
	
	
	
?>