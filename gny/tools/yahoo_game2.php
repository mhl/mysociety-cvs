#!/usr/bin/php5
<?php

	require_once(dirname(__FILE__) .'/../conf/general');  
	require_once(dirname(__FILE__) .'/../includes/init.php');
	require_once(dirname(__FILE__) .'/../includes/table_classes/gamegroup.php');	


    //get keyword
    $swiches = getopt('q:');

	$keyword = isset($swiches['q']) ? $swiches['q'] : null;	
	if($keyword == null){
	    print "Please specify a keyword to import groups for. e.g. -q residents \n";
	    exit;
    }

    //grab first page and figure out how many pages there are
    print "cheking number of pages for this keyword \n";
    $html = safe_scrape("http://groups.yahoo.com/search?query=" . urlencode($keyword), 43200);

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
        
        print "scraping page " . $i . "\n";
        
        //get page of results
        $url = "http://groups.yahoo.com/search?query=" . urlencode($keyword) . "&sc=-1&sg=" . $i . "&ss=1";
        
        $html = safe_scrape($url, 43200);
        $link_regex = "/<em><a href=\"\/group\/(.*?)?.*?\">(.*?)<\/a><\/em>/";
	    preg_match_all($link_regex, $html, $link_matches, PREG_PATTERN_ORDER);        
        
        //get the group pages
        foreach ($link_matches[2] as $link_match) {
            
            //build url and check if already imported
            $url = "http://groups.yahoo.com/group/" . trim($link_match);
            $is_imported = tableclass_gamegroup::is_imported($url);
            
            if($is_imported == false){
                
                 print "Scraping " . $link_match . "\n";
                 
                //sleepy time
                $sleep_time = get_random_numbers(1, 1, 15);
                sleep($sleep_time[0]);
                
                //scrape
                $group_html = safe_scrape($url, 3600);
            
                //Title
                $title_regex = "/<span class=\"ygrp-grdescr\">&middot; (.*?)<\/span>/";
    	        preg_match_all($title_regex, $group_html, $title_matches, PREG_PATTERN_ORDER); 
	        
    	        $title = html_entity_decode($title_matches[1][0]);
    	        $title = mk_utf8($title);
    	        if($title == ''){
    	           $title =  $link_match;
	            }
        
    	        //Description
    	        $description_regex = "/<div id=\"ygr_desc\" class=\"group-description\">(.*?)<\/div>/s";
    	        preg_match_all($description_regex, $group_html, $description_matches, PREG_PATTERN_ORDER);             

    	        $description = $description_matches[1][0];
    	        $description = strip_tags($description);
    	        $description = trim($description);
    	        $description = html_entity_decode($description);
    	        $description = str_replace("&#39;", "'", $description);
    	        $description = mk_utf8($description);

                //Category
                $category_regex = "/Category: <a href=\".*?\">(.*?)<\/a>/";
                preg_match_all($category_regex, $group_html, $category_matches, PREG_PATTERN_ORDER);
            
                $category = $category_matches[1][0];

                //Save group
                $game_group_new = factory::create('gamegroup');                
                $game_group_new->name =  $title; //str_replace("_", "", $link_match);
                $game_group_new->by_line = $title;            
                $game_group_new->link = $url;
                $game_group_new->description = $description;
                $game_group_new->category = $category;

                if($game_group_new->name != '' && $game_group_new->by_line != '' && $game_group_new->description != ''){
                    $success = $game_group_new->insert();
                    if($success){
                        print "Saved: " . $title . "\n";
                    }else{
                        print "Failed to save: " . $title . "\n";   
                        print_r($game_group_new);
                        print "\n";
                    }
                }else{
                        print "Failed, missing info: " . $title . "\n";                   
                }
            }else{
                print "Already imported " . $url . "\n";
            }
            
        }
        

    }
	
	
	
?>