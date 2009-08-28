<?php get_header(); ?>
		<?php if (have_posts()) : ?>

 	  <?php $post = $posts[0]; // Hack. Set $post so that the_date() works. ?>
 	  <?php /* If this is a category archive */ if (is_category()) { ?>
 	      <?php if(!in_category(29)){ ?>
		      <h1 class="pagetitle">mySociety blog &raquo; <?php single_cat_title(); ?></h1>
		  <?php }else{ ?>
		      <h1 class="pagetitle"><?php single_cat_title(); ?></h1>		      
		  <?php } ?>		        
 	  <?php /* If this is a tag archive */ } elseif( is_tag() ) { ?>
		<h1 class="pagetitle">mySociety blog &raquo; posts tagged &#8216;<?php single_tag_title(); ?>&#8217;</h1>
 	  <?php /* If this is a daily archive */ } elseif (is_day()) { ?>
		<h1 class="pagetitle">mySociety blog &raquo; archive for <?php the_time('F jS, Y'); ?></h1>
 	  <?php /* If this is a monthly archive */ } elseif (is_month()) { ?>
		<h1 class="pagetitle">mySociety blog &raquo; archive for <?php the_time('F, Y'); ?></h1>
 	  <?php /* If this is a yearly archive */ } elseif (is_year()) { ?>
		<h1 class="pagetitle">mySociety blog &raquo;  archive for <?php the_time('Y'); ?></h1>
	  <?php /* If this is an author archive */ } elseif (is_author()) { ?>
		<h1 class="pagetitle">mySociety blog &raquo; author Archive</h1>
 	  <?php /* If this is a paged archive */ } elseif (isset($_GET['paged']) && !empty($_GET['paged'])) { ?>
		<h1 class="pagetitle">mySociety blog &raquo; archives</h1>
 	  <?php } ?>
	<div class="contentwide">

<?php
if (is_category('Projects')) {
    $posts = query_posts($query_string . '&orderby=title&order=asc&posts_per_page=-1');
} elseif (is_category(29)) {
    $posts = query_posts($query_string . '&posts_per_page=-1');
    echo '<ul>';
} 

while (have_posts()) : the_post();

        // is idea submission?
         $is_idea = in_category(29);

        // get post meta and only display basics if this is an idea submission
	if ($is_idea) {
                $keys = get_post_custom_values('Author Name');
                $author_name = $keys[0];
                $keys = get_post_custom_values('Author Webpage');
                $author_web = $keys[0];                    
                if ($author_web == 'http://') {
                    $author_web = '';
                }
?>
		<div class="post dividerbottom">
			<li id="post-<?php the_ID(); ?>"><a href="<?php the_permalink() ?>" rel="bookmark" title="Permanent Link to <?php the_title_attribute(); ?>"><?php the_title(); ?></a>
                        <small>
                            <?php if($author_web == ''){ ?>
                                by <strong><?php echo $author_name; ?></strong>
                            <?php } else { ?>
                                by <strong><a rel="nofollow" href="<?php echo $author_web ?>"><?php echo $author_name; ?></a></strong>
                            <?php } ?>

			| <?php edit_post_link('Edit', '', ' | '); ?>  <?php comments_popup_link('No Comments &#187;', '1 Comment &#187;', '% Comments &#187;'); ?>
                        </small>

		</div>
<?php
	} else {
?>
		<div class="post dividerbottom">
			<h3 id="post-<?php the_ID(); ?>"><a href="<?php the_permalink() ?>" rel="bookmark" title="Permanent Link to <?php the_title_attribute(); ?>"><?php the_title(); ?></a></h3>
                    <small>
                        <?php the_time('l, F jS, Y') ?> by <strong><?php the_author() ?></strong>
                    </small>

			<div class="entry">
				<?php the_content() ?>
			</div>

			<p class="postmetadata"><?php the_tags('Tags: ', ', ', '<br />'); ?> Posted in <?php the_category(', ') ?> | <?php edit_post_link('Edit', '', ' | '); ?>  <?php comments_popup_link('No Comments &#187;', '1 Comment &#187;', '% Comments &#187;'); ?></p>

		</div>

<?php
	}

endwhile;

if (is_category(29)) {
    echo '</ul>';
}

?>

		<div class="navigation">
			<div class="alignleft"><?php next_posts_link('&laquo; Older Entries') ?></div>
			<div class="alignright"><?php previous_posts_link('Newer Entries &raquo;') ?></div>
		</div>

	<?php else : ?>

		<h2 class="center">Not Found</h2>
		<?php include (TEMPLATEPATH . '/searchform.php'); ?>

	<?php endif; ?>

	</div>
	

	<?php get_sidebar(); ?>
	
	<br class="clear"/>
<?php get_footer(); ?>
