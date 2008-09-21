<?php
/**
 * Table Definition for a user
 */
require_once('init.php');
require_once 'DB/DataObject.php';

class tableclass_gamegroup  extends DB_DataObject{

    public $__table = 'game_group';
    public $game_group_id;
    public $name;
    public $by_line;
    public $link;
    public $category;
    public $description;
    public $notlocal;
    public $game_user_id;
    public $matched;
    public $guid;

    /* Static get */
    function staticGet($k,$v=NULL) { return DB_DataObject::staticGet('tableclass_gamegroup',$k,$v); }

	/* Definition */
   function table() {
        return array(
            'game_group_id'   	=> DB_DATAOBJECT_INT + DB_DATAOBJECT_NOTNULL,
            'name'   	=> DB_DATAOBJECT_STR + DB_DATAOBJECT_NOTNULL,
            'by_line'   	=> DB_DATAOBJECT_STR + DB_DATAOBJECT_NOTNULL,
            'link'     		=> DB_DATAOBJECT_STR + DB_DATAOBJECT_NOTNULL,
            'category'     		=> DB_DATAOBJECT_STR,
            'description'   => DB_DATAOBJECT_STR + DB_DATAOBJECT_TXT,
            'notlocal'   		=> DB_DATAOBJECT_INT + DB_DATAOBJECT_BOOL,
            'game_user_id' => DB_DATAOBJECT_INT,
            'matched'   		=> DB_DATAOBJECT_INT + DB_DATAOBJECT_BOOL,
            'guid'     		=> DB_DATAOBJECT_STR + DB_DATAOBJECT_NOTNULL,
        );
    }

	/* Keys */
    function keys() {
        return array('game_group_id');
    }

	function insert(){
		
		$return = false;
		
		$this->guid = uniqid();
		
		//check is not already imported into game_group
		$search = factory::create('search');
		$game_groups = $search->search('gamegroup', 
			array(array('link', '=', $this->link)));
		
		//check not already in main group table
		$groups = $search->search('group', 
			array(array('involved_link', '=', $this->link)));

		if(sizeof($game_groups) == 0 && sizeof($groups) == 0){
			print "ready to save \n";
			$return = parent::insert();
		}else{
			 print "exists \n"
		}
		
		return $return;
	}
	
	public static function is_imported($url){

		$search = factory::create('search');
		$game_groups = $search->search('gamegroup', 
			array(array('link', '=', $url)));

		return sizeof($game_groups) > 0;
	}

}