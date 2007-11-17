{include file="../templates/header.tpl"}

<h3>{l}{$site_name} feeds / <acronym title="Application Programming Interface">API</acronym>{/l}</h3>

<p>
    {l}{$site_name} data is available programmatically as <a href="http://georss.org/">GeoRSS</a>
        feeds. These can be used in most web mapping APIs and desktop <acronym title="Geographic Information System">GIS</acronym> software like 
        <a href="http://mapufacture.com">mapufacture</a>, 
        <a href="http://maps.google.com">Google Maps</a>, <a href="http://developer.yahoo.com/maps/georss/index.html">Yahoo maps</a> 
        and <a href="http://pipes.yahoo.com/">Yahoo Pipes</a>. 
        Details of the API are listed below.
        We will add more feeds in the near future. Please <a href="{$www_server}/about/#contact">
            get in touch</a> if you want anything specific that isn't listed here.</span>{/l}
<p/>

<!--Single-->
<div class="apiitem">
	<h5>{l}Groups by location (bounding boxes){/l}</h5>
	<p class="apidefinition">
	{l}Returns bounding boxes of groups near a given location. Location can be defined by 
	   <a href="http://en.wikipedia.org/wiki/UK_postcodes"><acronym title="United Kingdom">UK</acronym> postcode</a>,
	   <a href="http://en.wikipedia.org/wiki/ZIP_Code"><acronym title="United States of America">USA ZIP code</a> </a>
	   or longitude / latitude.{/l}
	</p>
	<code>
	{$www_server}/rss.php?<strong>q</strong>=[postcode | zipcode | longitude,latitude]
	</code>
	<p class="apiexamples">
	    <a href="{$www_server}/rss.php?q=n19ap ">{l}view example{/l}</a>
	    {assign var="url" value="/rss.php?q=n19ap"}
	    <a href="http://maps.google.com/maps?f=q&hl=en&q={$www_server}{$url|escape:url}&layer=&ie=UTF8&z=15&om=1">{l}view on a map{/l}</a>
    </p>
</div>


<h4 id="hLicenseInfo">{l}License information{/l}</h4>
<p>
    {l}Data via the {$site_name} <acronym title="Application Programming Interface">api</acronym> 
        feeds is licensed under the <a href="http://creativecommons.org/licenses/by-sa/3.0/">
        Creative Commons Attribution-ShareAlike 3.0 license</a>.{/l}
</p>

{include file="../templates/footer.tpl"}