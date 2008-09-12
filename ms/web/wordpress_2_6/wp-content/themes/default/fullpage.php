<?php
/*
Template Name: Full width
*/
?>

<?php get_header(); ?>

	<h1><?php the_title(); ?></h1>
	<div class="contentfull">

		<?php if (have_posts()) : while (have_posts()) : the_post(); ?>
				<?php the_content('<p class="serif">Read the rest of this page &raquo;</p>'); ?>

				<?php wp_link_pages(array('before' => '<p><strong>Pages:</strong> ', 'after' => '</p>', 'next_or_number' => 'number')); ?>

		<?php endwhile; endif; ?>
	
	
		<?php edit_post_link('Edit this entry.', '<p class="editlink">', '</p>'); ?>

	</div>

<?php get_footer(); ?>