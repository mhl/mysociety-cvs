<?php
query_posts('cat=7&orderby=title&order=asc&posts_per_page=-1');
$pages = get_pages('child_of=403&echo=0');
    foreach ($pages as $page_obj) {
        $page = get_object_vars($page_obj);
        $url = '/' .  get_page_uri($page['ID']);
        $url;
        //$keys = array_keys($page);
        //print_r($keys);
?> 
<h4><a href="<?php print $url;?>"><?php print $page[post_title]; ?></a></h4>
<p><?php print $page[post_excerpt]; ?></p>


<?php  
} // end projects list

 ?>



