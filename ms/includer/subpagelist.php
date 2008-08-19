<?php
$pages = get_pages('echo=0&child_of=' . get_the_ID());
    foreach ($pages as $page_obj) {
        $page = get_object_vars($page_obj);
        $url = '/' .  get_page_uri($page['ID']);
        $url;
        //$keys = array_keys($page);
        //print_r($keys);
?> 
<h4><a href="<?php print $url;?>"><?php print $page[post_title]; ?></a></h4>
<?php print $page[post_excerpt]; ?>
<?php  
} // end projects list

 ?>
