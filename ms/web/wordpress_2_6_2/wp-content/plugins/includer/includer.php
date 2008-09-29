<?php
/*
Plugin Name: Includer
Plugin URI: http://www.mysociety.org/wpgoodies/includer
Description: includes files from the web directory
Version: 1.0
Author: angie@mysociety.org
Author URI: http://www.mysociety.org
*/

/*  Copyright 2008   UK Citizens Online Democracy  (email : angie@mysociety.org) http://www.mysociety.org

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Affero General Public License for more details.

Information about the GNU Affero GPL: 
http://www.fsf.org/licensing/licenses/agpl-3.0.html
*/

function includer_path_callback($content) {
    $pattern = '#(?:<p>)?<!-- includer:(.*)-->(?:</p>)?#';
    return preg_replace_callback(
        $pattern,
        get_includer_contents,
        $content
    );
}

function get_includer_contents($matches) {
    $path = '../includer/' . trim($matches[1]);

    if (is_file($path)) {
        ob_start();
        include $path;
        $contents = ob_get_contents();
        ob_end_clean();
        return $contents;
	}
    return '';
}

//Hook function
add_filter('the_content', 'includer_path_callback');
?>