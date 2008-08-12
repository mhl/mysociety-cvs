<?php
if(is_plugin_page()) {
    load_plugin_textdomain('includer', 'wp-content/plugins/includer');
    $location = get_option('siteurl') . '/wp-admin/admin.php?page=includer/options.php';

//Load the config
include("option_init.php");
//Main Option Page
}
?>
