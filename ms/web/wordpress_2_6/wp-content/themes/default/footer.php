<div id="footer">
<?
    print file_get_contents($_SERVER['DOCUMENT_ROOT'] .  "/footer.html"); 
?>

<!-- If you'd like to support WordPress, having the "powered by" link somewhere on your blog is the best way; it's our only promotion or advertising. -->
	<p>
		mySociety is a project of <a href="http://www.ukcod.org.uk/">UKCOD</a> | powered by
		<a href="http://wordpress.org/">WordPress</a>		
		|
		<a href="<?php bloginfo('rss2_url'); ?>">Entries (RSS)</a>
		 | 
		 <a href="<?php bloginfo('comments_rss2_url'); ?>">Comments (RSS)</a>
	</p>
		
		<!-- <?php echo get_num_queries(); ?> queries. <?php timer_stop(1); ?> seconds. -->
	</p>
</div>
</div>

<?php /* "Just what do you think you're doing Dave?" */ ?>
    <?php wp_footer(); ?>
</body>
</html>
