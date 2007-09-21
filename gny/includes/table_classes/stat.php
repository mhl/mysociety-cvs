<?php
/**
 * Table Definition for stat
 */
require_once('init.php');
require_once 'DB/DataObject.php';

class tableclass_stat extends DB_DataObject 
{
    ###START_AUTOCODE
    /* the code below is auto generated do not remove the above tag */

    public $__table = 'stat';                            // table name
    public $stat_id; 
    public $stat_key;                        // varchar(100)   not_null
    public $stat_value;                      // varchar(100)   not_null

    /* Static get */
    function staticGet($k,$v=NULL) { return DB_DataObject::staticGet('tableclass_Stat',$k,$v); }

    /* the code above is auto generated do not remove the tag below */
    ###END_AUTOCODE

	public static function increment_stat($stat_key){

		if(RECORD_STATS){
			//Update the stats table
			$search = factory::create('search');
			$stat_result = $search->search('stat', array(array('stat_key', '=', $stat_key)));

			//save
			if($stat_result != false && sizeof($stat_result) == 1){
				$stat = &factory::create('stat');
				$stat->stat_value = $stat_result[0]->stat_value + 1;
				$stat->whereAdd("stat_key = '" . $stat_key . "'");				
				$stat->update(false, true);
			}else{
				$stat = factory::create('stat');
				$stat->stat_key = $stat_key;
				$stat->stat_value = 1;
				$stat->insert();				
			}
		}

	}
}
