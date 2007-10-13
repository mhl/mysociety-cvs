{* basic  microformats hcard *}
<!--Microformats hCard-->
<div id="hcard-{$group->url_id}" class="vcard hide">
     
     {if $group->involved_type == 'email'}
         <div class="org">{$group->name}</div>
         <a class="email" href="{$www_server}/groups/{$group->url_id}/contact/">email (via web)</a>
     {else}
      <a class="url fn org" href="{$group->involved_link}">{$group->name}</a>
     {/if}
     
     <span class="note">{$group->description}</span> 

     <abbr class="geo" title="{$group->lat_centroid};{$group->long_centroid}">Centroid of the area covered by {$group->name}</abbr>
</div>
