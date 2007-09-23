{include file="../templates/header.tpl"}
<form id="frmAddContact" action="{$form_action}" method="post">
    {include file="../templates/formvars.tpl"}

    <h3>How do people join the group?</h3>
    <div>
        <ul id="ulInvolved" class="nobullets">
            <li>
                <input type="radio" class="radio" id="radInvolvedType_web" name="radInvolvedType" {if $group->involved_type == "link"}checked="checked"{/if} onclick="javascript:changeInvolvedType();" value="link"/>            
                <label for="radInvolvedType_web">Via a web page</label>   
                <input type="text" class="textbox large{if $warn_txtInvolvedLink} error{/if}" id="txtInvolvedLink" name="txtInvolvedLink" value="{$group->involved_link}" />                
                <small>e.g. a website or a google/yahoo groups page</small>
            </li>
            <li>
                <input type="radio" class="radio" id="radInvolvedType_email" name="radInvolvedType" {if $group->involved_type == "email"}checked="checked"{/if} onclick="javascript:changeInvolvedType();" value="email"/>
                <label for="radInvolvedType_email">Email for more information</label>        
                <input type="text" class="textbox large{if $warn_txtInvolvedEmail} error{/if}" id="txtInvolvedEmail" name="txtInvolvedEmail" value="{$group->involved_email}" />
                <small>people will be able to email this via the site, but won't be published</small>
            </li>
        </ul>
    </div>
    
    <h3>About you</h3>
    <ul class="form nobullets">
        <li>
            <label for="txtCreatedName">Your name *</label>
            <input type="text" class="textbox large{if $warn_txtCreatedName} error{/if}" id="txtCreatedName" name="txtCreatedName" value="{$group->created_name}" />
        </li>
        <li>
            <label for="txtCreatedEmail">Your email *</label>
            <input type="text" class="textbox large{if $warn_txtCreatedEmail} error{/if}" id="txtCreatedEmail" name="txtCreatedEmail" value="{$group->created_email}" />
            <small>This will not be published and <span class="highlight">we will not spam you</span></small>
        </li>
    </ul>

    <div class="buttons">
        <input type="submit" class="button" value="Preview &amp; confirm >"/>
    </div>
</form>
{include file="../templates/footer.tpl"}