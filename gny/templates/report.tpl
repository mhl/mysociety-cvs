{include file="../templates/header.tpl"}

    {if $show_sent == false}
        <h3>Contact {$site_name} about <em>{$group->name}</em></h3>
        <p>
            {l}
                If you would like to suggest a change to the page for <em><strong>{$group->name}</strong></em>, 
                or want to report something inappropriate, please use the form below to contact the {$site_name} team.
            {/l}
        </p>
        <form id="frmReportAbuse" action="{$form_action}" method="post">
            {include file="../templates/formvars.tpl"}
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
                    <textarea id="txtContactMessage" name="txtContactMessage" {if $warn_txtContactMessage}class="error"{/if}></textarea>
                </li>
            </ul>
            <small class="required"><span>*</span> = {l}required information{/l}</small>
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