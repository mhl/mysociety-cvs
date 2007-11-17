{include file="../templates/header.tpl"}

<h3>{l}About {$site_name}{/l}</h3>

<div class="contentleft">
    <p class="shout">
        {l}{$site_name} helps you find email lists, forums and community blogs where you live.{/l}
    </p>
    <ul class="shout">
        <li>
            {l}Discuss local issues and share information.{/l}
        </li>
        <li>
            {l}Find local issues that are important to you. Make a change with the help of others.{/l}
        </li>
        <li>
            {l}Run a local email list? Publicise your group and get new local members!{/l}
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