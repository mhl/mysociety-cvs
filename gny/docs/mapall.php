<?php

require_once('../includes/init.php');

class mapall_page extends pagebase {


	//bind
	function bind() {

        $search = factory::create('search');
		$groups = $search->search('group', array(
			array('long_bottom_left', '<', 1.7666667),
			array('long_top_right', '>', -8.1),
			array('lat_bottom_left', '<', 60.7833333),
			array('lat_top_right', '>', 49.1738889)	
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
