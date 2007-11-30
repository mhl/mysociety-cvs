{include file="../templates/header.tpl"}

    <h3>{l}Frequently asked questions{/l}</h3>
    <dl class="faq">
        <dt>{l}What does {$site_name} do?{/l}</dt>
        <dd>
            {l}It lets you find out about all those hidden email lists, forums and community blogs near where you live.{/l}
        </dd>
        <dt>{l}I run a local email group, forum or blog and want to add it to {$site_name}{/l}</dt>
        <dd>{l}It's very easy. Tell us a bit about the group, the approximate area it covers and how people
            can get involved. <a href="{$www_server}/add/about/">Get started</a>.{/l}
        </dd>
        <dt>{l}How do I find a group near me?{/l}</dt>
        <dd>
            {l}Enter a place name anywhere in the world, or a UK post code or USA Zip code in the search box on <a href="{$www_server}">the front page</a>.{/l}
        </dd>
        <dt>{l}Once I find a group how to join it?{/l}</dt>
        <dd>
            {l}Click on the "join this group" link. If the group lets you join online then you'll get taken to their website.  
            If not, you can contact the group owner via this site.{/l}
        </dd>
        <dt>{l}I can't find any groups near me, but would like to start one.{/l}</dt>
        <dd>{l}There are lots of free tools on the internet to help you start an online group. 
            Companies like <a href="http://groups.yahoo.com/start">Yahoo</a> and 
            <a href="http://groups.google.com/groups/create">Google</a> 
            provide free email groups services that is simple to set up. If you need help getting other 
            local people to promise to join your group before you start it, 
            you can use <a href="http://www.pledgebank.com">PledgeBank</a>.{/l}
        </dd>
        <dt>{l}I run a local group and would like to share my experiences or get advice{/l}</dt>
        <dd>
            {l}We have setup an <a href="http://groups.google.com/group/groupsnearyou">email discussion group</a> for people
            who run local email groups or online communities.{/l}
        </dd>
        <dt>{l}If I add a group will people be able to contact me?{/l}</dt>
        <dd>{l}If you choose to be contacted people will be able to email you via this website. 
            Your email will not be published though and we will not spam you or pass it on to anyone else.
            {/l}
        </dd>
        <dt>{l}Who runs {$site_name}?{/l}</dt>
        <dd>{l}{$site_name} is run by <a href="http://www.mysociety.org">mySociety.org</a>, a charity 
            which builds useful websites which give people simple, tangible benefits in the 
            civic and community aspects of their lives. It was built by 
            <a href="http://www.memespring.co.uk">Richard Pope</a>.
            {/l}
        </dd>
        <dt>{l}There is something wrong / inappropriate about a group, how do I report it?{/l}</dt>
        <dd>
            {l}Click on the "Something wrong with this group?" link at the bottom of the group's page. This will let you 
            send us an email telling us what is up.{/l}
        </dd>        
        <dt>{l}I am a geek and want to know how this site works{/l}</dt>
        <dd>
            {l}The site is built using <a href="http://www.php.net">php</a>, <a href="http://www.smarty.net">smarty</a>,
            <a href="http://www.mysql.com/">mySql</a> and <a href="http://script.aculo.us/">Scriptaculous</a>.
            It uses the <a href="gaze.mysociety.org">mySociety GAZE web service</a> to do place name searches, and
            Emad's <a href="http://emad.fano.us/blog/?p=277">free geocoder</a>.{/l}
        </dd>
        <dt>{l}Does the site have an <acronym title="Application Programming Interface">API</acronym>?{/l}</dt>
        <dd>
            {l}Yep. Group data is available via <a href="{$www_server}/api/">geoRSS feeds</a>.{/l}
        </dd>
    </dl>

{include file="../templates/footer.tpl"}
