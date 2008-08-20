<?php 
if (!@include "../conf/general") {
    if (!@include "../../conf/general") {
        if (!@include "../../../conf/general") {
            print "Error including conf/general in wp-config.php on mysociety.org WordPress";
            exit;
        }
    }
}
define('WP_USE_THEMES', true);

if (OPTION_STAGING) {
    // new site
    require('./wp/wp-blog-header.php');
} else {
    // old site XXX remove this in the end
    if (empty($_GET['cat'])) {
        $cat = 1;
    }
    /* Short and sweet */
    require('./wordpress/wp-blog-header.php');    
}

?>
