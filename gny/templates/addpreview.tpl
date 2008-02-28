{include file="../templates/header.tpl"}
<div class="contentfull">
    <form id="frmAddContact" action="{$form_action}" method="post">
        {include file="../templates/formvars.tpl"}
        <fieldset>
            <input type="hidden" id="hidSaveMapData" value="0" />
            <input type="hidden" id="hidMiniMap" value="{$mini_map}" />        
        </fieldset>
    
        {if $group->mode == "admin" || $group->mode == "edit"}
            <h3>{l}Preview your changes and click save to update this group{/l}</h3>
        {else}
            <h3>{l}Nearly done, review this group then click confirm{/l}</h3>    
        {/if}
        
        {include file="../templates/groupdetail.tpl"}
    
        <p id="pEditGroup">
            <span class="highlight">{l}Something wrong? Edit the <a href="{$www_server}/add/about/">group details{/l}</a>,
    	the <a href="{$www_server}/add/location/">area covered</a>, or
    	<a href="{$www_server}/add/contact/">how to join</a></span>
        </p>

        <div class="buttons">
            {if $group->mode == "admin"}
                <input type="submit" class="button" value="{l}Save changes{/l} &raquo;"/>        
            {elseif $group->mode == "edit"}
                <input type="submit" class="button" value="{l}Save changes{/l} &raquo;"/>                    
            {else}
                <input type="submit" class="button" value="{l}Confirm this group{/l} &raquo;"/>
            {/if}
        </div>
    </form>
</div>
{include file="../templates/footer.tpl"}
