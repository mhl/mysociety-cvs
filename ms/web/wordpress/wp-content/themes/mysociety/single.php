<?php 
// Spot we are just showing a proposals2006 post, and set menu etc.
global $menu_proposals2006;
foreach ($posts as $catcheck) 
{ 
    $catcheck_cats = wp_get_post_cats('', $catcheck->ID);
    if( is_array( $catcheck_cats ) ) {
        foreach ( $catcheck_cats as $cat_id ) {
            if ($cat_id == 3) { 
                $cat = 3; 
                $menu_proposals2006 = true;
            } 
        }
    }
}
get_header(); 

if ($cat == 3) {
    ?>
<div class="item_head">What is this all about?</div>
<div class="item">
<p>The idea described below was a submission to the mySociety Call for Proposals 2006. It is a 
suggestion for a website which meets our <a href="/proposals2006/submit">criteria</a>, to have a tangible benefit to the civic and community aspects of people's lives.
The winning
proposal <a href="http://www.mysociety.org/2006/09/27/the-mysociety-call-for-proposals-the-winner-and-runners-up/">was announced on 27th September 2006</a>; that is the one we are going to implement. You can still read, discuss and add comments to the idea below, or <a href="/proposals2006/view">browse all the proposals</a>. Maybe you and/or someone else can get together to implement one.
Read more <a href="/faq.php">about mySociety</a>.
</p></div>
<div class="item_foot"></div>

    <?
}

?>

	<div id="content" class="widecolumn">
				
  <?php if (have_posts()) : while (have_posts()) : the_post(); ?>
	
<!--		<div class="navigation">
			<div class="alignleft"><?php previous_post('&laquo; %','','yes') ?></div>
			<div class="alignright"><?php next_post(' % &raquo;','','yes') ?></div>
		</div> -->
	
		<div class="post">
			<div class="item_head" id="post-<?php the_ID(); ?>"><a
            href="<?php echo get_permalink() ?>" rel="bookmark"
            title="Permanent Link: <?php the_title(); ?>"><?php
                the_title(); ?> &mdash; 
                <?php the_time('jS F Y')?></a></div>

				<div class="meta"><?=($cat == 3) ? "Proposed by" : "Posted by"?> <?php the_author() ?>  </div> 
	
			<div class="item">
				<?php the_content('<p class="serif">Read the rest of this entry &raquo;</p>'); ?>
	
				<?php link_pages('<p><strong>Pages:</strong> ', '</p>', 'number'); ?>
	
            </div>
				<div class="item_foot">
					<small>
<!--						This entry was posted
						<?php /* This is commented, because it requires a little adjusting sometimes.
							You'll need to download this plugin, and follow the instructions:
							http://binarybonsai.com/archives/2004/08/17/time-since-plugin/ */
							/* $entry_datetime = abs(strtotime($post->post_date) - (60*120)); echo time_since($entry_datetime); echo ' ago'; */ ?> 
						on <?php the_time('l, F jS, Y') ?> 
						and is filed under <?php the_category(', ') ?>.
						You can follow any responses to this entry through the <?php comments_rss_link('RSS 2.0'); ?> feed. 
                        -->
						
						<?php if (('open' == $post-> comment_status) && ('open' == $post->ping_status)) {
							// Both Comments and Pings are open ?>
							You can <a href="#respond">leave a response</a>, or <a href="<?php trackback_url(display); ?>">trackback</a> from your own site.
						
						<?php } elseif (!('open' == $post-> comment_status) && ('open' == $post->ping_status)) {
							// Only Pings are Open ?>
							Responses are currently closed, but you can <a href="<?php trackback_url(display); ?> ">trackback</a> from your own site.
						
						<?php } elseif (('open' == $post-> comment_status) && !('open' == $post->ping_status)) {
							// Comments are open, Pings are not ?>
							<!-- You can skip to the end and leave a response. Pinging is currently not allowed.-->
			
						<?php } elseif (!('open' == $post-> comment_status) && !('open' == $post->ping_status)) {
							// Neither Comments, nor Pings are open ?>
							Both comments and pings are currently closed.			
						
						<?php } edit_post_link('Edit this entry.','',''); ?>
						
					</small>
	
			</div>
		</div>
		
	<?php comments_template(); ?>
	
	<?php endwhile; else: ?>
	
		<p><?php _e('Sorry, no posts matched your criteria.'); ?></p>
	
<?php endif; ?>
	
	</div>

<?php get_footer(); ?>
