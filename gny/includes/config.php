<?php
	// $Id: config.php,v 1.1 2007-09-21 06:49:59 richard Exp $

	// Copy me to config.php for a good time
	
	error_reporting(E_ERROR | E_WARNING | E_PARSE | E_USER_ERROR | E_USER_WARNING | E_USER_NOTICE | E_COMPILE_ERROR | E_CORE_ERROR);
	
	define('DEVSITE', true);
	
	// Paths
	define('VHOST_DIR', '/data/vhost');
	define('ROOT_DIR', VHOST_DIR . '/groups');
	define('INCLUDE_DIR', ROOT_DIR . '/includes');
	define('PEAR_DIR', INCLUDE_DIR . '/PEAR');
	define('DATA_DIR', ROOT_DIR . '/data');
	define('DOC_DIR' , ROOT_DIR . '/docs');
	define('TMP_DIR', ROOT_DIR . '/tmp');
	define('LOG_DIR', ROOT_DIR . '/logs');
	define('SMARTY_PATH', DATA_DIR . '/smarty_compile');
	define('TEMPLATE_DIR', ROOT_DIR . '/templates');	
	define('CACHE_DIR', DATA_DIR . '/cache');
	
    define('PERMISSIONS_DIR', 0774);
    define('PERMISSIONS_FILE', 0664);

	define('CACHE_TIME', 3600);
	define('DB_CACHE_EXPIRE', 3600);	

    define('SCRAPE_METHOD', 'PEAR');

	// Define the database details
		
	define('DB_HOST', 'localhost');
	define('DB_NAME', 'groups');
	define('DB_USER', 'root');
	define('DB_PASS', '');
	
	//urls
    define("WWW_SERVER", "http://localhost.groups"); 
    define("DOMAIN", "localhost.groups"); 

	//confirmation
    define("CONFIRMATION_BASE_URL", WWW_SERVER . '/confirm.php?q=');
    define("CONFIRMATION_EMAIL", 'confirm@' . DOMAIN);

	//Email titles
    define("EMAIL_PREFIX", '[groupsnearyou.com] ');	

	//Email addresses
	define("CONTACT_EMAIL", 'team@' . DOMAIN);	
    
    //Site name
    define("SITE_NAME", "GroupsNearYou.com"); 
    define("SITE_TAG_LINE", "meet your neighbours");     

	define ('DATETIMEFORMAT_SQL',	"Y-m-d H:i:s"); // 2006-06-02 12:23:23

    define('SESSION_COOKIE_LIFETIME', 0);
    define('SESSION_COOKIE_PATH', '/');
    define('SESSION_COOKIE_DOMAIN', null);

	//map stuff
	define('GOOGLE_MAPS_KEY', 'ABQIAAAA74qlSxRXDySLggVC9lWIbBRZ23lQiKJoYl1qG9qMQzGE6aRjpxTpe5_nu420ZAj3HJ5rHZu7QefTzA');
    define('MAX_MAP_ZOOM', 11);

	//email addresses
	define('GROUP_ORGANISERS_GROUP_URL', 'http://groups.google.com/group/groupsnearyou/');
	
	//Stats
	define('RECORD_STATS', true);
	

?>