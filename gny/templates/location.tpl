{include file="../templates/header.tpl"}

{* Check if gaze is up *}
{if $gaze_down == false}

    {if $country_code != ''}
        {* We have results! display them *}
        {if $found_places}
            <h3>Please confirm which place you are looking for</h3>
            <ul class="nobullets">
                {foreach name="places" from="$places" item="place"}
                    <li>
                        <a href="{$www_server}/search/{$place.name|escape:url}/{$place.longitude},{$place.latitude}">
                            {$place.name}{if $place.state !=''} ({$place.state}){/if}{if $place.near != ''} (near {$place.near}){/if}
                        </a>
                        <small><a href="http://maps.google.com/maps?ll={$place.latitude},{$place.longitude}&amp;z=12" class="quiet">[check on map]</a></small>
                    </li>
                {/foreach}
            </ul>
        
            {* Search form *}
            <form id="frmSearchPlaceName" action="{$form_action}" method="post">
                {include file="../templates/formvars.tpl"}
                <fieldset>
                    <label for="txtSearch">Change location?</label>
                    <input type="textbox" class="textbox" id="txtSearch" name="q" value="{$search_term}"/>
                    <select id="ddlCountry" name="country_code">
                        {foreach name="countries" from="$countries" item="country"}                
                            <option value="{$country->iso}"{if $country_code == $country->iso}selected="selected"{/if}>
                                {$country->printable_name}
                            </option>
                        {/foreach}
                    </select>
                    <input type="submit" class="button" value="Go" />
                </fieldset>
            </form>
        {else}
            {* No places found *}
            <div class="attention">
                <h3>Sorry, we couldn't find anywhere called {$search_term}</h3>
                <form id="frmSearchAgain" action="{$form_action}" method="post">
                    {include file="../templates/formvars.tpl"}
                    <fieldset>
                        <label for="txtSearch">Try another place name?</label>
                        <input type="textbox" class="textbox" id="txtSearch" name="q" value="{$search_term}"/>
                        <select id="ddlCountry" name="country_code">
                            {foreach name="countries" from="$countries" item="country"}                
                                <option value="{$country->iso}"{if $country_code == $country->iso}selected="selected"{/if}>
                                    {$country->printable_name}
                                </option>
                            {/foreach}
                        </select>
                        <input type="submit" class="button" value="Go" />
                    </fieldset>
                </form>
            </div>
            
        {/if}
    {else}
        <div class="attention">
            <h3>Please choose which country you are in</h3>
            <form id="frmSearchPlace" action="{$form_action}" method="post">
                {include file="../templates/formvars.tpl"}
                <fieldset>
                    <input type="hidden" name="q" value="{$search_term}"/>
                    <select id="ddlCountry" name="country_code">
                            <option></option>
                        {foreach name="countries" from="$countries" item="country"}                
                            <option value="{$country->iso}">
                                {$country->printable_name}
                            </option>
                        {/foreach}
                    </select>
                    <input type="submit" class="button" value="Go" />
                </fieldset>
            </form>
        </div>
    {/if}

{else}

    <div class="attention">
        
        <h3>Unable to search by place name</h3>
        <p>
            Sorry, searching by place name is currently unavailable. Please try again later, or <a href="{$www_server}">search by post code or zip code</a>
        </p>
    </div>

{/if}

{include file="../templates/footer.tpl"}
