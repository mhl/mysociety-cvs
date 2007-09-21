<?php
/**
 * Table Definition for groups
 */
require_once('init.php');
require_once 'DB/DataObject.php';

class tableclass_group extends DB_DataObject {
    ###START_AUTOCODE
    /* the code below is auto generated do not remove the above tag */

    public $__table = 'groups';                          // table name
    public $group_id;                        // int(4)  primary_key not_null
    public $name;                            // varchar(150)   not_null
    public $byline;                          // text()   not_null
    public $description;                     // text()   not_null
    public $tags;                            // text()  
    public $involved_type;                   // varchar(50)   not_null
    public $involved_link;                   // varchar(150)  
    public $created_name;                    // varchar(100)   not_null
    public $created_date;                    // timestamp()   not_null default_CURRENT_TIMESTAMP
    public $created_email;                   // varchar(100)   not_null
    public $confirmed;                       // tinyint(1)   not_null
    public $long_bottom_left;                // float()   not_null
    public $lat_bottom_left;                 // float()   not_null
    public $long_top_right;                  // float()   not_null
    public $lat_top_right;                   // float()   not_null
    public $zoom_level;                      // int(4)   not_null
    public $long_centroid;                   // float()   not_null
    public $lat_centroid;                    // float()   not_null
    public $url_id;                          // varchar(150)   not_null
    public $involved_email;                  // varchar(150)  

    /* Static get */
    function staticGet($k,$v=NULL) { return DB_DataObject::staticGet('tableclass_Groups',$k,$v); }

    /* the code above is auto generated do not remove the tag below */
    ###END_AUTOCODE

	public function set_url_id(){
	
		//set the default (remove spaces and dodgy chars)
		$url_id = format_string_for_url($this->name);
	
		//if we've somehow ended up with a zero length string, then just give it a number
		if($url_id == ''){
			$search = factory::create('search');
			$search_result = $search->search('group', array(array('group_id', '>', 1)),'AND' ,
				array(array('group_id', 'DESC'), 1));
			$url_id = $search_result[0]->id;
		}

		//check if its been taken
		$url_id_taken = true;
		$postfix = '';
		$loop_count = 0; //we only want to loop 5 times. more than than its gone pear shaped
		while($url_id_taken == true && $loop_count <=5) {

			$search = factory::create('search');
			$search_result = $search->search('group', array(array('url_id', '=', $url_id . $postfix)));
			if($search_result == false){
				$url_id_taken = false;
			}else{
				if($postfix == ''){
					$postfix = 1;
				}else{
					$postfix ++;
				}
				$url_id	.= '_' . $postfix;
			}
			$loop_count ++;
		}

		if($url_id_taken == true){
			trigger_error("Unable to create a unique url id for group: " . $this->name);
		}else{
			$this->url_id = $url_id . $postfix;	
		}

	}
}
