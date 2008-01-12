{include file="../templates/header.tpl"}

    {if $show_sent == false}
        <h3>Edit <em>{$group->name}</em> (creator only)</h3>

        <form action="{$form_action}" method="post">
            {include file="../templates/formvars.tpl"}
            <p>
                {l}
                    To edit the page on <em><strong>{$group->name}</strong></em> enter the email address you used to create the group.
                {/l}
                &nbsp;
                <input type="text" class="text{if $warn_txtEmail} error{/if}" id="txtEmail" name="txtEmail" value="{$data.txtEmail}" />
            </p>
            <div class="buttons">
                <input type="submit" value="Next >" />
            </div>
        </form>
        
    {else}

        <div class="attention">
            <h3>{l}Thanks! Your comments have been sent to the {$site_name} team{/l}</h3>
            <p>
                <a href="{$www_server}/groups/{$group->url_id}">{l}Back to <em>{$group->name}</em>{/l}</a>
                <br/>
               <a href="{$www_server}">{l}Do a new search{/l}</a> 
            </p>
        </div>
    {/if}

{include file="../templates/footer.tpl"}