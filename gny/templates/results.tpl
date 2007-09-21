{include file="../templates/header.tpl"}
    <form id="frmSearchPage" action="{$www_server}/results.php" method="post">
        {include file="../templates/formvars.tpl"}
        <fieldset>
            <input type="textbox" class="textbox" id="txtSearch" name="q" value="{$query_display_text}"/>
            <input type="submit" class="button" value="Go" />
        </fieldset>
    </form>

    {if $groups|@sizeof >0}
    <h3 class="centerpage">We found some groups for you!</h3>
        {foreach name="groups" from="$groups" item="group"}
            <div class="searchresult">
                <h4>
                    <a href="{$url}/groups/{$group->url_id}">{$group->name}</a> -  <em>{$group->byline}</em>
                </h4>
                <p>{$group->description|substr:0:200|strip_tags}...</p>
            </div>
        {/foreach}
    {else}
        <h3 class="centerpage">Sorry, we couldn't find any groups for {if $place_name !=''}{$place_name}{else}that location{/if}</h3>
        <form id="frmPledge" accept-charset="utf-8" name="pledge" method="post" action="http://www.pledgebank.com/new">
            <h4>Never mind. Why not use Pledgebank.com to start one?</h4>
			<ul class="form nobullets">
				<li>
					<label for="title">I will</label>
						<textarea title="Pledge" name="title" id="txtTitle"rows="2">setup a local email group to discuss what's going on in {if $place_name !=''}{$place_name}{else}[MY TOWN]{/if}</textarea>
					</p>
					<p>
						<label for="target">but only if</label>
						<input title="Target number of people" size="2" type="text" id="txtTarget" name="target" value="5">
						<input type="hidden" id="hidType" name="type" value="other people">
						other local people
					</p>
					<p>
						<label for="signup">will</label>
						<input type="text" id="txtSignup" name="signup" value="join the email group">
						<input type="hidden" name="date" value="">
						<input type="hidden" name="ref" value=""> 
						<input type="hidden" name="detail" value="" />
						<input type="hidden" name="name" value="">
						<input type="hidden" name="email" value="">
						<input type="hidden" name="identity" value=""></p>
				</li>

			</ul>
			<p>
        	    PledgeBank.com lets you say you will do something, but only if some other people will help you. You get your own web page and TXT number to help you gather support, plus you can print posters to promote your pledge.
        	</p>
			<div class="buttons">
        	    <input class="button" type="submit" name="tostep1" value="Continue on Pledgebank.com &gt;&gt;"></p>
        	</div>
        </form>
    {/if}
    
    <div id="divMeta">
        There are currently <strong>{$groups|@sizeof}</strong> groups near {$query_display_text}. 
        You can get updates of near new groups near {$query_display_text} by subscribing to <a class="rss" href="{$rss_link}">this 
        <acronym title="Really simple syndication">rss</acronym> feed</a> or view the areas covered by 
        groups on this page <a href="http://maps.google.com/maps?f=q&hl=en&q={$rss_link}&layer=&ie=UTF8&z=13&om=1">on a map</a>. You can permanently link to this page <a href="{$current_url}">here</a>.
    </div>
{include file="../templates/footer.tpl"}            