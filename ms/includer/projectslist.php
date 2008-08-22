<?php
//query_posts('cat=7&orderby=title&order=asc&posts_per_page=-1');

$pages = get_pages('child_of=403&echo=0');
echo '<ul id="project_list">';
foreach ($pages as $page_obj) {
    $page = get_object_vars($page_obj);
    $url = '/' .  get_page_uri($page['ID']) . '/';
    echo '<li><a href="', $url, '">', $page['post_title'], '</a></li>';
} // end projects list
echo '</ul>';

