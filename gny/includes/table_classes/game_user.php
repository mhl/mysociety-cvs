<?php
/**
 * Table Definition for a game user
 */
require_once('init.php');
require_once 'DB/DataObject.php';

class tableclass_game_user  extends DB_DataObject{

    public $__table = 'game_user';
    public $game_user_id;
    public $name;
    public $email;


    /* Static get */
    function staticGet($k,$v=NULL) { return DB_DataObject::staticGet('tableclass_game_user',$k,$v); }

	/* Definition */
   function table() {
        return array(
            'game_user_id'   	=> DB_DATAOBJECT_INT + DB_DATAOBJECT_NOTNULL,
            'name'   	=> DB_DATAOBJECT_STR + DB_DATAOBJECT_NOTNULL,
            'email'     		=> DB_DATAOBJECT_STR + DB_DATAOBJECT_NOTNULL
        );
    }

	/* Keys */
    function keys() {
        return array('game_user_id');
    }

}