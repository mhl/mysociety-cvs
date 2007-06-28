<?php get_header(); ?>

<?php print category_description($cat);?>
    <div class="item_foot"></div>

	<div id="content" class="narrowcolumn">

	<?php if (have_posts()) : ?>
		
		<?php while (have_posts()) : the_post(); ?>
				
			<div class="post">
				<div class="item_head" id="post-<?php the_ID(); ?>"><a
                href="<?php the_permalink() ?>" rel="bookmark"
                title="Permanent Link to <?php the_title(); ?>"><?php
                the_title(); ?></a></div>
				<div class="meta"><?=($cat == 3) ? "Proposed by" : "Posted by"?> <?php the_author() ?>, <?php the_time('jS F Y')?> </div> 
					
				<div class="item">
					<?php the_content('Read the rest of this entry &raquo;'); ?>
                </div>
		
				<div class="item_foot">
                    <?php the_category(',
                    ') ?> <strong>|</strong> <?php
                    edit_post_link('Edit','','<strong>|</strong>'); ?>
                    <?php comments_popup_link('No Comments &#187;', '1
                    Comment &#187;', '% Comments &#187;'); ?>	
                    <!-- <?php trackback_rdf(); ?> -->
				</div>
			</div>
	
		<?php endwhile; ?>

		<div class="navigation">
			<div class="alignleft"><?php posts_nav_link('','','&laquo; Previous Entries') ?></div>
			<div class="alignright"><?php posts_nav_link('','Next Entries &raquo;','') ?></div>
		</div>
		
	<?php else : ?>

		<h2 class="center">Not Found</h2>
		<p class="center"><?php _e("Sorry, but you are looking for something that isn't here."); ?></p>
		<?php include (TEMPLATEPATH . "/searchform.php"); ?>

	<?php endif; ?>

	</div>

<?php get_sidebar(); ?>

<?php get_footer(); ?>
