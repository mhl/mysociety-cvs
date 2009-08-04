<?php
/*
Template Name: Call for proposals 09
*/
?>

<?php get_header(); ?>

	<h1 class="hide"><?php the_title(); ?></h1>
	<div class="contentwide">
	    <img src="/contimg/call-for-proposals.jpg" height="434" width="500" />
	</div>
    <div class="contentnarrow right">
        <div class="proposalsintro">
            <p>
                We need <strong>your help</strong> to decide what mySociety builds next.
            </p>
            <p>
                Our previous calls for proposals have led to WhatDoTheyKnow.com, WriteToThem.com and Pledgebank.com.
            </p>
            <p>
                What <strong>big new services</strong> should we build? What <strong>features</strong> should we add to our existing sites? What bright ideas do you have to <strong>promote mySociety</strong> to the world?
            </p>
        </div>
    </div>

    <br class="clear"/>
    <div class="contentwide">
        <div>
    	    <h2>Tell us what you think we should do next</h2>
    		<?php if (have_posts()) : while (have_posts()) : the_post(); ?>
    				<?php the_content('<p class="serif">Read the rest of this page &raquo;</p>'); ?>

    				<?php wp_link_pages(array('before' => '<p><strong>Pages:</strong> ', 'after' => '</p>', 'next_or_number' => 'number')); ?>

    		<?php endwhile; endif; ?>
	
    		<?php edit_post_link('Edit this entry.', '<p class="editlink">', '</p>'); ?>
        </div>
    </div>
    <div class="contentnarrow right">
        <div class="sidebar">
            <h3>Ideas so far</h3>
            <!--Recent posts-->
            <?php if (!is_home()) { ?>
                <ul>
                    <?php $myposts = get_posts('numberposts=12&category=29');
                        foreach($myposts as $post) {?>
                            <li>
                                <a href="<?php the_permalink(); ?>"><?php the_title();?></a>
                            </li>
                    <?php } ?>
                </ul>
            <?php } ?>
        </div>
    </div>    
    
<?php include (TEMPLATEPATH . '/catposts.php'); ?>
<?php get_footer(); ?>