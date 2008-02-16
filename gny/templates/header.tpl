<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" 
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html lang="en" xml:lang="en"  xmlns="http://www.w3.org/1999/xhtml">
<head>

	<title>{$site_name} | {$page_title}</title>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    <meta name="keywords" content="GroupsNearYou, local, groups, local groups, neighbours, neighbors{if $group->tags}, {$group->tags|escape:html}{/if}" />
	<script type="text/javascript" src="{$www_server}/javascript/prototype.js"></script>
    <script type="text/javascript" src="{$www_server}/javascript/scriptaculous.js"></script>
    <script type="text/javascript" src="{$www_server}/javascript/functions.js"></script>
    <script type="text/javascript" src="{$www_server}/javascript/main.js"></script>
    {if $map_js}
        <script src="http://maps.google.com/maps?file=api&amp;v=2&amp;key={$google_maps_key}" type="text/javascript"></script>
        <script src="{$url}/javascript/map.js" type="text/javascript"></script>
    {/if}

	<link rel="stylesheet" media="all" type="text/css" href="{$www_server}/css/memespring.css" />
	<link rel="stylesheet" media="all" type="text/css" href="{$www_server}/css/main.css" />	
	<link rel="Shortcut Icon" href="{$www_server}/favicon.ico" type="image/x-icon" />
	
	{if $rss_link != ''}
	    <link rel="alternate" type="application/rss+xml" title="{$page_title}" href="{$rss_link}">
	{/if}

</head>

<body onload="javacript:{if $use_body_script == true && $onloadscript !=""}{$onloadscript}{/if};">
    <div id="divBeta">
        This site hasn't officially launched yet, we need your local knowledge to help it grow. 
        <a href="{$www_server}/add/about/">Add a group now</a>.
    </div>
    <div id="divHeader">
        <h1><a href="{$www_server}"><span class="hide">{l}GroupsNearYou.com{/l}</span></a></h1>
        <h2 class="hide">{l}Meet your neighbours{/l}</h2>
        <ul id="ulMenu" class="collapse">
            <li {if $menu_item =="about"}class="selected"{/if}><a href="{$www_server}/about/">{l}About{/l}</a></li>                                     
            <li {if $menu_item =="faq"}class="selected"{/if}><a href="{$www_server}/faq/"><acronym title="{l}Frequently asked questions{/l}">{l}FAQs{/l}</acronym></a></li>                
            <li {if $menu_item =="add"}class="selected"{/if}><a href="{$www_server}/add/about/">{l}Add a group{/l}</a></li>                        
            <li {if $menu_item =="search"}class="selected"{/if}><a href="{$www_server}">{l}Search{/l}</a></li>            
        </ul>
    </div>
    <div id="divPage">
        <div id="divContent">
            <span class="corner_tl corner">&nbsp;</span>
            <span class="corner_tr corner">&nbsp;</span>            
            <span class="corner_bl corner">&nbsp;</span>
            <span class="corner_br corner">&nbsp;</span>            
            {if $show_tracker == true}
                {* Tracker *}
                <div id="divTracker">
                   <ul id="ulTracker" class="collapse">
                   	<li{if $tracker_location == 2} class="current" {elseif $tracker_location > 2} class="complete" {/if}>
                   		{if $tracker_location >1}
                   			<a href="{$www_server}/add/about/" title="edit this section">{l}1. About the group{/l}</a>
                   		{else}
                   			{l}1. About the group{/l}
                   		{/if}
                   	</li>
                   	<li{if $tracker_location == 3} class="current" {elseif $tracker_location > 3} class="complete" {/if}>
                   		{if $tracker_location >2}
                   			<a href="{$www_server}/add/location/" title="edit this section">{l}2. Area covered{/l}</a>
                   		{else}
                   			{l}2. Area covered{/l}
                   		{/if}
                   	</li>
                   	<li{if $tracker_location == 4} class="current" {elseif $tracker_location > 4} class="complete" {/if}>
                   		{if $tracker_location >3} 
                   			    <a href="{$www_server}/add/contact/" title="edit this section">{l}3. Joining the group{/l}</a> 
                   		{else}	
                   			{l}3. Joining the group{/l}
                   		{/if}
                   	</li>
                   	<li{if $tracker_location == 5} class="current" {elseif $tracker_location > 5} class="complete" {/if}>
                   		{if $tracker_location >4} 
                   			    <a href="{$www_server}/add/preview/" title="edit this section">{l}4. Preview &amp; confirm{/l}</a> 
                   		{else}	
                   			{l}4. Preview &amp; confirm{/l}
                   		{/if}
                   	</li>
                   </ul>
                   <span class="corneralt_tl corner">&nbsp;</span>
                   <span class="corneralt_tr corner">&nbsp;</span>
               </div>
            {/if}
        
            <div id="divWarning" class="altfont {if $hide_tracker == true} notracker {/if} {if $show_warnings == false}hide{/if}">
                {if $show_warnings == true}
    				<ul class="nobullets">
                        {foreach name="warnings" from="$warnings" item="warning"}
                            <li>{$warning}</li>
                        {/foreach}
                    </ul>
    			{/if}
            </div>
