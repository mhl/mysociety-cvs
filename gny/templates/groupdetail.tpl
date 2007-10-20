<fieldset>
    <input type="hidden" id="hidSaveMapData" value="0" />
    <input type="hidden" id="hidMiniMap" value="{$mini_map}" />        
</fieldset>
<div id="divGroup" {if $preview == true}class="preview"{/if}>
    <div id="divGroupHeader">
        <h3>{$group->name}</h3>
        <h4>{$group->byline}</h4>
        {if $preview != true}
            <div id="divInvolved">
                {if $group->involved_type == 'email'}
                    {if !$dead_links}
                        <a href="{$www_server}/groups/{$group->url_id}/contact/">Join this group</a>
                    {else}
                        <a href="#" title="link disabled for preview">Join this group</a>
                    {/if}
                {else}
                    {if !$dead_links}
                        <a href="{$group->involved_link}">Join this group</a>
                    {else}
                        <a href="#" title="link disabled for preview">Join this group</a>
                    {/if}
                {/if}
            </div>
        {/if}
    </div>

    <div id="divDescription">
        {$group->description}
        <div id="divMapMiniWrapper">
            <div id="divMap"></div>
        </div>
    </div>

    <div id="divMeta">
        It has been tagged with the keywords <strong>{$group->tags}</strong>.
        This page was created by <strong>{$group->created_name} on {$group->created_date|date_format}</strong>. 
        {if !$dead_links}
            <a href="{$www_server}/groups/{$group->url_id|escape:url}/report/">Suggest a change to this group</a>
        {/if}
    </div>
</div>