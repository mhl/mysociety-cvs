{include file="../templates/header.tpl"}

<div class="attention">
    {if $show_sent == false}
        <h3>Your group has been added!</h3>
        <p>
            <span class="highlight">Do you know other people who run local groups?</span>
            <br/>
            <span class="highlight">Use the form below to suggest they add it to {$site_name}!</span>
        </p>
        <form id="frmOwnerContact" action="{$form_action}" method="post">
            {include file="../templates/formvars.tpl"}
               <ul class="form nobullets">
                    <li>
                        <label for="txtEmail">
                            Email addresses *
                        </label>
                        <textarea id="txtEmails" name="txtEmails" {if $warn_txtEmails}class="error"{/if}>{$data.txtEmails}</textarea>
                        &nbsp;<small>separate addresses by commas</small>
                    </li>
                    <li>
                        <label for="txtMessage">Your message *</label>
<textarea id="txtContactMessage" name="txtContactMessage" {if $warn_txtContactMessage}class="error"{/if}>{if $data.txtContactMessage == ''}
Hi,

I've just added {$group->name} to {$www_server}, which is a website that helps people find local email lists, blogs and forums where they live,
and thought you might be interested in adding your group?

All the best

{$group->created_name}
    {else}{$data.txtContactMessage}{/if}</textarea>
                    </li>
                </ul>
                <small class="required"><span>*</span> = required information</small>
                <div class="buttons">
                    <input type="submit" value="Send message" />
                </div>
        </form>
    {else}
    <h3>Your email has been sent!</h3>
        <p>
            We have set up an email group for people who organise groups like yours
        </p>
        <p><a href="{$organisers_group_url}">Click here to join the group organisers email group.</a></p>
    {/if}
</div>    

{include file="../templates/footer.tpl"}
