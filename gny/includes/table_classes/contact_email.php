<?php
/**
 * Table Definition for contact_email
 */
require_once('init.php');
require_once 'DB/DataObject.php';

class tableclass_contact_email extends DB_DataObject {
    ###START_AUTOCODE
    /* the code below is auto generated do not remove the above tag */

    public $__table = 'contact_email';                   // table name
    public $contact_email_id;                // int(4)  primary_key not_null
    public $to_email;                        // varchar(150)   not_null
    public $message;                         // text()   not_null
    public $subject;                         // varchar(255)   not_null
    public $from_email;                      // varchar(150)   not_null
    public $from_name;                       // varchar(150)  

    /* Static get */
    function staticGet($k,$v=NULL) { return DB_DataObject::staticGet('tableclass_Contact_email',$k,$v); }

    /* the code above is auto generated do not remove the tag below */
    ###END_AUTOCODE

	public function send(){
		
		//Setup email text
		$smarty = new Smarty();
        $smarty->compile_dir = SMARTY_PATH;
        $smarty->compile_check = true;
        $smarty->template_dir = TEMPLATE_DIR;
		$smarty->assign('text', $this->message);
		$smarty->assign('team_email', CONTACT_EMAIL);		

        $body = $smarty->fetch(TEMPLATE_DIR . '/emails/contact.tpl');

		//send email
		send_text_email($this->to_email, $this->from_name, $this->from_email, $this->subject, $body);
		
	}
}
