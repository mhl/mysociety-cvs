<?php
//query_posts('cat=7&orderby=title&order=asc&posts_per_page=-1');
$pages = get_pages('child_of=403&echo=0');
    foreach ($pages as $page_obj) {
        $page = get_object_vars($page_obj);
        $url = '/' .  get_page_uri($page['ID']) . '/';
        //$keys = array_keys($page);
        //print_r($keys);
        $imageurl = '';
        if (file_exists(dirname(__FILE__) . '/../web/contimg/projtns/' . strtolower($page['post_title']) . '.jpg')) {
            $imageurl = '/contimg/projtns/' . strtolower($page['post_title']) . '.jpg';
        }

?> 

<?php  if ($imageurl) {

?>
<div class="projects-entry">
<div class="wp-caption alignleft"><a href="<?php print $url;?>"><img src="<?php print $imageurl ?>" alt="" title="<?php print $page['post_title']; ?> screenshot" width="125" height="126" class="size-thumbnail" border="0" /></a>
</div>

<h2><a href="<?php print $url;?>"><?php print $page['post_title']; ?></a></h2>
<?php print $page['post_excerpt']; ?>
</div>

<?php } 
} // end projects list

 ?>



