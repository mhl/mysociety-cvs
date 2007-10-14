{include file="../templates/header.tpl"}

    {if $show_sent == false}
        <h3>Report abuse</h3>
        <p>
            If you think that there is something wrong with the information on the page for <em><strong>{$group->name}</strong></em>,
            please use the form below to contact the {$site_name} team.
        </p>
        <form id="frmReportAbuse" action="{$form_action}" method="post">
            {include file="../templates/formvars.tpl"}
            <ul class="form nobullets">
                <li>
                    <label for="txtName">
                        Your name *
                    </label>
                    <input type="text" class="text{if $warn_txtName} error{/if}" id="txtName" name="txtName" value="{$data.txtName}" />
                </li>
                <li>
                    <label for="txtEmail">
                        Your email address *
                    </label>
                    <input type="text" class="text{if $warn_txtEmail} error{/if}" id="txtEmail" name="txtEmail" value="{$data.txtEmail}" />
                </li>
                <li>
                    <label for="txtMessage">Your message *</label>
                    <textarea id="txtContactMessage" name="txtContactMessage" {if $warn_txtContactMessage}class="error"{/if}></textarea>
                </li>
            </ul>
            <small class="required"><span>*</span> = required information</small>
            <div class="buttons">
                <input type="submit" value="Next >" />
            </div>
        </form>
        
    {else}

        <div class="attention">
            <h3>Thanks! Your comments have been sent to the {$site_name} team</h3>
            <p>
                <a href="{$www_server}/groups/{$group->url_id}">Back to <em>{$group->name}</em></a>
                <br/>
               <a href="{$www_server}">Do a new search</a> 
            </p>
        </div>
    {/if}

{include file="../templates/footer.tpl"}