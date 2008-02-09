{include file="../templates/header.tpl"}
        <div class="contentfull">
            <h3>{l}About {$site_name}{/l}</h3>            
        </div>
        <div class="contentwide">
            <p class="shout">
                {l}We don't talk enough... <em>{$site_name}</em> helps people in your neighbourhood get to know each other{/l}
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
                    {l}Get people talking about local issues that are important to them.{/l}
                </li>
            </ul>
        </div>

        <div class="contentnarrow">
            <div class="note">
                <h4>{l}Want to know more?{/l}</h4>
                <ul class="nobullets">
                    <li><a href="{$www_server}/faq/">{l}Read our FAQ's{/l}</a></li>
                    <li><a href="{$www_Server}">{l}Search for a group{/l}</a></li>
                    <li><a href="http://www.mysociety.org/faq">{l}Read about mySociety{/l}</a></li>
                    <li><a href="mailto:team@{$domain}">{l}Contact us{/l}</a></li>        
                </ul>
            </div>
        </div>

{include file="../templates/footer.tpl"}