<?php

# Copy of the lines from WP main index.php, so it can be in subdirectory
define('WP_USE_THEMES', true);
include_once 'cfp/wp-config.php';

print wp_list_categories('title_li=&show_count=0');

