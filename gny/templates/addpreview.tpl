{include file="../templates/header.tpl"}
<form id="frmAddContact" action="{$form_action}" method="post">
    {include file="../templates/formvars.tpl"}
    <fieldset>
        <input type="hidden" id="hidSaveMapData" value="0" />
        <input type="hidden" id="hidMiniMap" value="{$mini_map}" />        
    </fieldset>

    <h3>{l}This is how your group will appear, review it then click confirm{/l}</h3>
    {include file="../templates/groupdetail.tpl"}
    
    <p id="pEditGroup">
        <span class="highlight">{l}Something wrong? <a href="{$www_server}/add/about/">click here to edit{/l}</a></span>
    </p>

    <div class="buttons">
        <input type="submit" class="button" value="{l}Confirm this group{/l} >"/>
    </div>
    
</form>

{include file="../templates/footer.tpl"}