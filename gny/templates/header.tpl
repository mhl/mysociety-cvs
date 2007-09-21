<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" 
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html lang="en" xml:lang="en"  xmlns="http://www.w3.org/1999/xhtml">
<head>

	<title>{$site_name} | {$page_title}</title>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
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

<body>
    <div id="divPage">
        <div id="divHeader">
            <h1><a href="{$www_server}">Groups<span>NearYou</span>.com</a></h1>
            <h2>Meet your neighbours</h2>
            <ul id="ulMenu" class="collapse">
                <li {if $menu_item =="about"}class="selected"{/if}><a href="{$www_server}/about/">About</a></li>                                     
                <li {if $menu_item =="faq"}class="selected"{/if}><a href="{$www_server}/faq/"><acronym title="Frequently asked questions">FAQ</acronym>s</a></li>                
                <li {if $menu_item =="add"}class="selected"{/if}><a href="{$www_server}/add/about/">Add a group</a></li>                        
                <li {if $menu_item =="search"}class="selected"{/if}><a href="{$www_server}">Search</a></li>            
            </ul>
        </div>

        <div id="divContent">
            {if $show_tracker == true}
            
                {* Tracker *}
               <ul id="ulTracker" class="collapse">
               	<li{if $tracker_location == 2} class="current" {elseif $tracker_location > 2} class="complete" {/if}>
               		{if $tracker_location >1}
               			<a href="{$www_server}/add/about/">1. About the group</a>
               		{else}
               			1. About the group
               		{/if}
               	</li>
               	<li{if $tracker_location == 3} class="current" {elseif $tracker_location > 3} class="complete" {/if}>
               		{if $tracker_location >2}
               			<a href="{$www_server}/add/location/">2. Location</a>
               		{else}	
               			2. Location
               		{/if}
               	</li>
               	<li{if $tracker_location == 4} class="current" {elseif $tracker_location > 4} class="complete" {/if}>
               		{if $tracker_location >3} 
               			    <a href="{$www_server}/add/preview/">3. Contact details</a> 
               		{else}	
               			3. Contact details
               		{/if}
               	</li>
               	<li{if $tracker_location == 5} class="current" {elseif $tracker_location > 5} class="complete" {/if}>
               		{if $tracker_location >4} 
               			    <a href="{$www_server}/add/preview/">4. Preview</a> 
               		{else}	
               			4. Preview
               		{/if}
               	</li>
               </ul>
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