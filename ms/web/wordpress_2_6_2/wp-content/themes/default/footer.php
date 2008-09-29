
		<div id="divFooter">
			<?
		    	print file_get_contents($_SERVER['DOCUMENT_ROOT'] .  "/footer.html"); 
			?>

			<p>
			mySociety is a project of <a href="http://www.ukcod.org.uk/">UK Citizens Online Democracy</a> (UKCOD). UKCOD is a registered charity in England and Wales, no. 1076346.
			</p>
		
				<!-- <?php echo get_num_queries(); ?> queries. <?php timer_stop(1); ?> seconds. -->
		</div>
	</div>
</div>

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
