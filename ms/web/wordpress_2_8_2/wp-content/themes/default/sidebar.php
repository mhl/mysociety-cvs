

	<!-- Main sidebar -->
	<div class="contentnarrow right">


		<div class="sidebar">



		<?php 	/* Widgetized sidebar, if you have the plugin installed. */
				if ( !function_exists('dynamic_sidebar') || !dynamic_sidebar() ) : ?>

			<!-- Author information is disabled per default. Uncomment and fill in your details if you want to use it.
			<li><h2>Author</h2>
			<p>A little something about you, the author. Nothing lengthy, just an overview.</p>
			</li>
			-->

<?php
if (is_category()) {
	$cat = intval( get_query_var('cat') );
	echo '<p id="sidebar_rss"><a href="', get_category_feed_link($cat), '"><img align="top" src="/feed.png" alt=""> RSS feed for this category</a></p>';
} else {
	echo '<p id="sidebar_rss"><a href="', bloginfo('rss2_url'), '"><img align="top" src="/feed.png" alt=""> RSS feed</a></p>';
}
?>

<!-- News list -->
<div class="infoboxpurple contentnarrow right dividerright">
	<form method=post action="https://secure.mysociety.org/admin/lists/mailman/subscribe/news">
		<h4>News alerts</h4>
		<p>
			<label for="txtEmail">Enter your email address below and we'll send you occasional emails about what we've been up to.</label>
		</p>
		<ul class="nobullets">
			<li>
				<input type="text" class="textbox" id="txtEmail" name="email" value="" />
			</li>
			<li>
				<input type="Submit" name="email-button" value="Add me to the list" />
			</li>
		</ul>
	</form>
</div>

<!-- News list -->
<div id="divElsewhere" class="infoboxblue contentnarrow right dividerright">
		<h4>Other ways to stay up to date</h4>
		<p>
			<ul class="nobullets">
				<li>
					<a href="https://secure.mysociety.org/admin/lists/mailman/listinfo">Join a mailing list</a>
				</li>
				<li>
					<a href="http://www.facebook.com/pages/mySociety/7262005939">Facebook page</a>
				</li>
				<li>
					<a href="http://twitter.com/mysociety">Follow us on Twitter</a>
				</li>
			</ul>
		</p>
</div>
			<!-- Categories -->
    
<br/>
			<h4>Categories</h4>
			<ul class="nobullets">
				<?php wp_list_categories('title_li=&show_count=0'); ?>
			</ul>
		
			<?php if ( is_404() || is_category() || is_day() || is_month() ||
						is_year() || is_search() || is_paged() ) {
			?>

			<!-- Archives -->
			<h4>Browse archives</h4>
			<ul class="nobullets">
				<?php wp_get_archives('type=yearly'); ?>
			</ul>
		

		<?php }?>

		<?php endif; ?>
	</ul>

	</div>
</div>



<!-- Navigation -->
<div class="sidebar contentnarrow right">
	<h4>Navigation</h4>
	<p>
		<div class="alignleft"><?php previous_post_link('&laquo; %link') ?></div>
		<div class="alignright"><?php next_post_link('%link &raquo;') ?></div>
	</p>
</div>
