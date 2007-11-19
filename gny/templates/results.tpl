{include file="../templates/header.tpl"}
    <form id="frmSearchPage" action="{$www_server}/results.php" method="post">
        {include file="../templates/formvars.tpl"}
        <fieldset>
            <input type="textbox" class="textbox" id="txtSearch" name="q" value="{$query_display_text|escape:html}"/>
            <input type="submit" class="button" value="Go" />
        </fieldset>
    </form>

    {if $groups|@sizeof >0}
    <h3 class="centerpage">{l}We found some groups for you!{/l}</h3>
        {foreach name="groups" from="$groups" item="group"}
            <div class="searchresult">
                <h4>
                    <a href="{$url}/groups/{$group->url_id}">{$group->name}</a> -  <em>{$group->byline}</em>
                </h4>
                <p>{$group->description|substr:0:200|strip_tags} <a href="{$url}/groups/{$group->url_id}">{l}read more...{/l}</a></p>
                {include file="../templates/hcard.tpl"}
            </div>
        {/foreach}
    {else}
        <div id="divResultsHelp" class="aligncenter">
            <h3>{l}Nobody has added any groups {if $place_name !=''}for {$place_name|escape:html}{else}for that location{/if} yet!{/l}</h3>
                <a href="{$www_server}/add/about/?q={$location}">{l}Add a group you know about {if $place_name !=''}in {$place_name|escape:html}{else}near {$query}{/if} &raquo;</a>{/l}
            <p>
                <a href="{$www_server}/add/about/?q={$location}">
                    <img src="{$www_server}/images/globe.png" alt="globe" title="{l}Add a group you know about {if $place_name !=''}in {$place_name|escape:html}{else}this location{/if}{/l}"/>
                </a>
                <br/>
                {l}
                    Help map the world&rsquo;s online communities by adding a community email group, <br/>forum or blog you know about{if $place_name !=''} in {$place_name|escape:html}{/if}.
                    <strong>It takes 4 simple steps to add a group.</strong>
                {/l} 
            </p>

        </div>
        <em id="emOr">or use PledgeBank.com to start one</em>        
        <form id="frmPledge"  accept-charset="utf-8" name="pledge" method="post" action="http://www.pledgebank.com/new">
			<ul class="form nobullets">
				<li>
					<label for="title">{l}I will{/l}</label>
						<textarea title="Pledge" name="title" id="txtTitle"rows="2">{l}setup a local email group to discuss what's going on in {if $place_name !=''}{$place_name}{else}[MY TOWN]{/if}{/l}</textarea>
					</p>
					<p>
						<label for="target">{l}but only if{/l}</label>
						<input title="Target number of people" size="2" type="text" id="txtTarget" name="target" value="5"/>
						<input type="hidden" id="hidType" name="type" value="other people">
						{l}other local people{/l}
					</p>
					<p>
						<label for="signup">{l}will{/l}</label>
						<input type="text" id="txtSignup" name="signup" value="{l}join the email group{/l}"/>
						<input type="hidden" name="date" value=""/>
						<input type="hidden" name="ref" value=""/> 
						<input type="hidden" name="detail" value="" />
						<input type="hidden" name="name" value=""/>
						<input type="hidden" name="email" value=""/>
						<input type="hidden" name="identity" value=""/>
						<input type="hidden" name="tags" value="{$site_name|lower}"/>
					</p>
				</li>

			</ul>
			<div class="buttons">
        	    <input class="button" type="submit" name="tostep1" value="{l}Continue on Pledgebank.com{/l} &raquo;"></p>
        	</div>
        </form>
        <p id="pPledgeBank">
    	    {l}PledgeBank is a website that lets you say you will do something, but only if some other people will help you. You get your own web page and TXT number to help you gather support, plus you can print posters to promote your pledge.{/l}
    	</p>
    {/if}

    <div id="divMeta">
        {l}There {if $groups|@sizeof == 1}is{else}are{/if} currently <strong>{$groups|@sizeof}</strong> {if $groups|@sizeof == 1}group{else}groups{/if} near {$query_display_text|escape:html}{/l}. 
        {l}You can get updates of new groups near {$query_display_text|escape:html} by subscribing to <a class="rss" href="{$rss_link}">this 
        <acronym title="Really simple syndication">rss</acronym> feed</a> or view the areas covered by 
        groups on this page <a href="http://maps.google.com/maps?f=q&hl=en&q={$rss_link|escape:url}&layer=&ie=UTF8&z=13&om=1">on a map</a>{/l}. {l}You can permanently link to this page <a href="{$current_url}">here</a>{/l}.
    </div>
{include file="../templates/footer.tpl"}            
