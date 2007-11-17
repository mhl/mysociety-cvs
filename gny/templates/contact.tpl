{include file="../templates/header.tpl"}
    <form action="{$form_action}" method="post">
        {include file="../templates/formvars.tpl"}
        <h3>Contact {$group->name}</h3>
        <ul class="form nobullets">
            <li>
                <label for="txtName">
                    {l}Your name{/l} *
                </label>
                <input type="text" class="text{if $warn_txtName} error{/if}" id="txtName" name="txtName" value="{$data.txtName}" />
            </li>
            <li>
                <label for="txtEmail">
                    {l}Your email address{/l} *
                </label>
                <input type="text" class="text{if $warn_txtEmail} error{/if}" id="txtEmail" name="txtEmail" value="{$data.txtEmail}" />
            </li>
            <li>
                <label for="txtMessage">{l}Your message{/l} *</label>
<textarea id="txtContactMessage" name="txtContactMessage" {if $warn_txtContactMessage}class="error"{/if}>{if $data.txtContactMessage == ''}
{l}Hi,

I found out about {$group->name} on {$site_name} and would like to know how I can get involved.

All the best{/l}
    {else}{$data.txtContactMessage}{/if}</textarea>
            </li>
        </ul>
        <small class="required"><span>*</span> = {l}required information{/l}</small>
        <div class="buttons">
            <input type="submit" value="{l}Next{/l} &raquo;" />
        </div>
    </form>
{include file="../templates/footer.tpl"}    
