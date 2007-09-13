<?php
function indent_recommendations($content) {
    $content = preg_replace("/\<p\>\<strong\>What NEED does this meet\?\<\/strong\>\<\/p\>(.*)<p><strong>What is the APPROACH?(.*)$/is", "\\1", $content);
    return $content;
}
if ($cat == 3) 
    add_filter('the_content', 'indent_recommendations');
?>

<?php get_header(); ?>


	<div id="content" class="narrowcolumn">

		<?php if (have_posts()) : ?>

		 <?php $post = $posts[0]; // Hack. Set $post so that the_date() works. ?>
<?php /* If this is a category archive */ if (is_category()) { ?>				
        <?php print category_description($cat);?>
		
 	  <?php /* If this is a daily archive */ } elseif (is_day()) { ?>
		<h2 class="pagetitle">Archive for <?php the_time('F jS, Y'); ?></h2>
		
	 <?php /* If this is a monthly archive */ } elseif (is_month()) { ?>
		<h2 class="pagetitle">Archive for <?php the_time('F, Y'); ?></h2>

		<?php /* If this is a yearly archive */ } elseif (is_year()) { ?>
		<h2 class="pagetitle">Archive for <?php the_time('Y'); ?></h2>
		
	  <?php /* If this is a search */ } elseif (is_search()) { ?>
		<h2 class="pagetitle">Search Results</h2>
		
	  <?php /* If this is an author archive */ } elseif (is_author()) { ?>
		<h2 class="pagetitle">Author Archive</h2>

		<?php /* If this is a paged archive */ } elseif (isset($_GET['paged']) && !empty($_GET['paged'])) { ?>
		<h2 class="pagetitle">Blog Archives</h2>

		<?php } ?>


<!--		<div class="navigation">
			<div class="alignleft"><?php posts_nav_link('','','&laquo; Previous Entries') ?></div>
			<div class="alignright"><?php posts_nav_link('','Next Entries &raquo;','') ?></div>
		</div>
        -->

		<?php while (have_posts()) : the_post(); ?>
		<div class="post">
				<div class="item_head" id="post-<?php the_ID(); ?>"><a
                href="<?php the_permalink() ?>" rel="bookmark"
                title="Permanent Link to <?php the_title(); ?>"><?php
                the_title(); ?></a></div>

                <div class="meta">
                    <?=($cat == 3) ? "Proposed by" : "Posted by"?> <?php the_author() ?>,
		    <?php the_time('jS F Y')?>
                </div>
				
				<div class="item">
					<?php the_content() ?>
				</div>
		
				<div class="item_foot"><!--Posted in <?php the_category(',
                ') ?> <strong>|</strong> -->
                <? if ($cat ==3 ) { ?>
                <a href="<?php the_permalink() ?>">Read full proposal &#187</a> |
                <? } ?>
            <?php

                edit_post_link('Edit','','<strong>|</strong>'); ?>
                <?php comments_popup_link('No Comments &#187;', '1
                Comment &#187;', '% Comments &#187;'); ?></div> 
				
				<!--
				<?php trackback_rdf(); ?>
				-->
			</div>
	
		<?php endwhile; ?>

		<div class="navigation">
            <? if ($cat ==3 ) { ?>
			<div class="alignleft"><?php
			# XXX: Very ugly, but I can't find a better way - basically copy posts_nav_link and subfunctions
			#      Trying ob_* didn't work at all
			$nxtlabel = '&laquo; Older Proposals';
			$prelabel = 'Newer Proposals &raquo;';
			if (! is_single()) {
				if (get_query_var('what_to_show') == 'posts') {
					preg_match('#FROM (.*) GROUP BY#', $request, $matches);
					$fromwhere = $matches[1];
					$numposts = $wpdb->get_var("SELECT COUNT(ID) FROM $fromwhere");
					$max_page = ceil($numposts / $posts_per_page);
				} else {
					$max_page = 999999;
				}
				if ($max_page > 1) {
					if ($paged > 1) {
						$nextpage = intval($paged) - 1;
						if ($nextpage < 1) $nextpage = 1;
						echo '<a href="';
						echo str_replace('index.php', 'proposals2006/view', get_pagenum_link($nextpage));
						echo '">'. $prelabel .'</a>';
					}
					print '</div> <div class="alignright">';
					if (!$paged)
						$paged = 1;
					$nextpage = intval($paged) + 1;
					if ($nextpage <= $max_page) {
						echo '<a href="';
						echo str_replace('index.php', 'proposals2006/view', get_pagenum_link($nextpage));
						echo '">'. $nxtlabel .'</a>';
					}

				}
			}
			?></div>
            <? } else { ?>
			<div class="alignleft"><?php posts_nav_link('','','&laquo; Older Posts') ?></div>
			<div class="alignright"><?php posts_nav_link('','Newer Posts &raquo;','') ?></div>
            <? } ?>
		</div>
	
	<?php else : ?>

		<h2 class="center">Not Found</h2>
		<?php include (TEMPLATEPATH . '/searchform.php'); ?>

	<?php endif; ?>
		
	</div>

<?php get_sidebar(); ?>

<?php get_footer(); ?>
