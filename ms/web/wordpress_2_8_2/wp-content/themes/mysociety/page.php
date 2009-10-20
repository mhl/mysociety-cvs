<?php get_header(); ?>

	<h1><?php the_title(); ?></h1>
		
	<div class="contentfull">

		<?php if (have_posts()) : while (have_posts()) : the_post();?>
		<div class="post" id="post-<?php the_ID(); ?>">

			<div class="entry">
				<?php the_content('<p class="serif">Read the rest of this page &raquo;</p>'); ?>

				<?php wp_link_pages(array('before' => '<p><strong>Pages:</strong> ', 'after' => '</p>', 'next_or_number' => 'number')); ?>

			</div>
		</div>
		<?php endwhile; endif; ?>
	<?php edit_post_link('Edit this entry.', '<p class="editlink">', '</p>'); ?>
	<?php include (TEMPLATEPATH . '/catposts.php'); ?>
	</div>

<?php

$is_cee_cfp = ($_SERVER['SERVER_NAME'] == 'cee.mysociety.org' && substr($_SERVER['REQUEST_URI'], 0, 5) == '/cfp/');
if ($is_cee_cfp) {
    get_sidebar('cfp');
}
get_footer();

