<?php
/*
Template Name: Mysociety2008 Home
*/
?>

<?php get_header(); ?>

	<div id="content" class="fullcolumn">

		<?php $count=0; if (have_posts()) : while (have_posts()) : the_post(); $count++ ?>
		<?php if ($count > 1) break; ?>
					<?php the_content('<p class="serif">Read the rest of this page &raquo;</p>'); ?>
		<?php endwhile; endif; ?>
		<?php edit_post_link('Edit this entry.', '<p class="editlink">', '</p>'); ?>

	</div>
<?php get_footer(); ?>