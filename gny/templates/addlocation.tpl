{include file="../templates/header.tpl"}
<form action="{$form_action}" method="post">
    {include file="../templates/formvars.tpl"}
    <fieldset>
        <input type="hidden" id="hidSaveMapData" value="1" />    
        <input type="hidden" id="hidMiniMap" value="{$mini_map}" />
        <input type="hidden" id="hidLongBottomLeft" name="hidLongBottomLeft" value="{$group->long_bottom_left|escape:html}" />
        <input type="hidden" id="hidLatBottomLeft" name="hidLatBottomLeft" value="{$group->lat_bottom_left|escape:html}" />
        <input type="hidden" id="hidLongTopRight" name="hidLongTopRight" value="{$group->long_top_right|escape:html}" />
        <input type="hidden" id="hidLatTopRight" name="hidLatTopRight" value="{$group->lat_top_right|escape:html}" />
        <input type="hidden" id="hidLatCentroid" name="hidLatCentroid" value="{$group->lat_centroid|escape:html}" />
        <input type="hidden" id="hidLongCentroid" name="hidLongCentroid" value="{$group->long_centroid|escape:html}" />
        <input type="hidden" id="hidZoomLevel" name="hidZoomLevel" value="{$group->zoom_level|escape:html}" />
    </fieldset>

    <div>
	<div id="mapNo">
	        <h3>{l}Describe the <em>approximate</em> area covered by the group{/l}</h3>

		<textarea name="txtLocationDesc" id="txtLocationDesc" rows=10 cols=70>{$group->location_desc|escape:html}</textarea>

	</div>

        <div id="mapYes">

        <h3>{l}Choose the <em>approximate</em> area covered by the group using the red box{/l}</h3>

        <div id="divMapWrapper">
            <div id="divMapSearch">
                <label for="txtMapSearch">{l}Go to location{/l}</label>
                <input type="text" class="text" id="txtSearchMap" onkeypress="return submitMapSearch(event);"/>
                <input id="btnMapSearch" type="button" onclick="javascript:searchMap();"value="Go" />
                <img id="imgMapLoading" src="{$www_server}/images/maploading.gif" width="16px" height="16px" alt="Loading ..." title="Loading ..."/>
                <small>
                    {if $country_code == 'US'}
                        {l}e.g. <em>94105</em> or <em>San Francisco</em> or <em>London, UK</em>{/l}
                    {elseif  $country_code == 'GB'}
                        {l}e.g. <em>SW9 8JX</em> or <em>Manchester</em> or <em>San Francisco, US</em>{/l}
                    {else}
                        {l}e.g. <em>Paris, France</em> or <em>Sydney, Australia</em>{/l}
                    {/if}
                </small>
            </div>
            <div id="divMap" style="width: 590px; height: 350px">
            
            </div>
        </div>

	</div>

        <div class="buttons">
            <input type="submit" value="{l}Joining the group{/l} &raquo;" />
        </div>
    </div>
</form>
{include file="../templates/footer.tpl"}
