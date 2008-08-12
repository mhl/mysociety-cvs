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

if (OPTION_STAGING == '1') {
    require('./wp/wp-blog-header.php');
    print "staging";
} else {
    if (empty($_GET['cat'])) {
        $cat = 1;
    }
/* Short and sweet */
    require('./wordpress/wp-blog-header.php');    
    print "live";
}

?>
