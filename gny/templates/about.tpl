{include file="../templates/header.tpl"}

<h3>{l}About {$site_name}{/l}</h3>

<div class="contentleft">
    <p class="shout">
        {l}We don't talk enough. {$site_name} helps people in your neighbourhood get to know each other!{/l}
    </p>
    <ul class="shout nobullets">
        <li>
            
        </li>
        <li>
            {l}Find email lists, forums and community blogs where you live{/l}
        </li>
        <li>
            {l}Help people find a group you know about by <a href="{$www_server}/add/about/">adding it to {$site_name} in 4 simple steps</a>{/l}
        </li>
        <li>
            {l}Get people talking about local issues that are important to them. Make a change with the help of others.{/l}
        </li>
    </ul>
</div>

<div class="contentright">
    <h4>{l}Want to know more?{/l}</h4>
    <ul class="nobullets">
        <li><a href="{$www_server}/faq/">{l}Read our FAQ's{/l}</a></li>
        <li><a href="{$www_Server}">{l}Search for a group{/l}</a></li>
        <li><a href="mailto:team@{$domain}">{l}Contact us{/l}</a></li>        
    </ul>
</div>

{include file="../templates/footer.tpl"}