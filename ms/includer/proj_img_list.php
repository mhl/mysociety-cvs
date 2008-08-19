<?php
query_posts('cat=7&orderby=title&order=asc&posts_per_page=-1');
$pages = get_pages('child_of=403&echo=0');
    foreach ($pages as $page_obj) {
        $page = get_object_vars($page_obj);
        $url = '/' .  get_page_uri($page['ID']);
        $url;
        //$keys = array_keys($page);
        //print_r($keys);
        $imageurl = '';
        if (file_exists(dirname(__FILE__) . '/../web/contimg/projtns/' . strtolower($page[post_title]) . '.jpg')) {
            $imageurl = '/contimg/projtns/' . strtolower($page[post_title]) . '.jpg';
        }

?> 

<?php  if ($imageurl) { 

?>
<div class="wp-caption alignleft" style="width: 129px"><a href="<?php print $url;?>">
<img src="<?php print $imageurl ?>" alt="image of <?php print $page[post_title]; ?>" title="<?php print $page[post_title]; ?>" width="125" height="126" class="size-thumbnail" border="0"/></a>
<p class="wp-caption-text"><?php print $page[post_title]; ?></p></div>

<h4><a href="<?php print $url;?>"><?php print $page[post_title]; ?></a></h4>
<?php print $page[post_excerpt]; ?>

<hr />
<?php } 
} // end projects list

 ?>



