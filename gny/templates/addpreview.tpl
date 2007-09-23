{include file="../templates/header.tpl"}
<form id="frmAddContact" action="{$form_action}" method="post">
    {include file="../templates/formvars.tpl"}

    <h3>This is how the group will appear, review it then click confirm</h3>
    {include file="../templates/groupdetail.tpl"}
    
    <p id="pEditGroup">
        <span class="highlight">Something wrong? <a href="{$www_server}/add/about/">click here to edit</a></span>
    </p>

    <div class="buttons">
        <input type="submit" class="button" value="Confirm this group >"/>
    </div>
    
</form>

{include file="../templates/footer.tpl"}