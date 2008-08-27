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

<!-- Piwik -->
<script type="text/javascript">
var pkBaseURL = (("https:" == document.location.protocol) ? "https://piwik.mysociety.org/" : "http://piwik.mysociety.org/");
document.write(unescape("%3Cscript src='" + pkBaseURL + "piwik.js' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
<!--
piwik_action_name = '';
piwik_idsite = 5;
piwik_url = pkBaseURL + "piwik.php";
piwik_log(piwik_action_name, piwik_idsite, piwik_url);
//-->
</script>
<noscript><img src="http://piwik.mysociety.org/piwik.php?i=1" style="border:0" alt=""></noscript>
<!-- /Piwik -->

</body>
</html>
