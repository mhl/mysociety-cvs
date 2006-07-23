	<div id="sidebar">
            <?php include (TEMPLATEPATH . '/searchform.php'); ?>

			
			<?php /* If this is a category archive */ if (is_category() && $cat!=1) { ?>
	<!--		<p>You are currently browsing the archives for the <?php single_cat_title(''); ?> category.</p>-->
			
			<?php /* If this is a daily archive */ } elseif (is_day()) { ?>
			<p>You are currently browsing the <a href="<?php echo get_settings('siteurl'); ?>"><?php echo bloginfo('name'); ?></a> weblog archives
			for the day <?php the_time('l, F jS, Y'); ?>.</p>
			
			<?php /* If this is a monthly archive */ } elseif (is_month()) { ?>
			<p>You are currently browsing the <a href="<?php echo get_settings('siteurl'); ?>"><?php echo bloginfo('name'); ?></a> weblog archives
			for <?php the_time('F, Y'); ?>.</p>

      <?php /* If this is a yearly archive */ } elseif (is_year()) { ?>
			<p>You are currently browsing the <a href="<?php echo get_settings('siteurl'); ?>"><?php echo bloginfo('name'); ?></a> weblog archives
			for the year <?php the_time('Y'); ?>.</p>
			
		 <?php /* If this is a search archive */ } elseif (is_search()) { ?>
            <div class="item_head"></div>
			<div class="item">You have searched the <a href="<?php echo get_settings('siteurl'); ?>"><?php echo bloginfo('name'); ?></a> weblog archives
			for <strong>'<?php echo wp_specialchars($s); ?>'</strong>. If you are unable to find anything in these search results, you can try one of these links.</div>
            <div class="item_foot"></div>

			<?php /* If this is a paged archive */ } elseif (isset($_GET['paged']) && !empty($_GET['paged'])) { ?>
			<p>You are currently browsing the <a href="<?php echo get_settings('siteurl'); ?>"><?php echo bloginfo('name'); ?></a> weblog archives.</p>

			<?php } ?>

			<?php wp_list_pages('title_li=<h2>' . __('Pages') . '</h2>' ); ?>

			<?php if (is_category() && $cat==1) { ?>
				<div class="item_head">Developer's Blog</div>
				<div class="item"><ul>
				<?php wp_get_archives('type=postbypost&limit=10&cat=2'); ?>
				</ul></div>
				<div class="item_foot"></div>
			<?php } ?>

			<div class="item_head"><?php 
                    if (is_category())
                        print single_cat_title('') . ' ';
                    _e('Archives'); 
            ?></div>
            <div class="item">
				<ul class="archive_list">
				<?php ($cat == 3) ? wp_get_archives("cat=$cat&type=postbypost") : wp_get_archives("cat=$cat"); ?>
				</ul>
            </div>
            <div class="item_foot">
            </div>

			<?php if ($cat!=3) { ?>
                <div class="item_head">Categories</div>
                <div class="item">
<ul><?php wp_list_cats('feed=XML&use_desc_for_title=0&feed_image=/rss.gif');?></ul>
</div>
<div class="item_foot">
</div>
            <?php } else { ?>
                <div class="item_head">RSS Feed</div>
                <div class="item">

	<a href="<?php bloginfo('rss2_url'); ?>&cat=<?=$cat?>">New proposals <img border="0" src="/rss.gif" alt="RSS"valign="bottom"></a> 
</div>
<div class="item_foot">
</div>
            <?php } ?>


<!--			<h2><?php _e('Categories'); ?></h2>
				<ul>
				<?php list_cats(0, '', 'name', 'asc', '', 1, 0, 1, 1, FALSE, 1, 0,'','','','','') ?>
				</ul>-->

<!--
			<?php /* If this is the frontpage */ if ( is_home() || is_page() ) { ?>				
				<?php get_links_list(); ?>
				
				<li><h2><?php _e('Meta'); ?></h2>
				<ul>
					<?php wp_register(); ?>
					<li><?php wp_loginout(); ?></li>
					<li><a href="http://validator.w3.org/check/referer" title="<?php _e('This page validates as XHTML 1.0 Transitional'); ?>"><?php _e('Valid <abbr title="eXtensible HyperText Markup Language">XHTML</abbr>'); ?></a></li>
					<li><a href="http://gmpg.org/xfn/"><abbr title="XHTML Friends Network">XFN</abbr></a></li>
					<li><a href="http://wordpress.org/" title="<?php _e('Powered by WordPress, state-of-the-art semantic personal publishing platform.'); ?>">WordPress</a></li>
					<?php wp_meta(); ?>
				</ul>
				</li>
			<?php } ?>
		</ul>
-->			
	</div>

