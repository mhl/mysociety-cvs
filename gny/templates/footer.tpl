        </div>
        <div id="divFooter">
            <ul class="inline">
                <li><a href="{$www_server}">Home</a></li>
                <li><a href="{$www_server}/api/"><acronym title="Application Programming Interface">API</acronym> &amp; feeds</a></li>                                
                <li><a href="http://groups.google.com/group/groupsnearyou">Discussion list</a></li>
                <li><a href="{$www_server}/about/">About</a></li>                         
                <li><a href="{$www_server}/about/#contact">Contact</a></li>                
            </ul>

        </div>
    </div>
    {if $onloadscript !="" || $set_focus_control !=""}
		<script type="text/javascript" defer="defer">
			{if $set_focus_control !=""}setFocus('{$set_focus_control}');{/if}
			{if $onloadscript !=""}{$onloadscript} {/if}
		</script>
	{/if}
	
	<script src="http://www.google-analytics.com/urchin.js" type="text/javascript">
    </script>
    <script type="text/javascript">
        _uacct = "UA-321882-8";
        urchinTracker();
    </script>
</body>
</html>
