{include file="../templates/header.tpl"}
<form id="frmAddContact" action="{$form_action}" method="post">
    {include file="../templates/formvars.tpl"}

    {include file="../templates/groupdetail.tpl"}

    <div class="buttons">
        <input type="submit" class="button" value="Confirm >"/>
    </div>
    
</form>

{include file="../templates/footer.tpl"}