<div id="divGroup" {if $preview == true}class="preview"{/if}>
    <div id="divGroupHeader">
        <h3>{$group->name}</h3>
        <h4>{$group->byline}</h4>
        {if $preview != true}
            <div id="divInvolved">
                {if $group->involved_type == 'email'}
                    <a href="{$www_server}/groups/{$group->url_id}/contact/">Contact this group</a>
                {else}
                    <a href="{$group->involved_link}">Visit group's website</a>
                {/if}
            </div>
        {/if}
    </div>

    <div id="divDescription">
        {$group->description}
    </div>

    <div id="divMeta">
        You can <a href="javascript:popup_map('{$www_server}/map.php?url_id={$group->url_id|escape:url}');" title="View on a map (new window)">view the area covered by this group on a map</a>.
        It has been tagged with <strong>{$group->tags}</strong>.
        This page was created by <strong>{$group->created_name} on {$group->created_date|date_format}</strong>. <a href="{$www_server}/groups/{$group->url_id|escape:url}/report/">Report abuse?</a>
    </div>
</div>