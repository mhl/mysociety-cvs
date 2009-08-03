<?PHP
// START project category blog entries
    $uri = $_SERVER['SCRIPT_URL'];
    preg_match('#^/projects/(.*?)/#', $uri, $matches);
    $catname = $matches[1];
    $categories =  get_categories();
    $hasblog = 0;
    foreach ($categories as $cat) {
    if ($cat->category_nicename == $catname) {
        $posts = query_posts('category_name=' . $catname . '&orderby=date&order=desc&posts_per_page=-1');
        $hasblog = 1;
    }
}

    if ($hasblog) {
// print 'id is ' . $post->get_id;
 ?>

    <hr />
        <h2>Blog entries for <?php print single_cat_title(''); ?></h2>
		<?php while (have_posts()) : the_post(); 
?>
		<div class="post">
		 
				<h3 id="post-<?php the_ID();  ?>"><a href="<?php the_permalink() ?>" rel="bookmark" title="Permanent Link to <?php the_title_attribute(); ?>"><?php the_title(); ?></a></h3>
				<small><?php the_time('l, F jS, Y') ?> by <strong><?php the_author() ?></strong></small>

				<div class="entry">
					<?php the_content() ?>
				</div>

				<p class="postmetadata"><?php the_tags('Tags: ', ', ', '<br />'); ?> Posted in <?php the_category(', ') ?> | <?php edit_post_link('Edit', '', ' | '); ?>  <?php comments_popup_link('No Comments &#187;', '1 Comment &#187;', '% Comments &#187;'); ?></p>

			</div>

		<?php endwhile; ?>

		<div class="navigation">
			<div class="alignleft"><?php next_posts_link('&laquo; Older Entries') ?></div>
			<div class="alignright"><?php previous_posts_link('Newer Entries &raquo;') ?></div>
		</div>
    <?php }  
        // END project category blog entries
    ?>
