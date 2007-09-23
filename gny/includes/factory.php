<?php
/** @internal Set Callback for object unserialization */
ini_set('unserialize_callback_func', 'unserialize_callback_factory');

require_once('table_classes/config.php');
require_once('table_classes/group.php');
require_once('table_classes/country.php');

class factory {

	public static function create ($class_name, $element_id=null, $cache=false, $require_only=false) {
		
		$object = null;

		switch ($class_name) {
			case 'group':
				require_once( 'table_classes/config.php' );
				require_once('table_classes/group.php');
				if (!$require_only) {
					$object = DB_DataObject::factory($class_name);
				}
				break;
			case 'contact_email':
				require_once( 'table_classes/config.php' );
				require_once('table_classes/contact_email.php');				
				if (!$require_only) {
					$object = DB_DataObject::factory($class_name);
				}
				break;				
			case 'confirmation':
				require_once( 'table_classes/config.php' );
				require_once('table_classes/confirmation.php');								
				if (!$require_only) {
					$object = DB_DataObject::factory($class_name);
				}
				break;	
			case 'country':
				require_once( 'table_classes/config.php');
				require_once('table_classes/country.php');								
				if (!$require_only) {
					$object = DB_DataObject::factory($class_name);
				}
				break;
			case 'stat':
				require_once( 'table_classes/config.php' );
				require_once( 'table_classes/stat.php' );				
				if (!$require_only) {
					$object = DB_DataObject::factory($class_name);
				}
				break;									
			case 'group_search':
				require_once('group_search.php');
				if (!$require_only) {
					$object = new group_search();
				}
				break;
			case 'gaze':
				require_once('apis/gaze.php');
				if (!$require_only) {
					$object = new gaze();
				}
				break;		
			case 'search':
				require_once('search.php');
				if (!$require_only) {
					$object = new searcher();
				}
				break;
			case 'json':
				require_once('json.php');
				if (!$require_only) {
					$object = new Services_JSON();
				}				
				break;
							
			// Catch all

			default:
				// This is an unsupported class and is most definatly a major
				// error, but only if we're not doing require_only. This will
				// effect sessions so that they my not be loaded back 100%
				// correctly. This is mainly a hack to stop the PEAR error
				// object from crashing everything as it stores things that
				// have gone wrong, including the page classes which are not
				// part of the factory.
				
				if (!$require_only) {
					trigger_error('Unknown class: ' . $class_name, 'The class that was thrown at this factory method is unknown. Check that you\'re passing the right data or that you haven\'t forgotten to define the class here!');
				}
				else {
					// We'll mention something in the error log as this is an
					// error
					
					error_log('Could not load class ' . $class_name . ' via require_only in teh factory');
				}
				break;
		}
		
		// And if we're here, we should have an object that we can now apply
		// the loading rules to
		
		return factory::load($object, $element_id, $cache);
	}
	
	private static function load($object, $element_id, $cache=false) {
		if (isset($element_id) && ($element_id === 0 || !empty($element_id))) {
			// We need to load data for this item
			$object->element_id = $element_id;
			$object->load($cache);
		}
		
		return $object;
	}
}

/**
 * This function will be called automatically when unserialize attempts to
 * create an object that it doesn't know about. In order for it to do what it
 * needs to do, we need to require the correct file, so we're just going to pass
 * this through the factory which will require what is required (hopefully)
 */
function unserialize_callback_factory($classname) {

	factory::create($classname, null, null, true);
}

?>