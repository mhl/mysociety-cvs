{include file="../templates/admin/header.tpl"}

    <form id="frmGroups" action="searchgroups.php" method="post">
        {include file="../templates/formvars.tpl"}
        
        <div id="divSearch">
            <label for="txtSearch">Search groups by name</label>
            <input type="text" name="txtSearch" id="txtSearch" value="{$search}"/>
            <input type="submit" value="Go"/>
        </div>

        <div>
            {if $groups|@sizeof >0}
                <table>
                {foreach name="groups" from="$groups" item="group"}
                    <tr {if $group->confirmed == false}class="disabled"{/if}>
                        <td>
                            {$group->name}&nbsp;<a target="_new" href="{$url}/groups/{$group->url_id}?admin=1">[view group]</a>
                        </td>
                        <td class="buttoncell">
                            <input type="button" class="edit" value="Edit" onclick="javascript:editGroup({$group->group_id});"/>
                        </td>
                        {if $group->confirmed == true}
                        <td class="buttoncell">
                            <input type="button" class="disable" value="Disable" onclick="javascript:disableGroup('{$group->name|escape:url}', {$group->group_id});"/>
                        </td>
                        {else}
                            <td class="buttoncell">
                                <input type="button" class="enable" value="Enable" onclick="javascript:enableGroup('{$group->name|escape:url}', {$group->group_id});"/>
                            </td>
                        {/if}
                        <td class="buttoncell">
                            <input type="button" class="delete" value="Delete" onclick="javascript:deleteGroup('{$group->name|escape:url}', {$group->group_id});"/>
                        </td>
                    </tr>
                {/foreach}
            </table>
            {/if}
        </div>
    </form>
{include file="../templates/admin/footer.tpl"}
