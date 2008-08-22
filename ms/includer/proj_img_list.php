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

<div class="projects-entry">

<?php  if ($imageurl) { ?>
<h2><a href="<?=$url ?>"><img src="<?php print $imageurl ?>" alt="" title="<?php print $page['post_title']; ?> screenshot" width="125" height="126" class="size-thumbnail" border="0" /><?=$page['post_title'] ?></a></h2>
<?php } else { ?>
<h2><a href="<?=$url ?>"><?=$page['post_title'] ?></a></h2>
<?php }  ?>

<?=$page['post_excerpt'] ?>
</div>

 
<?php
} // end projects list
 ?>



