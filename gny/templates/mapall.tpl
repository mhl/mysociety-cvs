<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">

<html lang="en">
<head>
	<title>{$page_title} | {$site_name}</title>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    <meta name="keywords" content="GroupsNearYou, local, groups, local groups, neighbours, neighbors{if $group->tags}, {$group->tags|escape:html}{/if}" />
	<script type="text/javascript" src="{$www_server}/javascript/prototype.js"></script>
    <script type="text/javascript" src="{$www_server}/javascript/scriptaculous.js"></script>
    <script type="text/javascript" src="{$www_server}/javascript/functions.js"></script>
    <script type="text/javascript" src="{$www_server}/javascript/main.js"></script>

        <script src="http://maps.google.com/maps?file=api&amp;v=2&amp;key={$google_maps_key}" type="text/javascript"></script>
        <script src="{$url}/javascript/map.js" type="text/javascript"></script>

	<link rel="stylesheet" media="all" type="text/css" href="{$www_server}/css/memespring.css" />
	<link rel="stylesheet" media="all" type="text/css" href="{$www_server}/css/main.css" />	
	<link rel="Shortcut Icon" href="{$www_server}/favicon.ico" type="image/x-icon" />


</head>
<body>


    <div id="divMap" style="width:900px; height:900px"></div>

    <script>
    
        //make map
        map = new GMap2(document.getElementById("divMap"));
        map.setCenter(new GLatLng(52, 0), 6);
      
        //add groups
        {foreach name="groups" from="$groups" item="group"}
            rectBounds = new GLatLngBounds(
                new GLatLng({$group->lat_bottom_left}, {$group->long_bottom_left}),
                new GLatLng({$group->lat_top_right}, {$group->long_top_right}));


        	//add the new one						
            map.addOverlay(new Rectangle(rectBounds, 2, '#280FFF', 0.5));

        {/foreach}
        
    </script>

</body>
</html>
