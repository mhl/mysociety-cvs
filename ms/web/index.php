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

require('./wp/wp-blog-header.php');

?>
