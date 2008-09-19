{include file="../templates/header.tpl"}

    <div class="contentwide">
		<h3>Add random groups</h3>
		<p class="flattop">
			There are nearly 30,000 yahoo groups containing the word 'residents' and over 15,000 with the word 'neighbo<strike>u</strike>rhood' in, but we've no idea what towns and cities they actually cover. That means loads of local knowlaged locked away where none can find it (boo). So we need your help to map them! (don't worry google, you're next).
		</p>
		<h4>How it works</h4>
		<p class="flattop">
			We show you the description of a random group, if you think looks like a local email group (a resident's association or a knitting club) you then have to guess what area you think it covers.
		</p>
		
		<h4>Get started</h4>
	    <form id="frmStartMapping" action="{$form_action}" method="post">
            {include file="../templates/formvars.tpl"}
			<ul class="form nobullets">
				<li>
					<label for="txtName">
						Name
					</label>
					<input type="text" id="txtName" name="txtName" value="{$game_name}" />
				</li>
				<li>
					<label for="txtEmail">
						Email
					</label>
					<input type="text" id="txtEmail" name="txtEmail" value="{$game_email}" />
				</li>
				<li>
					(Name and email are optional)
				</li>
				<li>
					<input type="submit" value ="Start mapping >" />
				</li>
			</ul>
		</form>

		<h4>Top mappers</h4>
		<p class="flattop">
			So for <strong>{$user_count} people</strong> have helped map <strong>{$match_count} groups</strong>. Here are the top {$site_name} mappers.
		</p>
		<table id="tblTopMappers">
			{foreach name="league_table" from="$league_table" item="league_table_item"}
				<tr {if $smarty.foreach.league_table.iteration <= 5}class="top5"{/if}>
					<td class="c1">
						{$league_table_item.name}
					</td>
					<td class="c2">
						{$league_table_item.mapped}
					</td>
				</tr>
			{/foreach}
		</table>
	</div>

    <div class="contentnarrow">
		<h3>or add one you know about</h3>
		<p class="flattop">
			If you already know of a local email group, blog or forum, you can add it directly.
		</p>
		<a class="linkbutton" href="{$www_server}/groups/{$group->url_id}/contact/">
            <span class="left">&nbsp;</span>
            <span class="middle">Add a group &raquo;</span>                
            <span class="right">&nbsp;</span>
        </a>
	</div>
{include file="../templates/footer.tpl"}