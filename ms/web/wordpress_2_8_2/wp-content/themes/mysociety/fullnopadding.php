<?php
/*
Template Name: Full width, no padding
*/
?>
<?php get_header(); ?>
		<h1><?php the_title(); ?></h1>
		<?php $count=0; if (have_posts()) : while (have_posts()) : the_post(); $count++ ?>
		<?php if ($count > 1) break; ?>
					<?php the_content('<p class="serif">Read the rest of this page &raquo;</p>'); ?>
		<?php endwhile; endif; ?>
		<?php edit_post_link('Edit this entry.', '<p class="editlink">', '</p>'); ?>

<?php get_footer(); ?>