{include file="../templates/header.tpl"}

<div class="attention">
    {if $show_sent == false}
        <h3>{l}Your group has been added!{/l}</h3>
        <p>
            <span class="highlight">{l}Do you know other people who run local groups?{/l}</span>
            <br/>
            <span class="highlight">{l}Use the form below to suggest they add it to {$site_name}!{/l}</span>
        </p>
        <form id="frmOwnerContact" action="{$form_action}" method="post">
            {include file="../templates/formvars.tpl"}
               <ul class="form nobullets">
                    <li>
                        <label for="txtEmail">
                            {l}Email addresses{/l} *
                        </label>
                        <textarea id="txtEmails" name="txtEmails" {if $warn_txtEmails}class="error"{/if}>{$data.txtEmails}</textarea>
                        &nbsp;<small>{l}separate addresses by commas{/l}</small>
                    </li>
                    <li>
                        <label for="txtMessage">{l}Your message{/l} *</label>
<textarea id="txtContactMessage" name="txtContactMessage" {if $warn_txtContactMessage}class="error"{/if}>{if $data.txtContactMessage == ''}
{l}Hi,

I've just added {$group->name} to {$site_name}, which is a website that helps people find local email lists, blogs and forums where they live, and thought you might want to add your group?

To add a group go to: {$www_server}

All the best

{$name}{/l}
    {else}{$data.txtContactMessage}{/if}</textarea>
                    </li>
                </ul>
                <small class="required"><span>*</span> = required information</small>
                <div class="buttons">
                    <input type="submit" value="Send message" />
                </div>
        </form>
    {else}
    <h3>{l}Your email has been sent!{/l}</h3>
        <p>
            {l}We have set up an email group for people who organise groups like yours{/l}
        </p>
        <p><a href="{$organisers_group_url}">{l}Click here to join the group organisers email group.{/l}</a></p>
    {/if}
</div>    

{include file="../templates/footer.tpl"}
