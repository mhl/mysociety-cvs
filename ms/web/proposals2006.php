<?php 
if (empty($_GET['cat'])) {
    $cat = 3;
}
/* Short and sweet */
define('WP_USE_THEMES', true);
require('wordpress/wp-blog-header.php');
?>
