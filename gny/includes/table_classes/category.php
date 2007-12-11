<?php
/**
 * Table Definition for country
 */
require_once('init.php');
require_once 'DB/DataObject.php';

class tableclass_category extends DB_DataObject 
{
    ###START_AUTOCODE
    /* the code below is auto generated do not remove the above tag */

    public $__table = 'category';                         // table name
    public $category_id;
    public $name;
    public $hint;
    public $url_id;


    /* Static get */
    function staticGet($k,$v=NULL) { return DB_DataObject::staticGet('tableclass_Category',$k,$v); }

    /* the code above is auto generated do not remove the tag below */
    ###END_AUTOCODE
}
