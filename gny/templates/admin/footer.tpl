        </div>
    </div>
    {if $onloadscript !="" || $set_focus_control !=""}
		<script type="text/javascript" defer="defer">
			{if $set_focus_control !=""}setFocus('{$set_focus_control}');{/if}
			{if $onloadscript !=""}{$onloadscript} {/if}
		</script>
	{/if}

</body>
</html>
