{include file="../templates/header.tpl"}

<p id="frontAddBlurb">This site hasn't officially launched yet. We need your knowledge
about local groups near you to help it grow. <a href="/add/about/">Add a group now!</a>
</p>

    <form id="frmSearchMain" action="{$form_action}" method="post">
        {include file="../templates/formvars.tpl"}
        <div id="divMainSearch">
            <label for="txtSearch">
                {l}Find email groups and web communities <br/>where you live{/l}
            </label>
            <input type="text" id="txtSearch" name="txtSearch" class="textbox{if $warn_txtSearch} error{/if}" 
                onclick="if (this.value=='{$search_hint}') this.value='';" value="{if $data.txtSearch == ''}{$search_hint}{else}$data.txtSearch{/if}"/>
            <input type="submit" id="btnSearch" name="btnIndex" value="{l}Go{/l}" />
            <small>
                {if $country == 'US'}
                    e.g. <em><a href="{$www_server}/search/94105/">94105</a></em> or <em><a href="{$www_server}/search/San Francisco/">San Francisco</a></em>
                {elseif  $country == 'GB'}
                    e.g. <em><a href="{$www_server}/search/sw98jx/">SW9 8JX</a></em> or <em><a href="{$www_server}/search/brixton/">Brixton</a></em>
                {else}
                    e.g. <em><a href="{$www_server}/search/berlin/13.400,52.517">Berlin</a></em> or <em><a href="{$www_server}/search/barcelona/2.183,41.383">Barcelona</a></em>
                {/if}
            </small>
        </div>
        <div id="divFrontLeft">
            <h3>{l}Recently added groups{/l}</h3>
            <ul class="nobullets">
                {foreach name="groups" from="$groups" item="group"}
                    <li>
                        <a href="{$www_server}/groups/{$group->url_id}">{$group->name}</a> -  <em>{$group->byline}</em>
                    </li>
                {/foreach}
            </ul>
            <a id="aBrowseAll" href="{$www_server}/browse/">{l}Browse all groups{/l} &gt;&gt;</a>
        </div>
        <div id="divFrontRight">
            <h3>{l}Help us map the worlds online communities{/l}</h3>
            <p>
                <strong>{l}It's simple, just 4 steps to add any group you know about{/l}</strong>. {l}Tell us what the group does, what area it covers and how 
                people near you can get involved, then confirm the details.{/l}<br/>
                <a id="aGetStarted" href="{$www_server}/add/about/">{l}Add a group now{/l} &gt;&gt;</a>
            </p>
        </div>
    </form>
{include file="../templates/footer.tpl"}
