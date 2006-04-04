<?php get_header(); ?>

	<div id="content" class="narrowcolumn">

	<?php if (have_posts()) : ?>

		<h2 class="pagetitle">Search Results</h2>
		
		<div class="navigation">
			<div class="alignleft"><?php posts_nav_link('','','&laquo; Previous Entries') ?></div>
			<div class="alignright"><?php posts_nav_link('','Next Entries &raquo;','') ?></div>
		</div>


		<?php while (have_posts()) : the_post(); ?>
				
			<div class="post">
				<div class="item_head" id="<?php the_ID(); ?>"><a href="<?php the_permalink() ?>" rel="bookmark" title="Permanent Link to <?php the_title(); ?>"><?php the_title(); ?></a>
				<small><?php the_time('l, F jS, Y') ?></small>
                </div>

				<div class="meta"><?=($cat == 3) ? "Proposed by" : "Posted by"?> <?php the_author() ?>  </div> 
				
				<div class="item">
					<?php the_content() ?>
				</div>
		
				<div class="item_foot"><!--Posted in <?php the_category(', ') ?> <strong>|--></strong> <?php edit_post_link('Edit','','<strong>|</strong>'); ?>  <?php comments_popup_link('No Comments &#187;', '1 Comment &#187;', '% Comments &#187;'); ?></div> 
				
				<!--
				<?php trackback_rdf(); ?>
				-->
			</div>
	
		<?php endwhile; ?>

		<div class="navigation">
			<div class="alignleft"><?php posts_nav_link('','','&laquo; Previous Entries') ?></div>
			<div class="alignright"><?php posts_nav_link('','Next Entries &raquo;','') ?></div>
		</div>
	
	<?php else : ?>

		<h2 class="center">Not Found</h2>
		<?php include (TEMPLATEPATH . '/searchform.php'); ?>

	<?php endif; ?>
		
	</div>

<?php get_sidebar(); ?>

<?php get_footer(); ?>
