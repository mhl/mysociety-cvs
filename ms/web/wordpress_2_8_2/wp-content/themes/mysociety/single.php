<?php get_header(); ?>
	<?php if (have_posts()) : while (have_posts()) : the_post(); ?>
	    
	    <?php
            // is idea submission?
            $is_idea = in_category(29);
            $is_cee_cfp = ($_SERVER['SERVER_NAME'] == 'cee.mysociety.org' && substr($_SERVER['REQUEST_URI'], 0, 5) == '/cfp/');

            //get post meta if this is an idea submission
            if ($is_idea || $is_cee_cfp) {
                $keys = get_post_custom_values('Author Name');
                $author_name = $keys[0];
                $keys = get_post_custom_values('Author Webpage');
                $author_web = $keys[0];                    
                if($author_web == 'http://'){
                   $author_web = '';
                }
            }
        ?>

		<!--Title-->
		<?php if (!$is_idea){ ?>
		    <h1><?php the_title(); ?></h1>
		<?php }else{ ?>
		    <h1>Call For Proposals 2009 &raquo; <?php the_title(); ?></h1>		
		<?php } ?>
		
		<!--Post-->
		<div class="contentwide">
		    
		    <?php if ($is_idea || $is_cee_cfp) { ?>
                
                    <small>
                        <?php if($author_web == ''){ ?>
                            By <strong><?php echo $author_name; ?></strong>
                        <?php } else { ?>
                            By <strong><a href="<?php echo $author_web ?>"><?php echo $author_name; ?></a></strong>
                        <?php } ?>
                    </small>
            <?php } else { ?>
                <small>
                    <?php the_time('l, F jS, Y') ?> by <strong><?php the_author() ?></strong>
                </small>
            <?php } ?>

			<div class="entry" id="post-<?php the_ID(); ?>">
				<?php the_content('<p class="serif">Read the rest of this entry &raquo;</p>'); ?>

				<?php wp_link_pages(array('before' => '<p><strong>Pages:</strong> ', 'after' => '</p>', 'next_or_number' => 'number')); ?>
				<?php the_tags( '<p>Tags: ', ', ', '</p>'); ?>

				<p class="postmetadata alt">
					<small>
						This entry was posted
						<?php /* This is commented, because it requires a little adjusting sometimes.
							You'll need to download this plugin, and follow the instructions:
							http://binarybonsai.com/archives/2004/08/17/time-since-plugin/ */
							/* $entry_datetime = abs(strtotime($post->post_date) - (60*120)); echo time_since($entry_datetime); echo ' ago'; */ ?>
						on <?php the_time('l, F jS, Y') ?> at <?php the_time() ?>
						and is filed under <?php the_category(', ') ?>.
						<?php post_comments_feed_link('Follow responses to this entry'); ?> (RSS2 feed).

						<?php if (('open' == $post-> comment_status) && ('open' == $post->ping_status)) {
							// Both Comments and Pings are open ?>
							You can <a href="#respond">leave a response</a>, or <a href="<?php trackback_url(); ?>" rel="trackback">trackback</a> from your own site.

						<?php } elseif (!('open' == $post-> comment_status) && ('open' == $post->ping_status)) {
							// Only Pings are Open ?>
							Responses are currently closed, but you can <a href="<?php trackback_url(); ?> " rel="trackback">trackback</a> from your own site.

						<?php } elseif (('open' == $post-> comment_status) && !('open' == $post->ping_status)) {
							// Comments are open, Pings are not
							// You can skip to the end and leave a response. Pinging is currently not allowed.

						} elseif (!('open' == $post-> comment_status) && !('open' == $post->ping_status)) {
							// Neither Comments, nor Pings are open ?>
							Both comments and pings are currently closed.

						<?php } edit_post_link('Edit this entry','','.'); ?>

					</small>
				</p>
			</div>

			<!-- Comments -->		
			<?php comments_template(); ?>


	<?php endwhile; else: ?>

		<p>Sorry, no posts matched your criteria.</p>

<?php endif; ?>

</div>
		
<!-- Sidebar -->
<?php
if (!$is_idea && !$is_cee_cfp) {
    get_sidebar();
} else {
    if ($is_idea) {
        $add_link = '/call-for-proposals-2009/';
        $view_link = '/category/proposal-submissions-2009/';
    } elseif ($is_cee_cfp) {
        $add_link = '/';
        $view_link = '/cfp/view/';
    }

?>
    <div class="contentnarrow right">
        <p>
        <a class="linkbutton" href="<?=$add_link?>">
                <span class="left">&nbsp;</span>
                <span class="middle">Add an idea ...</span>
                <span class="right">&nbsp;</span>
            </a>
            <br class="clear"/>
        </p>
        <h3>Ideas so far</h3>
        <!--Recent posts-->
            <ul>
<?php

if ($is_idea) {
    query_posts('category_name=proposal-submissions-2009&showposts=10');
} elseif ($is_cee_cfp) {
    query_posts('showposts=10');
}

while (have_posts()) : the_post(); ?>
                <li>
                    <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
                </li>
<?php endwhile;?>
            </ul>
            <a href="<?=$view_link?>">View all ideas &raquo;</a>
    </div>
<?php } ?>

<?php get_footer(); ?>
