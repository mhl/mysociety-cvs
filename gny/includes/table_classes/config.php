<?php
	//define database configuration values
	$options = &PEAR::getStaticProperty('DB_DataObject','options');

	$debug_level = SQL_DEBUG_LEVEL;
	if(isset($_GET['sqldebug'])){
		//$debug_level = $_GET['sqldebug'];
	}


	$options = array(
	'database' => 'mysql://' . OPTION_GNY_DB_USER . ':'. OPTION_GNY_DB_PASS .'@' . OPTION_GNY_DB_HOST . '/' . OPTION_GNY_DB_NAME,
	'schema_location' => INCLUDE_DIR . '/table_classes/',
	'class_location' => INCLUDE_DIR . '/table_classes/',
	'require_prefix' => 'DataObjects/',
	'class_prefix' => 'tableclass_',
	'db_driver' => 'MDB2',
	'ini_' . OPTION_GNY_DB_NAME => INCLUDE_DIR . '/table_classes/groups.ini',	
	"debug" => $debug_level
	);
?>
