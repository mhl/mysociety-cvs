{include file="../templates/header.tpl"}
<form id="frmAddContact" action="{$form_action}" method="post">
    {include file="../templates/formvars.tpl"}

    <h3>{l}How do people join the group? *{/l}</h3>
    <div>
        <ul id="ulInvolved" class="nobullets">
            <li>
                <input type="radio" class="radio" id="radInvolvedType_web" name="radInvolvedType" {if $group->involved_type == "link"}checked="checked"{/if} onclick="javascript:changeInvolvedType();" value="link"/>            
                <label for="radInvolvedType_web">{l}Via a web page{/l}</label>   
                <input type="text" class="textbox large{if $warn_txtInvolvedLink} error{/if}" id="txtInvolvedLink" name="txtInvolvedLink" value="{$group->involved_link}" />                
                <small>{l}e.g. a website or a Google/ Yahoo/ Facebook groups page{/l}</small>
            </li>
            <li>
                <input type="radio" class="radio" id="radInvolvedType_email" name="radInvolvedType" {if $group->involved_type == "email"}checked="checked"{/if} onclick="javascript:changeInvolvedType();" value="email"/>
                <label for="radInvolvedType_email">{l}Email for more information{/l}</label>        
                <input type="text" class="textbox large{if $warn_txtInvolvedEmail} error{/if}" id="txtInvolvedEmail" name="txtInvolvedEmail" value="{$group->involved_email}" />
                <small>{l}will <strong>not</strong> be published, but people will be able to contact it{/l}</small>
            </li>
        </ul>
    </div>
    
    <h3>{l}About you{/l}</h3>
    <ul class="form nobullets">
        <li>
            <label for="txtCreatedName">{l}Your name{/l} *</label>
            <input type="text" class="textbox large{if $warn_txtCreatedName} error{/if}" id="txtCreatedName" name="txtCreatedName" value="{$group->created_name}" />
        </li>
        <li>
            <label for="txtCreatedEmail">{l}Your email{/l} *</label>
            <input type="text" class="textbox large{if $warn_txtCreatedEmail} error{/if}" id="txtCreatedEmail" name="txtCreatedEmail" value="{$group->created_email}" />
            <small>{l}This will not be published and <span class="highlight">we will not spam you</span>{/l}</small>
        </li>
    </ul>
    <small class="required"><span>*</span> = {l}required information{/l}</small>
    <div class="buttons">
        <input type="submit" class="button" value="{l}Preview &amp; confirm{/l} &raquo;"/>
    </div>
</form>
{include file="../templates/footer.tpl"}
