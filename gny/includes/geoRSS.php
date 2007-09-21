<?php

/*
	This is a really basic couple of classes for reading geoRSS feeds. It currently only supports point data.
	You use it like this:
	$geo_rss = new geo_rss_feed();
	$geo_rss->load_from_url('http://www.planningalerts.com/api.php?call=postcode&postcode=sw98jx&area_size=l');
	
*/

   require_once ('init.php');
   require_once ("PEAR/HTTP/Request.php");     
	class geoRSS {
	
		public $title ="";		
		public $link = "";
		public $description = "";				
		public $geo_rss_items;
	
		public function __construct(){
		
			$this->items = array();
			
		}
		
		public function load_from_url($url){
			$xml = safe_scrape_cached($url);
		   	return $this->load_from_string($xml);
		}
		
		public function load_from_string($xml){

			//TODO: add validation of georss feed
			$success = false;
			$parsed = simplexml_load_string($xml);
			if ($parsed != false){
				$success = true;
				
				$namespaces = $parsed->getNamespaces(true);

				$this->title = safe_string($parsed->channel->title);
				$this->link = safe_string($parsed->channel->link);
				$this->title = safe_string($parsed->channel->title);	
				$this->description = safe_string($parsed->channel->description);

				if(sizeof($parsed->channel->item) > 0){
					foreach($parsed->channel->item as $item) {
						$geo_rss_item = new geo_rss_item();
						$geo_rss_item->title = safe_string($item->title);
						$geo_rss_item->guid = safe_string($item->guid);
						$geo_rss_item->point = safe_string($item->point);	

						// process the georss stuff
						if (isset($namespaces['georss'])) {
							$geo = $item->children($namespaces['georss']);
							list($lat, $lng) = split(' ', (string) $geo->point);
							$geo_rss_item->lat = $lat;
							$geo_rss_item->lng = $lng;
							
							$geo_rss_item->featurename = trim((string) $geo->featurename);
							
						}
						elseif (isset($namespaces['geo'])) {
							$geo = $item->children($namespaces['geo']);
							$geo_rss_item->lat = (float) $geo->lat;
							$geo_rss_item->lng = (float) $geo->long;
						}
						$geo_rss_item->description = safe_string($item->description);
						$geo_rss_item->link = safe_string($item->link);
						$geo_rss_item->comments = safe_string($item->comments);
						$geo_rss_item->date = strtotime(safe_string($item->pubDate));	
						
						//add to the list											
						array_push($this->items, $geo_rss_item);
					}
				}
			}
			
			return $success;			
		}
	}
	
	class geo_rss_item{
		public $title ="";
		public $guid = "";
		public $featurename = "";
		public $point = "";
		public $lat = "";		
		public $lng = "";				
		public $description = "";				
		public $link = "";
		public $comments = "";			
	}
	
?>