{include file="../templates/header.tpl"}

    <h3>All groups</h3>
    {assign var="previous_letter" value=""}
    <dl class="azindex">
        {foreach from=$groups item=group}
    		{assign var="current_letter" value=$group->name|substr:0:1|upper}
    		
    		{if $current_letter != $previous_letter}
    		        </ul>
		        </dd>
	        
            	<dt id="{$group->name}">
            	    {$current_letter}
            	</dt>
        		<dd>
        		    <ul class="nobullets collapse">
    		{/if}
    		        
    		            <li>
    		                <a href="{$www_server}/groups/{$group->url_id}" title="{$group->byline}">{$group->name}</a>
    		            </li>
    		        
    		{assign var="previous_letter" value=$group->name|substr:0:1|upper}
        {/foreach}
    </dl>

{include file="../templates/footer.tpl"}