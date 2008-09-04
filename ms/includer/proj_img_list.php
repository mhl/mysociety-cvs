<?php

//query_posts('cat=7&orderby=title&order=asc&posts_per_page=-1');
$pages = get_pages('child_of=403&echo=0&sort_column=menu_order');
foreach ($pages as $page_obj) {
    $page = get_object_vars($page_obj);
    $url = '/' .  get_page_uri($page['ID']) . '/';
    //$keys = array_keys($page);
    //print_r($keys);
    $imageurl = '';
    if (file_exists(dirname(__FILE__) . '/../web/contimg/projtns/' . str_replace(" ", "-", strtolower($page['post_title']) . '.jpg'))) {
        $imageurl = '/contimg/projtns/' . str_replace(" ", "-", strtolower($page['post_title'])) . '.jpg';
    }

    echo '<div class="projects-entry">';
    echo '<h3><a href="', $url, '">';
    if ($imageurl) {
        echo '<img src="', $imageurl, '" alt="" title="', $page['post_title'], ' screenshot" width="125" height="126" class="size-thumbnail" border="0" />';
    }
    echo $page['post_title'], '</a></h3>', $page['post_excerpt'], ' <a href="', $url, '">Find out more&hellip;</a></div>';
} // end projects list

