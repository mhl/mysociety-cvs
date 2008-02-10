{include file="../templates/header.tpl"}
<div class="contentfull">
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
            <h3>{l}Now check your email!{/l}</h3>
            <p>
                {l}We have sent you an email, <span class="highlight">click on the link in the email</span> to edit this group.
                If you don't receive an email in a few minutes, try checking your spam filter{/l}
            </p>
        </div>
    {/if}
</div>
{include file="../templates/footer.tpl"}