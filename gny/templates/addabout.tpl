{include file="../templates/header.tpl"}
    <form action="{$form_action}" method="post">
        {include file="../templates/formvars.tpl"}
        <h3>Tell us a bit about this email group, forum or blog</h3>
	<p>You can help people in your neighbourhood get to know each other.
	Please add any local group you know about, to help more people join up!
	</p>
        <ul class="form nobullets">
            <li>
                <label for="txtName">Group name *</label>
                <input type="text" class="textbox{if $warn_txtName} error{/if}" id="txtName" name="txtName" value="{$group->name}" />
            </li>
            <li>
                <label for="txtByline">One line description *</label>
                <input type="text" class="textbox{if $warn_txtByline} error{/if}" id="txtByline" name="txtByline" value="{$group->byline}" />
                <small>e.g. A residents&rsquo; email group for Woking, UK</small>
            </li>
            <li>
                <label for="txtDescription">More information (optional)</label>
                <textarea class="textbox{if $warn_txtDescription} error{/if}" id="txtDescription" name="txtDescription">{$group->description}</textarea>
                <br/>
                <small id="smlDescriptionHint">Tell us what your group does. Some <acronym title="html is web page code in case you were wondering">html</acronym> is ok (<acronym title="link to a web page">&lt;a&gt;</acronym>, <acronym title="italic text">&lt;em&gt;</acronym>, <acronym title="bold text">&lt;strong&gt;</acronym>).</small>
            </li>
            <li>
                <label for="txtTags">Keywords for this group</label>
                <input type="text" class="textbox large{if $warn_txtTags} error{/if}" id="txtTags" name="txtTags" value="{$group->tags}"  title="Add tags to help people find this group"/>
                <small>e.g. <em>crime, environment, Camden</em></small>
            </li>
        </ul>    
         <small class="required"><span>*</span> = required information</small>
        <div class="buttons">
            <input type="submit" value="Area covered >" />
        </div>
    </form>
{include file="../templates/footer.tpl"}        
