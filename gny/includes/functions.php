<?php

	require_once('HTTP/Request.php');
	require_once('cache.php');
	
	//Send a text email
    function send_text_email($to, $from_name, $from_email, $subject, $body){
        
    	$headers  = 'MIME-Version: 1.0' . "\r\n";
		$headers .= 'Content-type: text/plain; charset=iso-8859-1' . "\r\n";
		$headers .= 'From: ' . $from_name. ' <' . $from_email . ">\r\n";
		    
		mail($to, $subject, $body, $headers);

    }

	//Valid email address?
    function valid_email ($string) {
        $valid = false;
    	if (!ereg('^[-!#$%&\'*+\\./0-9=?A-Z^_`a-z{|}~]+'.
    		'@'.
    		'[-!#$%&\'*+\\/0-9=?A-Z^_`a-z{|}~]+\.'.
    		'[-!#$%&\'*+\\./0-9=?A-Z^_`a-z{|}~]+$', $string)) {
    		$valid = false;
    	} else {
    		$valid =  true;
    	}
    	
    	return $valid;
    }

	//Valid URL?
	function valid_url($url) {
		return preg_match("/^(http(s?):\\/\\/|ftp:\\/\\/{1})((\w+\.)+)\w{2,}(\/?)$/i", $url);
	}

	function raw_urls_to_links($text){
	
		//replace strings with http etc
		$return = preg_replace('/(\s|^)(http(s?):\\/\\/|ftp:\\/\\/{1})((\w+\.)+)\w{2,}(\/?)/i', '<a href="$0">$0</a>', 
			$text); 
			
		$return = preg_replace('/(\s|^)((\w+\.)+)\w{2,}(\/?)/i', '<a href="http://$0">$0</a>', 
			$return);	
			
		return $return;
	
	}

	//is a postcode?
	function is_postcode ($postcode) {
		// See http://www.govtalk.gov.uk/gdsc/html/noframes/PostCode-2-1-Release.htm

		$in  = 'ABDEFGHJLNPQRSTUWXYZ';
		$fst = 'ABCDEFGHIJKLMNOPRSTUWYZ';
		$sec = 'ABCDEFGHJKLMNOPQRSTUVWXY';
		$thd = 'ABCDEFGHJKSTUW';
		$fth = 'ABEHMNPRVWXY';
		$num = '0123456789';
		$nom = '0123456789';
		$gap = '\s\.';	

		if (	preg_match("/^[$fst][$num][$gap]*[$nom][$in][$in]$/i", $postcode) ||
				preg_match("/^[$fst][$num][$num][$gap]*[$nom][$in][$in]$/i", $postcode) ||
				preg_match("/^[$fst][$sec][$num][$gap]*[$nom][$in][$in]$/i", $postcode) ||
				preg_match("/^[$fst][$sec][$num][$num][$gap]*[$nom][$in][$in]$/i", $postcode) ||
				preg_match("/^[$fst][$num][$thd][$gap]*[$nom][$in][$in]$/i", $postcode) ||
				preg_match("/^[$fst][$sec][$num][$fth][$gap]*[$nom][$in][$in]$/i", $postcode)
			) {
			return true;
		} else {
			return false;
		}
	}

	//is a postcode?
	function is_partial_postcode ($postcode) {
		// See http://www.govtalk.gov.uk/gdsc/html/noframes/PostCode-2-1-Release.htm

		$in  = 'ABDEFGHJLNPQRSTUWXYZ';
		$fst = 'ABCDEFGHIJKLMNOPRSTUWYZ';
		$sec = 'ABCDEFGHJKLMNOPQRSTUVWXY';
		$thd = 'ABCDEFGHJKSTUW';
		$fth = 'ABEHMNPRVWXY';
		$num = '0123456789';
		$nom = '0123456789';
		$gap = '\s\.';	

		if (	preg_match("/^[$fst][$num]$/i", $postcode) ||
				preg_match("/^[$fst][$num][$num]$/i", $postcode) ||
				preg_match("/^[$fst][$sec][$num]$/i", $postcode) ||
				preg_match("/^[$fst][$sec][$num][$num]$/i", $postcode) ||
				preg_match("/^[$fst][$num][$thd]$/i", $postcode) ||
				preg_match("/^[$fst][$sec][$num]$/i", $postcode)
			) {
			return true;
		} else {
			return false;
		}
	}

	function pad_partial_postcode($partial_postcode){

		$partial_postcode = strtolower($partial_postcode);
		if($partial_postcode == "sw1" || $partial_postcode == "ec1"){
			$return = $partial_postcode . "a 1aa";
		}elseif($partial_postcode == "sw9"){
			$return = $partial_postcode . "8jx";		
		}else{
			$return = $partial_postcode . " 1aa";
		}
				
		return $return;
		
	}

	//iszip code
	function is_zipcode ($zipcode) {

		if (preg_match("/[0-9]{5}/", $zipcode)) {
			return true;	
		} else {
			return false;
		}
	}
	
	//Does a stig look like a long/lat value
	function is_longlat ($longlat) {

		$return = true;
		$split = explode(",", $longlat);
		if(sizeof($split) != 2){
			$return = false;
		}else{
			if (!is_numeric(str_replace("-", "", $split[0]))){
				$return = false;
			}
			if (!is_numeric(str_replace("-", "", $split[1]))){
				$return = false;
			}
		}
		
		return $return;

	}

	//clean postcode (adds space and makes uppcase)
	function clean_postcode ($postcode) {

		$postcode = str_replace(' ','',$postcode);
		$postcode = strtolower($postcode);

		$reg = array();
		$postcode = trim($postcode);
		preg_match('/^(.+?)([0-9][a-z]{2})$/',$postcode, $reg);
	
		$clean_postcode = trim($reg[1]) . ' ' . trim($reg[2]);
		$clean_postcode = strtoupper($clean_postcode);
	
		return $clean_postcode;

	}

	//clean postcode (adds space and makes uppcase)
	function postcode_to_district ($postcode) {

		$reg = array();
		$postcode = trim($postcode);
		preg_match('/^(.+?)([0-9][a-z]{2})$/',$postcode, $reg);
	
		$clean_postcode = trim($reg[1]);
		$clean_postcode = strtoupper($clean_postcode);

		return $clean_postcode;

	}

	//Get a location (uses a google maps proxy)
	function get_postcode_location($zip, $country){

		$url = "http://geo.localsearchmaps.com/?zip={zip}&country={country}";
		$url = str_replace('{zip}', urlencode($zip), $url);
		$url = str_replace('{country}', urlencode($country), $url);

		$data = safe_scrape_cached($url);
		return process_emag_geocoder($data);
	}

	//Get a location (uses a google maps proxy)
	function get_place_location($place, $country, $street = null){		

		//try the city search (for outside the us)
		$url = "http://geo.localsearchmaps.com/?city={place}&country={country}";
		$url = str_replace('{place}', urlencode($place), $url);
		$url = str_replace('{country}', urlencode($country), $url);
		if(isset($street)){
			$url .= "&street=" . urlencode($street);
		}

		//TODO: implement the US location search
		//http://geo.localsearchmaps.com/?loc=1600+Amphitheatre+Parkway,+Mountai n+View+CA++94043

		$data = safe_scrape_cached($url);
		return process_emag_geocoder($data);
	}
	
	
	//process results from http://geo.localsearchmaps.com/
	function process_emag_geocoder($data){
		if (strpos($data, 'location not found') > -1){
			$return = false;
		}else{
			$return = array();

			//very hacky this, but hay, ho im in a hurry
			$data = str_replace('map.centerAndZoom(new GPoint(', '', $data);
			$data = str_replace(')', '', $data);
			$data = str_replace(';', '', $data);
			$exploded = explode(',', $data);

			$return[0] = trim($exploded[0]) + 0; //+0 to cast as number
			$return[1] = trim($exploded[1]) + 0;			

		}		
		return $return;
	}

	//Tiny url
    function tiny_url($url,$length=30){

    	// make nasty big url all small
    	if (strlen($url) >= $length){
    		$tinyurl = @file ("http://tinyurl.com/api-create.php?url=$url");
    		
    		if (is_array($tinyurl)){
    			$tinyurl = join ('', $tinyurl);
    		} else {
    			$tinyurl = $url;
    		}
    	} else {  
    		$tinyurl = $url; 
    	}

    	return $tinyurl;
    }

    //Google maps url
    function googlemap_url_from_postcode($postcode, $zoom = 15){
        $postcode = strtolower(str_replace(" ", "+", $postcode));
        return "http://maps.google.co.uk/maps?q=$postcode&z=$zoom";
    }

	//Scarpe a url and cache it
    function safe_scrape_cached($url){

		$cache = cache::factory();

		$cached = $cache->get($url);
		if (isset($cached) && $cached !== false) {
			return $cached;
		}else{
			$page = safe_scrape($url);
		    $cache->set($url, $page, "safe_scrape");	
			return $page;
		}
		
	}	

	//Scrape a url
    function safe_scrape($url){
        $page = "";
        for ($i=0; $i < 3; $i++){ 
            if($page == false){
                 if (SCRAPE_METHOD == "PEAR"){
                     $page = scrape_page_pear($url);
                 }else{
                     $page = scrape_page_curl($url);         
                 }
            }   
        }
        return $page;
    }
    
	//scrape by pear
    function scrape_page_pear($url){
        $page = "";
        $request = new HTTP_Request($url, array("method" => "GET"));
        $request->sendRequest();
        $page = $request->getResponseBody();
        
        return $page;

    }
    
	//scrape by curl
    function scrape_page_curl($url) {
		$ch = curl_init($url);
		curl_setopt($ch,CURLOPT_RETURNTRANSFER,TRUE);
		curl_setopt($ch,CURLOPT_FOLLOWLOCATION,TRUE);
		return curl_exec($ch);
	}

	function safe_string($object){
		return $object . '';
	}

	//Redirect page to a URL
	function redirect ($url){
	    header("Location: $url");
		exit;
	}

	//Throw 404
	function throw_404(){
		header("HTTP/1.0 404 Not Found");
		exit;
	}

	//Format a string for a url
	function format_string_for_url($string) {
		$string = ereg_replace('&', 'and', $string);
		$string = ereg_replace("'", '', $string);
		$string = ereg_replace(' ', '_', $string);
		$string = strtolower(iconv("UTF-8", "ASCII//TRANSLIT", $string));
		return $string;
	}

	///////////////////////////////
	// Cal's functions from
	// http://www.iamcal.com/publish/article.php?id=13

	// Call this with a key name to get a GET or POST variable.
	function get_http_var ($name, $sanitize=true, $default=null){
		//global $HTTP_GET_VARS, $HTTP_POST_VARS;
		if (array_key_exists($name, $_POST)) {
			return mk_utf8(clean_var($_POST[$name], $sanitize));
		}
		if (array_key_exists($name, $_GET)) {
			return mk_utf8(clean_var($_GET[$name], $sanitize));
		}
	
		return $default;
	}

	/**
	 * Take a string and make it utf8 if it isn't already (it should be though)
	 */
	function mk_utf8($string) {
		return (is_utf8($string) ? $string : utf8_encode($string));
	}

	function clean_var ($a, $sanitize=true){
		$out = (ini_get("magic_quotes_gpc") == 1) ? recursive_strip($a) : $a;
	
		if ($sanitize) {
			// We want to filter out all kinds of nasty shit that a user might
			// have thrown at us.
		
			// Filtering commented out at the moment as it seems to be causing
			// problems on the dev site.
			//return filter_var($out, FILTER_SANITIZE_STRING, FILTER_FLAG_NO_ENCODE_QUOTES);	
			return $out;
		}
		else {
			return $out;
		}
	}

	function recursive_strip ($a){
		if (is_array($a)) {
			while (list($key, $val) = each($a)) {
				$a[$key] = recursive_strip($val);
			}
		} else {
			$a = StripSlashes($a);
		}
		return $a;
	}

	function is_utf8($str) {
		if ($str === mb_convert_encoding(mb_convert_encoding($str, "UTF-32", "UTF-8"), "UTF-8", "UTF-32")) {
			return true;
		} else {
			return false;
		}
	}

	//Approximate zoom level for a google map based on 2 longitude values
	function approximate_gmap_zoom($long_left, $long_right){

		$width = $long_left - $long_right;
		if($width < 0){
			$width = $width / -1;
		}
	
		$width = floor($width);

		$zoom = 0;
		if($width <= 1){
			$zoom = 8;
		}elseif($width <= 3){
			$zoom = 7;
		}elseif($width <= 5){
			$zoom = 6;
		}elseif($width <= 15){
			$zoom = 5;	
		}else{
			$zoom = 3;
		}

		return $zoom;
	}
	
	function vardump($bla) {
		print '<pre style="text-align: left">';
		var_dump($bla);
		print '</pre>';
	}
	// Format a date to mysql format
	function mysql_date($date){
	    return date("Y-m-d H::i:s", $date);
	}

	// very inacurate way of converting distance to a point on latitude	
	function distance_to_latitude($distance_km){
		$km_per_degree = 111;
		return $latitude + ($distance_km / $km_per_degree);
	}
	
	// very inacurate way of converting distance to a point on longitude
	function distance_to_longitude($distance_km){
		$km_per_degree = 111.321;
		return $distance_km / $km_per_degree;
	}
	
?>