<?php
/*
Plugin Name: Batch Categories
Version: 1.4
Plugin URI: http://robm.me.uk/projects/plugins/wordpress/batch-categories/
Description: Easily manage the mass categorisation of posts that match various criteria.
Author: Rob Miller
Author URI: http://robm.me.uk/
*/

require_once dirname(__FILE__) . '/admin.php';

$bc_urls = $bc_tagging = null;

function bc_init() {
	global $bc_urls, $wp_version;
	
	$bc_urls = array(
		'admin' => 'edit.php?page=batch_categories',
		'keyword' => 'edit.php?page=batch_categories&s=%s',
		'category' => 'edit.php?page=batch_categories&cat=%s',
		'tag' => 'edit.php?page=batch_categories&t=%s'
	);
}
add_action('plugins_loaded', 'bc_init');

?>