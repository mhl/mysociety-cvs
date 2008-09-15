<?php 

$body_id = 'moretravel';

# XXX This is hideous
ob_start();
include "interactive_map.php";
include "../../wp/wp-blog-header.php";
add_action('wp_head', 'add_swfobject_js');
include "../../wp/wp-content/themes/default/header.php"; 
$header = ob_get_clean();
$header = str_replace('<title>mySociety', '<title>mySociety &raquo; Travel-time maps', $header);
header('HTTP/1.0 200 OK');
print $header;
?>

<h1>More travel-time maps and their uses</h1>

<!-- <ul>
<li><a href="#background">Background</a></li>
<li><a href="#beware">Buyer beware</a></li>
<li><a href="#legibility">Improving legibility and clarity</a></li>
<li><a href="#houseprices">House prices</a> (this is the juicy one)</li>
<li><a href="#cartrain">Car vs public transport</a></li>
<li><a href="#traincycle">Public transport vs cycling</a></li>
<li><a href="#realtime">How can I get a map?</a></li>
<li><a href="#acknowledgments">Acknowledgments</a></li>
<li><a href="#notes">Technical notes</a></li>
</ul>
-->

<!--<p>(See also: <a href="methods.php">description of methods</a>;
<a href="slides.pdf">presentation slides</a>. You may also be interested in
<a href="https://secure.mysociety.org/admin/lists/mailman/listinfo/maps">the
mySociety maps mailing list</a>.)</p> -->


<div class="contenthalf">
<p> In 2006, our <a
href="http://www.mysociety.org/2007/03/05/rip-chris-lightfoot-1978-to-2007/">late
friend</a> and colleague Chris Lightfoot produced a 
<a href="/2006/travel-time-maps/">series of time travel
contour maps</a>, after the Department for Transport approached mySociety about
experimenting with novel ways of re-using public sector data.</p>

<p>This mapping work was very important because it provides a potentially
revolutionary new way of working out the best place for people to live and
work.</p>

</div>

<?php print file_get_contents($_SERVER['DOCUMENT_ROOT'] . "/../includer/maps_ad.php"); ?>

<br class="clear"/>
<p>Following widespread interest across the net and a major feature in
the Evening Standard, the Department for Transport asked us to show them how
this work could be taken further, and that is what we are showing here today.</p>


<h2><a name="legibility"></a>Improving legibility and clarity</h2>
 
<p>Many of the maps we produced last time were very pretty, but could be somewhat
difficult to interpret. We therefore teamed up with Stamen to improve the
visual clarity and fun. Our first approach was to improve the base mapping to
something more delicate and appropriate, using OpenStreetMap. We then worked
on the colours and textures of the contours to make them quicker to interpret.
Click on the images for larger versions.</p>

<table border="0">
<tr>

<td width="45%" valign="top">
<h3>Old map of London</h3>

<p>Showing travel times to work at the Department for Transport in Pimlico, arriving at 9am</p>

<p><a href="oldmap.png"><img src="oldmap_small.png" alt="Old map of London showing travel times to work at the Department for Transport in Pimlico, arriving at 9am" /></a>
<br /><b>Click image for bigger version.</b><br /><em><small>&copy; Crown copyright. All rights reserved. Department&nbsp;for&nbsp;Transport&nbsp;100020237&nbsp;2007</small></em></p>
</td>

<td width="10%">&nbsp;</td>

<td width="45%" valign="top">
<h3>New map of London</h3>
<p>Showing travel times to work at the Department for Transport in Pimlico, arriving at 9am</p>

<p><a href="SW1P4DR_20km_contours_800.png"><img src="SW1P4DR_20km_contours_400.png" alt="New map of London showing travel times to work at the Department for Transport in Pimlico, arriving at 9am" /></a>
<br /><b>Click image for bigger version.</b></p>
</td>

</tr>
</table>

<h2><a name="interactive"></a>Introducing interactive maps</h2>

<p>Whilst working on improving the usability of these maps, we came to realise
that the complexity of graphical display could be substantially reduced by
replacing multiple contour lines with a single interactive slider. Have a go
here.</p>

<p>(Remember, each of these maps are useful for only <em>one destination</em>)</p>

<?php interactive_map("sw1p4dr-400-20km/config.xml", "mapintro", 400, 474) ?>

<h2><a name="houseprices"></a>House prices</h2>

<p>Next, it is clearly no good to be told that a location is very convenient for
your work if you can&rsquo;t afford to live there. So we have produced some
interactive maps that allow users to set both the maximum time they&rsquo;re willing
to commute, and the median house price they&rsquo;re willing or able to pay. Slide the
sliders on the following map and all will come clear.</p>

<?php interactive_map("sw1p4dr-640-32km/config.xml", "maphouse1", 640, 731) ?>

<p>We have <a href="morehousing">more such maps of London</a>, with centres at BBC Television Centre and the
Olympic Stadium Site.</p>

<h2><a name="cartrain"></a>Car vs public transport</h2>

<p>Many people these days are looking to move to public transport, due to reasons
varying from congestion, to cost, to environmental impact. But where can you
live if you want to have the chance of getting to work speedily?</p>

<p>The following map shows which areas it makes more sense to get public
transport to work in Edinburgh, and which areas it makes more sense to drive.</p>

<p style="text-align: center"><a href="EH12QL_driving_800.png"><img src="EH12QL_driving_400.png" alt="Getting to Edinburgh University by 09:00 - public transport vs road" /></a>
<br /><b>Click image for bigger version.</b></p>

