{include file="../templates/header.tpl"}
    <form id="frmSearchMain" action="{$form_action}" method="post">
        {include file="../templates/formvars.tpl"}
        <div id="divMainSearch">
            <label for="txtSearch">
                Find email lists and web communities <br/>where you live
            </label>
            <input type="text" id="txtSearch" name="txtSearch" class="textbox{if $warn_txtSearch} error{/if}" 
                onclick="if (this.value=='{$search_hint}') this.value='';" value="{if $data.txtSearch == ''}{$search_hint}{else}$data.txtSearch{/if}"/>
            <input type="submit" id="btnSearch" name="btnIndex" value="Go" />
            <small>
                {if $country == 'US'}
                    e.g. <em>94105</em> or <em>San Francisco</em>
                {elseif  $country == 'GB'}
                    e.g. <em>SW9 8JX</em> or <em>Brixton</em>
                {else}
                    e.g. <em>Berlin</em> or <em>Gdansk</em>
                {/if}
            </small>
        </div>
        <div id="divFrontLeft">
            <h3>Recently added groups</h3>
            <ul class="nobullets">
                {foreach name="groups" from="$groups" item="group"}
                    <li>
                        <a href="{$www_server}/groups/{$group->url_id}">{$group->name}</a> -  <em>{$group->byline}</em>
                    </li>
                {/foreach}
            </ul>
        </div>
        <div id="divFrontRight">
            <h3>Want to add your group?</h3>
            <p>
                <strong>It's simple, just 3 steps</strong>. Tell us what the group does,what area it covers and how 
                people near you can get involved.<br/>
                <a id="aGetStarted" href="{$www_server}/add/about/">Get started &gt;&gt;</a>
            </p>
        </div>
    </form>
{include file="../templates/footer.tpl"}
