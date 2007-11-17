{include file="../templates/header.tpl"}

<div class="attention large">
    <h3>{$title}</h3>
    <p>
        {l}We have sent you an email to confirm {$confirm_type}, <span class="highlight">click on the link in the email</span> to {$action_result}. If you don't get an email in the next few minutes, try checking your spam filter.{/l}
    </p>
</div>    

{include file="../templates/footer.tpl"}
