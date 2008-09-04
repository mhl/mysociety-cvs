

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


		
			<!-- Categories -->
			<h4>Categories</h4>
			<ul class="nobullets">
				<?php wp_list_categories('show_count=1&title_li=&show_count=0&feed=RSS'); ?>
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


		<?php /* If this is the frontpage */ if ( is_home() || is_page() ) { ?>
			<?php wp_list_bookmarks(); ?>

			<li><h2>Meta</h2>
			<ul>
				<?php wp_register(); ?>
				<li><?php wp_loginout(); ?></li>
				<li><a href="http://validator.w3.org/check/referer" title="This page validates as XHTML 1.0 Transitional">Valid <abbr title="eXtensible HyperText Markup Language">XHTML</abbr></a></li>
				<li><a href="http://gmpg.org/xfn/"><abbr title="XHTML Friends Network">XFN</abbr></a></li>
				<li><a href="http://wordpress.org/" title="Powered by WordPress, state-of-the-art semantic personal publishing platform.">WordPress</a></li>
				<?php wp_meta(); ?>
			</ul>
			</li>
		<?php } ?>

		<?php endif; ?>
	</ul>
	</div>
</div>

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
