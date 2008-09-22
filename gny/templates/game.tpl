{include file="../templates/header.tpl"}

	<!-- inputs -->
	<fieldset>
        <input type="hidden" id="hidGameHash" value="" />
        <input type="hidden" id="hidMaxMapZoom" value="{$max_map_zoom}" />
        <input type="hidden" id="hidSaveMapData" value="1" />    
        <input type="hidden" id="hidMiniMap" value="{$mini_map}" />
        <input type="hidden" id="hidLongBottomLeft" name="hidLongBottomLeft" value="" />
        <input type="hidden" id="hidLatBottomLeft" name="hidLatBottomLeft" value="" />
        <input type="hidden" id="hidLongTopRight" name="hidLongTopRight" value="" />
        <input type="hidden" id="hidLatTopRight" name="hidLatTopRight" value="" />
        <input type="hidden" id="hidLatCentroid" name="hidLatCentroid" value="" />
        <input type="hidden" id="hidLongCentroid" name="hidLongCentroid" value="" />
        <input type="hidden" id="hidZoomLevel" name="hidZoomLevel" value="" />
        <input type="hidden" id="hidName" value="{$game_name}" />
        <input type="hidden" id="hidEmail" value="{$game_email}" />
        <input type="hidden" id="hidGroupName" value="" />
    </fieldset>

        <div class="contentfull">
			
			<!-- thanks -->
			<div id="divThanks">
				
			</div>
			
			<!-- choose -->
			<div id="divGameChoose">
				<h3>1) Does this look like a local group?</h3>

				<h4 id="hTitle1">

				</h4>
				<a id="aLink1" accesskey="v" href="" target="_new"><span class="accesskey">V</span>iew website (new window)</a>&nbsp;&nbsp;
				
				<a id="aGoogle1" accesskey="g" href="" target="_new"><span class="accesskey">G</span>oogle this group (new window)</a>
				<div id="divGameGroupText" taborder="10">
					&nbsp;
				</div>
				<div class="buttons">
					<small>(Windows &amp; Unix: Alt + n, Alt + k, Alt + y / Mac: Ctrl + n, Ctrl + k, Ctrl + y)</small>					
					<input type="button" onclick="gameNotLocal();setupGame();" accesskey="n" value="Nope"/>
					<input type="button" onclick="setupGame();" accesskey="k" value="Unsure, skip it"/>					
					<input type="button" onclick="showGameDetail();" accesskey="y" value="Yes it does!"/>
				</div>
			</div>

			<!-- Detail -->
			<div id="divGameDetail">
				<h3>2) Tidy up the description and choose a category</h3>
				<h4 id="hTitle2">

				</h4>		
				<a id="aLink2" accesskey="v" href="" target="_new"><span class="accesskey">V</span>iew website (new window)</a>&nbsp;&nbsp;
				<a id="aGoogle2" accesskey="g" href="" target="_new"><span class="accesskey">G</span>oogle this group (new window)</a>
				<ul class="form nobullets">
					<li>
						<textarea id="txtGameDetail" taborder="20"></textarea>
					</li>
					<li>
						<label for="ddlCategory">Choose a category</label>
	                    <select id="ddlCategory" taborder="30">
								<option value="0">&nbsp;</option>
	                        {foreach from="$categories" item="category"}
	                            <option value="{$category->category_id}">
	                                {$category->name} ({$category->hint})
	                            </option>
	                        {/foreach}
	                    </select>
					</li>
					<li>
						<label for="txtGameTags">Add some tags (optional)</label>						
						<input type="text" id="txtGameTags" taborder="40" value=""/>
						<br/>
						<small>
							e.g. <a href="javascript:gameSetTag('crime');">crime</a>,
							<a href="javascript:gameSetTag('residents association');">residents association,</a>
							<a href="javascript:gameSetTag('neighbourhood watch');">neighbourhood watch,</a>
							<a href="javascript:gameSetTag('freecycle');">freecycle</a>
							<a href="javascript:gameSetTag('recycle');">recycle</a>							
						</small>
					</li>
				</ul>

				<h3>3) Try and locate the approximate area it covers (if you are unsure, click cancel)</h3>
				<div id="divMapWrapper">
		            <div id="divMapSearch">
		                <label for="txtMapSearch">Go to location</label>
		                <input type="text" class="textbox large" id="txtSearchMap" onkeypress="return submitMapSearch(event);" taborder="50"/>
		                <input id="btnMapSearch" type="button" onclick="searchMap(false);" value="Go" taborder="60"/>
		                <img id="imgMapLoading" src="{$www_server}/images/maploading.gif" width="16px" height="16px" alt="Loading ..." title="Loading ..."/>
		                <small>
		                       {l}e.g. <em>Paris, France</em> or <em>Sydney, Australia</em>{/l}
		                </small>
		            </div>
		            <div id="divMap" style="width: 590px; height: 350px">

		            </div>
		
		        </div>
				<!-- Buttons -->
				<div class="buttons">
					<small>(Windows &amp; Unix: Alt + c, Alt + s / Mac: Ctrl + c, Ctrl + s)</small>										
					<input type="button" accesskey="c" onclick="hideGameDetail();setupGame();" value="Cancel" taborder="90"/>
					<input type="button" accesskey="s" onclick="validateGame();" value="Save &amp; do another" taborder="100" id="saveGame" />
				</div>
			</div>
			
			

        </div>

{include file="../templates/footer.tpl"}
