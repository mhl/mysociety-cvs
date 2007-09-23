{include file="../templates/header.tpl"}
    <form action="{$form_action}" method="post">
        {include file="../templates/formvars.tpl"}
        <h3>Contact {$group->name}</h3>
        <ul class="form nobullets">
            <li>
                <label for="txtName">
                    Your name
                </label>
                <input type="text" class="text{if $warn_txtName} error{/if}" id="txtName" name="txtName" value="{$data.txtName}" />
            </li>
            <li>
                <label for="txtEmail">
                    Your email address
                </label>
                <input type="text" class="text{if $warn_txtEmail} error{/if}" id="txtEmail" name="txtEmail" value="{$data.txtEmail}" />
            </li>
            <li>
                <label for="txtMessage">Your message</label>
<textarea id="txtContactMessage" name="txtContactMessage" {if $warn_txtContactMessage}class="error"{/if}>{if $data.txtContactMessage == ''}
Hi,

I found out about {$group->name} on {$site_name} and would like to know how I can get involved.

All the best
    {else}{$data.txtContactMessage}{/if}</textarea>
            </li>
        </ul>
        <div class="buttons">
            <input type="submit" value="Next >" />
        </div>
    </form>
{include file="../templates/footer.tpl"}    
