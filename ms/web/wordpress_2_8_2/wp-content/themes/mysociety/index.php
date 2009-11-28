<?php

get_header();

if (have_posts()) : ?>

	<h1 class="pagetitle hide">mySociety blog</h1>
	<div class="contentwide">

<?php
    if (is_category('Projects')) {
        $posts = query_posts($query_string . '&orderby=title&order=asc&posts_per_page=-1');
    }

    while (have_posts()) : the_post();
    
    $is_cee_cfp = ($_SERVER['SERVER_NAME'] == 'cee.mysociety.org' && substr($_SERVER['REQUEST_URI'], 0, 5) == '/cfp/');
    if ($is_cee_cfp) {
        $keys = get_post_custom_values('Author Name');
        $author_name = $keys[0];
        $keys = get_post_custom_values('Author Webpage');
        $author_web = $keys[0];                    
        if($author_web == 'http://'){
            $author_web = '';
        }
    }
?>
		<div class="post dividerbottom">
				<h3 id="post-<?php the_ID(); ?>"><a href="<?php the_permalink() ?>" rel="bookmark" title="Permanent Link to <?php the_title_attribute(); ?>"><?php the_title(); ?></a></h3>

		    <?php if ($is_cee_cfp) { ?>
                    <small>
                        <?php the_time('l, F jS, Y') ?>
                        <?php if($author_web == ''){ ?>
                            by <strong><?php echo $author_name; ?></strong>
                        <?php } else { ?>
                            by <strong><a href="<?php echo $author_web ?>"><?php echo $author_name; ?></a></strong>
                        <?php } ?>
                    </small>
            <?php } else { ?>
                <small>
                    <?php the_time('l, F jS, Y') ?> by <strong><?php the_author() ?></strong>
                </small>
            <?php } ?>


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