<!-- <h3>Cardiff Central Railway Station</h3>
<p><a href="cardiff.png"><img src="cardiff_small.png" alt="Getting to Cardiff central railway station by 09:00 - public transport vs road" /></a>
<h3>Birmingham University</h3>
<p><a href="birmingham.png"><img src="birmingham_small.png" alt="Getting to Birmingham University by 09:00 - public transport vs road" /></a>
-->

<p>Remember, these are not general maps for the whole city, each map is only
useful for the specific target place of work or study marked with the black
dot. Please don&rsquo;t make a mistake and use these to pick your own place of
residence unless you happen to work at the location these maps are centred on!</p>

<h2><a name="traincycle"></a>Public transport vs cycling</h2>

<p>For some people, the dilemma is not between the car and the train, it is
between the bicycle and public transport. This map comprehensively shows that
if you want to commute to the Department for Transport, and you live anywhere
near the centre of London, it&rsquo;s best to get on a bike if commuting speed is
your main concern.</p>

<p style="text-align: center"><a href="SW1P4DR_20km_cycling_800.png"><img width="400" src="SW1P4DR_20km_cycling_400.png" alt="" /></a>
<br /><b>Click image for bigger version.</b></p>

<h2><a name="realtime"></a>How can I get a map?</h2>

<p>There are two ways in which you can get a travel map of this sort centred
on a location of interest to you.</p>

<p>If you&rsquo;re a interested user, you can contact your local transport journey
planning organisation, for example Transport for London or San Francisco BART,
and encourage them to work with us to get a system like this working
interactively on their websites.</p>

<p>If you&rsquo;re a rich user, or company, you can commission us to create bespoke
maps &ndash; we&rsquo;re a non-profit after all and all the money will help run our other
projects. And if you&rsquo;re <strong>really</strong> rich, you can work with us to develop a
real-time service of the sort that the transport agencies should be doing.
Francis Irving from mySociety has written a <a href="realtime">technical
review</a> on the challenges of developing a real-time map generation system.</p>

<p>If you&rsquo;re interested in working with us on this, email <a
href="mailto:karl&#64;mysociety.org">karl&#64;mysociety.org</a>.</p>

<h2><a name="acknowledgments"></a>Acknowledgments</h2>

<p> Please <a href="/contact">contact us</a> if you have any
questions or comments. If you&rsquo;re interested in this area, please also sign up
to the (fairly low-traffic) <a
href="http://secure.mysociety.org/admin/lists/mailman/listinfo/maps">mySociety
maps mailing list</a>. </p>

<p>The idea was pioneered by the late and sorely missed <a href="http://www.ex-parrot.com/~chris/wwwitter/">Chris Lightfoot</a>. 
All later code developments implemented by <a href="http://www.flourish.org/">Francis Irving</a>. The street maps were
generated by <a href="http://www.zxv.ltd.uk/">ZXV</a> and Artem Pavlenko from <a href="http://www.openstreetmap.org/">OpenStreetMap</a>
data using <a href="http://mapnik.org/">Mapnik</a>. The map graphical improvements, Flash and general sense of design is thanks
to Tom Carden at <a href="http://stamen.com/">Stamen</a>;
<a href="http://www.dracos.co.uk/">Matthew</a> ran around tidying, spell-checking, validating, and outdenting.
Tom Steinberg of <a href="http://www.mysociety.org/">mySociety</a> herded all the cats together.
The work was funded by the <a href="http://www.dft.gov.uk/">Department for
Transport</a>.</p>

<h2><a name="crosssell"></a>If you liked this...</h2>

<p>mySociety, who produced this report, is a non-profit. We build websites
that give people simple, tangible benefits in the civic and community aspects
of their lives. Try some of them out!</p>

<ul>
<li><strong>Graffiti, fly tipping, broken paving slabs or street lighting?</strong>
Get them fixed on <a href="http://www.fixmystreet.com/">FixMyStreet</a>.</li>

<li>Want to know what <strong>your MP is doing in your name</strong>? 
Find out on <a href="http://www.theyworkforyou.com">TheyWorkForYou</a>.</li>

<li><strong>Change the world</strong> by saying "I&rsquo;ll do it <strong>but only if</strong> you will too". 
Make a pledge on <a href="http://www.pledgebank.com">PledgeBank</a>.</li>

</ul>

<h2><a name="notes"></a>Technical notes</h2>

<p>Journey times to work are for a week day in 2007. They were generated by screen
scraping the Transport for London and Transport Direct journey planner
websites. All journeys from public transport stops (in the NaPTAN database of
such stops) to the destination were calculated using the journey planner. Points
not immediately on top of a stop or station were interpolated using a walking
speed to get to the nearest public transport stop.</p>

<p>House prices are based on house sales recorded in the Land Registry for a
large random sample of London postcodes. For each point the median is
calculated from the price of sales in a 1km radius round that point.  Sales
from all of 2006 are included in calculating this median, but are house price
inflation adjusted to be the price as in December 2006.</p>

<p>mySociety makes open source software, so you can get the 
<a href="https://secure.mysociety.org/cvstrac/dir?d=mysociety/iso">source
code</a> for the scripts that made these maps, and we can give you copies of
the OpenStreetMap base mapping. Some other data, such as NaPTAN, will require
permission from their owners.</p>

<?php include "../../wp/wp-content/themes/default/footer.php"; ?>

