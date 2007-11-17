{include file="../templates/header.tpl"}
    <form action="{$form_action}" method="post">
        {include file="../templates/formvars.tpl"}

    <h3>{l}Tell us a bit about this email group, forum or blog{/l}</h3>
	<p id="pAddInitBlurb">{l}By adding a group you can help people in your neighbourhood get to know each other.{/l}
	{l}<span class="highlight">Please add any local group you know about</span>, to help more people join up!{/l}
	</p>
        <ul class="form nobullets">
            <li>
                <label for="txtName">{l}Group name{/l} *</label>
                <input type="text" class="textbox{if $warn_txtName} error{/if}" id="txtName" name="txtName" value="{$group->name}" />
            </li>
            <li>
                <label for="txtByline">{l}One line description{/l} *</label>
                <input type="text" class="textbox{if $warn_txtByline} error{/if}" id="txtByline" name="txtByline" value="{$group->byline}" />
                <small>{l}e.g. A residents&rsquo; email group for Woking, UK{/l}</small>
            </li>
            <li>
                <label for="txtDescription">{l}More information (optional){/l}</label>
                <textarea class="textbox{if $warn_txtDescription} error{/if}" id="txtDescription" name="txtDescription">{$group->description}</textarea>
                <br/>
                <small id="smlDescriptionHint">{l}Tell what your group does.{/l} {l}Some <acronym title="html is web page code in case you were wondering">html</acronym> is ok{/l} (<acronym title="link to a web page">&lt;a&gt;</acronym>, <acronym title="italic text">&lt;em&gt;</acronym>, <acronym title="bold text">&lt;strong&gt;</acronym>).</small>
            </li>
            <li>
                <label for="txtTags">{l}Keywords for this group{/l}</label>
                <input type="text" class="textbox large{if $warn_txtTags} error{/if}" id="txtTags" name="txtTags" value="{$group->tags}"  title="{l}Add tags to help people find this group{/l}"/>
                <small>{l}e.g. <em>crime, environment, Camden</em>{/l}</small>
            </li>
        </ul>    
         <small class="required"><span>*</span> = {l}required information{/l}</small>
        <div class="buttons">
            <input type="submit" value="{l}Area covered{/l} >" />
        </div>
    </form>
{include file="../templates/footer.tpl"}        
