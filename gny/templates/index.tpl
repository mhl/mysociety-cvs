{include file="../templates/header.tpl"}

    <div id="divHome">
        <span class="corneralt_tl corner">&nbsp;</span>
        <span class="corneralt_tr corner">&nbsp;</span>
        <div class="contentleft">
            <div id="divBubble">
                <span class="corner">&nbsp;</span>
                <p>
                    We don't talk enough...
                    <br/>
                    <strong>Groups Near You</strong> helps people in your neighbourhood
                    get to know each other
                </p>
                <div id="divPeople">
                    <span class="corner_bl corner">&nbsp;</span>
                </div>
            </div>
        </div>
        <div class="contentright">
            <form id="frmSearchMain" action="{$form_action}" method="post" class="pod">
                <fieldset>
                    {include file="../templates/formvars.tpl"}
                    <h4>
                    <label for="txtSearch">
                        {l}Find email groups and social networks where you live{/l},
                    </label>
                    </h4>
                    <input type="text" id="txtSearch" name="txtSearch" class="textbox{if $warn_txtSearch} error{/if}" 
                        onclick="if (this.value=='{$search_hint}') this.value='';" value="{if $data.txtSearch == ''}{$search_hint}{else}$data.txtSearch{/if}"/>
                    <input type="submit" id="btnSearch" name="btnIndex" value="{l}Go{/l}" />
                    <br/>
                    <small>
                        {*
                        {if $country == 'US'}
                            e.g. <em><a href="{$www_server}/search/94105/">94105</a></em> or <em><a href="{$www_server}/search/San Francisco/">San Francisco</a></em>
                        {elseif  $country == 'GB'}
                        *}
                            e.g. <em><a href="{$www_server}/search/sw98jx/">SW9 8JX</a></em> or <em><a href="{$www_server}/search/brixton/-0.100,51.467">Brixton</a></em>
                        {*
                        {else}
                            e.g. <em><a href="{$www_server}/search/berlin/13.400,52.517">Berlin</a></em> or <em><a href="{$www_server}/search/barcelona/2.183,41.383">Barcelona</a></em>
                        {/if}
                        *}
                    </small>
                </fieldset>
            </form>
        </div>
        <br class="clear"/>
    </div>

    {* Get involved *}
    <div id="divGetInvolved" class="contentfull">
        <h4>{l}Help us map the world's online communities!{/l}</h4>
        <p>
            {l}
                We need *your* help to map all those hidden neighbourhood email lists, forums and community blogs where you live.
               Help us map some random groups from the web, or add a group you know about.
            {/l}
            <a class="largelinkbutton" href="{$www_server}/add/start/">
                <span class="left">&nbsp;</span>
                <span class="middle">{l}Add a group now{/l} &raquo;</span>                
                <span class="right">&nbsp;</span>                
            </a>
        </p>
    </div>
    <hr/>
    {* Recent groups *}
    <div id="divRecent" class="contentfull">
        <h4>{l}Recently added groups{/l}</h4>
        <ul class="nobullets">
            {foreach name="groups" from="$map_groups" item="group"}
                <li>
                    <a href="{$www_server}/groups/{$group->url_id}" title="{$group->byline}">
                        {$group->name}
                    </a>
                </li>
            {/foreach}
        </ul>
        <a href="{$www_server}/browse/">{l}Browse all groups{/l} &raquo;</a>        
        <div id="divLatestMap">
        
        </div>
    </div>
    <hr/>    
    <div id="divStartGroup" class="contentfull">
        <h4>{l}No groups near you? Start your own...{/l}</h4>
        <p>
            {l}Starting an email group for your neighbourhood can make a real difference to the community you live in.
            You can start one now, for free, using one of these sites. 
            Then use <a href="http://www.pledgebank.com">Pledge Bank</a> to gather support.
            {/l}
        </p>
        <ul id="ulGroupSoftware" class="inline">
            <li>
                <a href="http://groups.yahoo.com">
                    <img src="{$www_server}/images/yahoo.png" alt="Yahoo! Groups" title="Yahoo! Groups"/>
                </a>
            </li>
            <li>
                <a href="http://groups.google.com">
                    <img src="{$www_server}/images/google.png" alt="Google Groups" title="Google Groups"/>
                </a>
            </li>
            <li>
                <a href="http://www.facebook.com/">
                    <img src="{$www_server}/images/facebook.png" alt="Facebook" title="Facebook"/>
                </a>
            </li>
        </ul>
    </div>

    <br class="clear"/>
    
    {* group info for populated google map *}
    <fieldset>
        {foreach name="groups" from="$map_groups" item="group"}
            <input type="hidden" class="groupdata" value="{literal}{{/literal}long: {$group->long_centroid}, lat: {$group->lat_centroid}, name:'{$group->name|escape:javascript}'{literal}}{/literal}"/>
        {/foreach}
    </fieldset>
    
{include file="../templates/footer.tpl"}
