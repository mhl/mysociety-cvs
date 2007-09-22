<?php
	set_include_path(".:../conf:../includes/:../includes/PEAR:".get_include_path());
	// we need to search one more path up for ajax/ subdirectory
	set_include_path("../../conf:../../includes/:../../includes/PEAR:".get_include_path());

	error_reporting(E_ERROR | E_WARNING | E_PARSE | E_USER_ERROR | E_USER_WARNING | E_USER_NOTICE | E_COMPILE_ERROR | E_CORE_ERROR);

	require_once ('PEAR.php');
	require_once ('general');
	require_once ('element.php');
	require_once ('factory.php');
	require_once ('error_handle.php');
	require_once ('session.php');
	require_once('DB/DataObject.php' );
	require_once('DB/DataObject/Cast.php');	
	require_once ('functions.php');	
	require_once ('pagebase.php');

?>
