{include file="../templates/header.tpl"}
<form action="{$form_action}" method="post">
    {include file="../templates/formvars.tpl"}
    <fieldset>
        <input type="hidden" id="hidSaveMapData" value="1" />        
        <input type="hidden" id="hidLongBottomLeft" name="hidLongBottomLeft" value="{$group->long_bottom_left|escape:html}" />
        <input type="hidden" id="hidLatBottomLeft" name="hidLatBottomLeft" value="{$group->lat_bottom_left|escape:html}" />        
        <input type="hidden" id="hidLongTopRight" name="hidLongTopRight" value="{$group->long_top_right|escape:html}" />                    
        <input type="hidden" id="hidLatTopRight" name="hidLatTopRight" value="{$group->lat_top_right|escape:html}" />        
        <input type="hidden" id="hidLatCentroid" name="hidLatCentroid" value="{$group->lat_centroid|escape:html}" />
        <input type="hidden" id="hidLongCentroid" name="hidLongCentroid" value="{$group->long_centroid|escape:html}" />                        
        <input type="hidden" id="hidZoomLevel" name="hidZoomLevel" value="{$group->zoom_level|escape:html}" />                
    </fieldset>

    <div>
        <h3>Choose the <em>approximate</em> area covered by your group</h3>

        <div id="divMapWrapper">
            <div id="divMapSearch">
                <label for="txtMapSearch">Jump to location</label>
                <input type="text" class="text" id="txtSearchMap" onkeypress="return submitMapSearch(event);"/>
                <input type="button" onclick="javascript:searchMap();"value="Go" />
                <small>e.g. SW9 8JX or Manchester, UK</small>
            </div>
            <div id="divMap" style="width: 590px; height: 350px">
            
            </div>
        </div>
        <div class="buttons">
            <input type="submit" value="Contact details >" />
        </div>
    </div>
</form>
{include file="../templates/footer.tpl"}