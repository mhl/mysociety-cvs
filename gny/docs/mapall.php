<?php
require_once('init.php');

class mapall_page extends pagebase {


	//bind
	function bind() {


        $search = factory::create('search');
		$groups = $search->search('group', array(
			array('long_bottom_left', '<', 1),
			array('long_top_right', '>', -2),
			array('lat_bottom_left', '<', 55),
			array('lat_top_right', '>', 50)	
			),
			'AND'
		);

		$this->assign("groups", $groups);

		$this->display_template();   
        
    }
	
}

//create class instance
$mapall_page = new mapall_page();

?>
