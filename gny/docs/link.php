<?php

	$redirect = get_http_var('q');

	if(isset($redirect) || $redirect == ''){
		throw_404();
	}
	
	if(!valid_url($redirect)){
		trigger_error("Tried to redirect to an invalid url on link.php: " . $redirect);
		throw_404();	
	}

	//Update the stats table
	tableclass_stat::increment_stat("linkredirect.count");
	
	//redirect
	redirect($redirect);

?>