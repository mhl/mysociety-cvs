{include file="../templates/header.tpl"}
    <div class="contentfull">
        <h3>{l}Tell us a bit about this email group, forum or blog{/l}</h3>
    </div>
    <form action="{$form_action}" method="post">
        <div class="contentwide">
            {include file="../templates/formvars.tpl"}
            <ul class="form nobullets">
                <li>
                    <label for="txtName">{l}Group name{/l} *</label>
                    <input type="text" class="textbox{if $warn_txtName} error{/if}" id="txtName" name="txtName" value="{$group->name}" />
                </li>
                <li>
                    <label for="txtByline">{l}Short description{/l} *</label>
                    <input type="text" class="textbox{if $warn_txtByline} error{/if}" id="txtByline" name="txtByline" maxlength="70" value="{$group->byline}" />
                    <small  class="textboxhint">{l}e.g. A residents&rsquo; email group for Woking, UK{/l}</small>
                </li>
                <li>
                    <label for="txtDescription">{l}More information{/l}</label>
                    <textarea class="textbox{if $warn_txtDescription} error{/if}" id="txtDescription" name="txtDescription" cols="8" rows="5">{$group->description}</textarea>
                    <small class="textboxhint">{l}Tell what your group does.{/l} {l}Some <acronym title="html is web page code in case you were wondering">html</acronym> is ok{/l} (<acronym title="link to a web page">&lt;a&gt;</acronym>, <acronym title="italic text">&lt;em&gt;</acronym>, <acronym title="bold text">&lt;strong&gt;</acronym>).</small>
                </li>
                <li id="liCategory">
                    <label for="ddlCategory">{l}Type of group{/l}</label>
                    <select id="ddlCategory" name="ddlCategory" {if $warn_ddlCategory}class="error"{/if}>
                        <option value="0" {if $group->category_id == 0 || $group->category_id == ""}selected="selected"{/if}>
                            &nbsp;
                        </option>
                        {foreach from="$categories" item="category"}
                            <option value="{$category->category_id}" {if $group->category_id == $category->category_id}selected="selected"{/if}>
                                {$category->name} ({$category->hint})
                            </option>
                        {/foreach}
                    </select>
                </li>
                <li>
                    <label for="txtTags">{l}Keywords for group{/l}</label>
                    <input type="text" class="textbox{if $warn_txtTags} error{/if}" id="txtTags" name="txtTags" value="{$group->tags}"  title="{l}Add tags to help people find this group{/l}"/>
                    <small class="textboxhint">{l}e.g. <em>crime, environment, Camden</em>{/l}</small>
                </li>
            </ul>    
             <small class="required"><span>*</span> = {l}required information{/l}</small>
        </div>
        <div class="contentnarrow">
        	<p class="note">
        	    {l}Please add any local online groups you know about, it'll help more people in your community to start talking!{/l}
        	</p>        
        </div>
        <div class="contentfull">
	    <br class="clear"/>
            <div class="buttons">
                <input type="submit" value="{l}Area covered{/l} &raquo;" />
            </div>
        </div>
    </form>
{include file="../templates/footer.tpl"}        
