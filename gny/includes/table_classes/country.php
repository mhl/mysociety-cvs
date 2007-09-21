<?php
/**
 * Table Definition for country
 */
require_once('init.php');
require_once 'DB/DataObject.php';

class tableclass_country extends DB_DataObject 
{
    ###START_AUTOCODE
    /* the code below is auto generated do not remove the above tag */

    public $__table = 'country';                         // table name
    public $iso;                             // char(2)  primary_key not_null
    public $name;                            // varchar(80)   not_null
    public $printable_name;                  // varchar(80)   not_null
    public $iso3;                            // char(3)  
    public $numcode;                         // smallint(2)  
    public $disabled;                        // tinyint(1)  

    /* Static get */
    function staticGet($k,$v=NULL) { return DB_DataObject::staticGet('tableclass_Country',$k,$v); }

    /* the code above is auto generated do not remove the tag below */
    ###END_AUTOCODE
}
