        </div>
    </div>
    <div id="divFooter">
        <ul class="inline">
            <li><a href="{$www_server}">{l}Home{/l}</a>&nbsp;|</li>
            <li><a href="{$www_server}/api/"><acronym title="Application Programming Interface">API</acronym> &amp; feeds</a>&nbsp;|</li>                                
            <li><a href="http://groups.google.com/group/groupsnearyou">{l}Discussion list{/l}</a>&nbsp;|</li>
            <li><a href="{$www_server}/about/">{l}About{/l}</a>&nbsp;|</li>                         
            <li><a href="mailto:team@{$domain}">{l}Contact{/l}</a></li>                
            <li><a href="blog.{$domain}">{l}Blog{/l}</a></li>
        </ul>
    </div>
    {if $onloadscript !="" || $set_focus_control !="" && use_body_script == false}
		<script type="text/javascript" defer="defer">
			{if $set_focus_control !=""}setFocus('{$set_focus_control}');{/if}
			{if $onloadscript !=""}{$onloadscript} {/if}
		</script>
	{/if}
	
    {if $track}{$track}{/if}
    <script src="http://www.google-analytics.com/urchin.js" type="text/javascript">
    </script>
    <script type="text/javascript">
        _uacct = "UA-321882-11";
        if (typeof urchinTracker == 'function') urchinTracker();
    </script>
</body>
</html>
