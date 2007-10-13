{include file="../templates/header.tpl"}

    <h3>Frequently asked questions</h3>
    <dl class="faq">
        <dt>What does GroupsNearMe.com do?</dt>
        <dd>
            If lets you find out about all those hidden email lists, forums and community blogs near where you live.
        </dd>
        <dt>I am run a local email group, forum or blog and want to add it to GroupdsNearMe.com</dt>
        <dd>
            It's very easy. Tell us a bit about the group, the approximate area it covers and how people
            can get involved. <a href="{$www_server}/add/about/">Click here to get started</a>.
        </dd>
        <dt>How do I find a group near me?</dt>
        <dd>
            Enter a place name anywhere in the world, or a UK post code or USA Zip code in the search box on <a href="{$www_server}">this page</a>.
        </dd>
        <dt>Once I find a group how to join it?</dt>
        <dd>
            Click on the "join this group" link. If the group lets you join online then you'll get taken to their website.  
            If not, you can contact the group owner via this site.
        </dd>
        <dt>I can find any groups near me, but would like to start one.</dt>
        <dd>
            There are lots of free tools on the internet to help you start an online group. 
            Companies like <a href="http://groups.yahoo.com/start">Yahoo</a> and 
            <a href="http://groups.google.com/groups/create">Google</a> 
            provide free email groups services that is simple to set up. If you need help getting other 
            local people to promise to join your group before you start it, 
            you can use <a href="http://www.pledgebank.com">PledgeBank.com</a>.
        </dd>
        <dt>I run a local group and would like to share my experiences or get advice</dt>
        <dd>
            We have setup an <a href="http://groups.google.com/group/groupsnearyou">email discussion group</a> for people
            who run local email groups or online communities.
        </dd>
        <dt>If I add a group will people be able to contact me?</dt>
        <dd>
            If you choose to be contacted people will be able to email you via this website. 
            Your email will not be published though and we will not spam you or pass it on to anyone else.
        </dd>
        <dt>Who runs {$site_name}?</dt>
        <dd>
            {$site_name} is run by <a href="http://www.mysociety.org">mySociety.org</a>, a charity 
            which builds useful websites which give people simple, tangible benefits in the 
            civic and community aspects of their lives. It was built by 
            <a href="http://www.memespring.co.uk">Richard Pope</a>.
        </dd>
        <dt>I am a geek and want to know how this site works</dt>
        <dd>
            The site is built using <a href="http://www.php.net">php</a>, <a href="http://www.smarty.net">smarty</a>,
            <a href="http://www.mysql.com/">mySql</a> and <a href="http://script.aculo.us/">Scriptaculous</a>.
            It uses the <a href="gaze.mysociety.org">mySociety GAZE web service</a> to do place name searches, and
            Emad's <a href="http://emad.fano.us/blog/?p=277">free geocoder</a>.
        </dd>
        <dt>Does the site have an <acronym title="Application Programming Interface">API</acronym>?</dt>
        <dd>
            Yep. Group data is available via <a href="{$www_server}/api/">geoRSS feeds</a>.
        </dd>
    </dl>

{include file="../templates/footer.tpl"}