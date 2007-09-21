{include file="../templates/header.tpl"}

{if $refering_url != '' && $show_return == true}
    <div id="divReturnToSearch">
        <a href="{$refering_url}">&lt; back to search results</a>
    </div>
{/if}

{include file="../templates/groupdetail.tpl"}

{include file="../templates/hcard.tpl"}

{include file="../templates/footer.tpl"}