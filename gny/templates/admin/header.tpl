<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" 
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html lang="en" xml:lang="en"  xmlns="http://www.w3.org/1999/xhtml">
<head>

	<title>{$site_name} admin| {$page_title}</title>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
	<script type="text/javascript" src="{$admin_server}/javascript/prototype.js"></script>
    <script type="text/javascript" src="{$admin_server}/javascript/scriptaculous.js"></script>
    <script type="text/javascript" src="{$admin_server}/javascript/functions.js"></script>
    <script type="text/javascript" src="{$admin_server}/javascript/admin.js"></script>
	<link rel="stylesheet" media="all" type="text/css" href="{$admin_server}/css/memespring.css" />
	<link rel="stylesheet" media="all" type="text/css" href="{$admin_server}/css/admin.css" />	
	<link rel="Shortcut Icon" href="{$admin_server}/favicon.ico" type="image/x-icon" />
	
	{if $rss_link != ''}
	    <link rel="alternate" type="application/rss+xml" title="{$page_title}" href="{$rss_link}">
	{/if}

</head>

<body>
    <div id="divPage">
        <div id="divHeader">
            <h1>{$site_name} admin pages</h1>
            <ul id="ulMenu" class="inline">
                <li {if $menu_item =="home"}class="selected"{/if}><a href="{$admin_server}/admin/">Home</a></li>                                     
                <li {if $menu_item =="edit"}class="selected"{/if}><a href="{$admin_server}/admin/searchgroups.php">Manage groups</a></li>                
                <li {if $menu_item =="translate"}class="selected"{/if}><a href="#">Translation</a></li>
            </ul>
        </div>

        <div id="divContent">
            <div id="divWarning" class="altfont {if $hide_tracker == true} notracker {/if} {if $show_warnings == false}hide{/if}">
                {if $show_warnings == true}
    				<ul class="nobullets">
                        {foreach name="warnings" from="$warnings" item="warning"}
                            <li>{$warning}</li>
                        {/foreach}
                    </ul>
    			{/if}
            </div>
