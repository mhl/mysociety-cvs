<?php

get_header();

if (have_posts()) : ?>

	<h1 class="pagetitle">mySociety blog</h1>
	<div class="contentwide">

<?php
    if (is_category('Projects')) {
        $posts = query_posts($query_string . '&orderby=title&order=asc&posts_per_page=-1');
    }

    while (have_posts()) : the_post();
    
        //exclude call for proposals
        if ( !in_category('29') ) {
    
?>
		<div class="post dividerbottom">
				<h3 id="post-<?php the_ID(); ?>"><a href="<?php the_permalink() ?>" rel="bookmark" title="Permanent Link to <?php the_title_attribute(); ?>"><?php the_title(); ?></a></h3>
				<small><?php the_time('l, F jS, Y') ?> by <strong><?php the_author() ?></strong></small>

				<div class="entry">
					<?php the_content() ?>
				</div>

				<p class="postmetadata"><?php the_tags('Tags: ', ', ', '<br />'); ?> Posted in <?php the_category(', ') ?> | <?php edit_post_link('Edit', '', ' | '); ?>  <?php comments_popup_link('No Comments &#187;', '1 Comment &#187;', '% Comments &#187;'); ?></p>

			</div>
		<?php } ?>
		<?php endwhile; ?>

		<div class="navigation">
			<div class="alignleft"><?php next_posts_link('&laquo; Older Entries') ?></div>
			<div class="alignright"><?php previous_posts_link('Newer Entries &raquo;') ?></div>
		</div>
	</div>

<?php else : ?>

	<div class="contentfull">
		<h2 class="center">Not Found</h2>
		<?php include (TEMPLATEPATH . '/searchform.php'); ?>
	</div>

<?php endif;
	
get_sidebar();
echo '<br class="clear"/>';
get_footer();
