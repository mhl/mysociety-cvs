        </div>
    </div>
    <div id="divFooter">
        <ul class="inline">
            <li><a href="{$www_server}">{l}Home{/l}</a>&nbsp;|</li>
            <li><a href="{$www_server}/api/"><acronym title="Application Programming Interface">API</acronym> &amp; feeds</a>&nbsp;|</li>                                
            <li><a href="http://groups.google.com/group/groupsnearyou">{l}Discussion list{/l}</a>&nbsp;|</li>
            <li><a href="{$www_server}/about/">{l}About{/l}</a>&nbsp;|</li>            
            <li><a href="http://blog.{$domain}">Blog</a>&nbsp;|</li>                             
            <li><a href="mailto:team@{$domain}">{l}Contact{/l}</a></li>                
        </ul>
    </div>
    {if $onloadscript !="" || $set_focus_control !="" && use_body_script == false}
		<script type="text/javascript" defer="defer">
			{if $set_focus_control !=""}setFocus('{$set_focus_control}');{/if}
			{if $onloadscript !=""}{$onloadscript} {/if}
		</script>
	{/if}
	
    {if $track}{$track}{/if}

    <!-- Piwik -->
    <script type="text/javascript">
    var pkBaseURL = (("https:" == document.location.protocol) ? "https://piwik.mysociety.org/" : "http://piwik.mysociety.org/");
    document.write(unescape("%3Cscript src='" + pkBaseURL + "piwik.js' type='text/javascript'%3E%3C/script%3E"));
    </script>
    <script type="text/javascript">
    <!--
    piwik_action_name = '';
    piwik_idsite = 6;
    piwik_url = pkBaseURL + "piwik.php";
    piwik_log(piwik_action_name, piwik_idsite, piwik_url);
    //-->
    </script>
    <noscript><img src="http://piwik.mysociety.org/piwik.php?i=1" style="border:0" alt=""></noscript>
    <!-- /Piwik -->

</body>
</html>
