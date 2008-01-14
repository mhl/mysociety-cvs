<?php 
/* XXX can't override the title easily, which will make us look like total
 * morons. For this page it should be, "Travel-time maps". */
include "../../wordpress/wp-blog-header.php";
include "../../wordpress/wp-content/themes/mysociety/header.php"; 
include "interactive_map.php";
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

<p>In 2006, our <a
href="http://www.mysociety.org/2007/03/05/rip-chris-lightfoot-1978-to-2007/">late
friend</a> and colleague Chris Lightfoot produced a series of time travel
contour maps, after the Department for Transport approached mySociety about
experimenting with novel ways of re-using public sector data.

<p>If you have not seen this previous work it is important that you now take a <a
href="/2006/travel-time-maps/">read through the original page</a> to see what
we are building on. 

<p>The original maps were very popular online, and the Evening Standard even
published a large article with a copy of one of the maps which covered greater
London. The Department for Transport asked us to show them how this work could
be taken further, and that is what we are showing here today.

<h2><a name="legibility"></a>Improving legibility and clarity</h2>
 
<p>Many of the maps we produced last time were very pretty, but could be somewhat
difficult to interpret. We therefore teamed up with Stamen to improve the
visual clarity and fun. Our first approach was to improve the base mapping to
something more delicate and appropriate, using OpenStreetMap. We then worked
on the colours and textures of the contours to make them quicker to interpret.
Click on the images for larger versions.

<table border="0">
<tr>

<td width="45%" valign="top">
<h3>Old map of London</h3>

<p>Showing travel times to work at the Department for Transport in Pimlico, arriving at 9am

<p><a href="oldmap.png"><img src="oldmap_small.png" alt="Old map of London showing travel times to work at the Department for Transport in Pimlico, arriving at 9am"></a>
<br><b>Click image for bigger version.</b><br><em><small>&copy; Crown copyright. All rights reserved. Department&nbsp;for&nbsp;Transport&nbsp;100020237&nbsp;2007</small></em>
</td>

<td width="10%">&nbsp;</td>

<td width="45%" valign="top">
<h3>New map of London</h3>
<p>Showing travel times to work at the Department for Transport in Pimlico, arriving at 9am

<p><a href="SW1P4DR_20km_contours_800.png"><img src="SW1P4DR_20km_contours_400.png" alt="New map of London showing travel times to work at the Department for Transport in Pimlico, arriving at 9am"></a>
<br><b>Click image for bigger version.</b>
</td>

</tr>
</table>

<h2><a name="interactive"></a>Introducing interactive maps</h2>

<p>Whilst working on improving the usability of these maps, we came to realise
that the complexity of graphical display could be substantially reduced by
replacing multiple contour lines with a single interactive slider. Have a go
here.

<p>(Remember, each of these maps are useful for only <em>one destination</em>)

<?php interactive_map("sw1p4dr-400-20km/config.xml", "mapintro", 400, 474) ?>

<h2><a name="houseprices"></a>House prices</h2>

<p>Next, it is clearly no good to be told that a location is very convenient for
your work if you can't afford to live there. So we have produced some
interactive maps that allow users to set both the maximum time they're willing
to commute, and the median houseprice they're willing or able to pay. Slide the
sliders on the following map and all will come clear.

<?php interactive_map("sw1p4dr-640-32km/config.xml", "maphouse1", 640, 731) ?>

<p><a href="morehousing.php">Click here for more such maps of London</a>, with centres at BBC Television Centre and the
Olympic Stadium Site.

<h2><a name="cartrain"></a>Car vs public transport</h2>

<p>Many people these days are looking to move to public transport, due to reasons
varying from congestion, to cost, to environmental impact. But where can you
live if you want to have the chance of getting to work speedily?   

<p>The following map shows travel times to get work in downtown Cardiff for
9am. If you move your mouse over the map, though, it will switch to show you
which areas it makes more sense to get public transport to work, and which
areas in makes more sense to drive.

<p style="text-align: center"><a href="EH12QL_driving_800.png"><img src="EH12QL_driving_400.png" alt="Getting to Edinburgh University by 09:00 - public transport vs road"></a>
<br><b>Click image for bigger version.</b>

<!-- <h3>Cardiff Central Railway Station</h3>
<p><a href="cardiff.png"><img src="cardiff_small.png" alt="Getting to Cardiff central railway station by 09:00 - public transport vs road"></a>
<h3>Birmingham University</h3>
<p><a href="birmingham.png"><img src="birmingham_small.png" alt="Getting to Birmingham University by 09:00 - public transport vs road"></a>
-->

<p>Remember, these are not general maps for the whole city, each map is only
useful for the specific target place of work or study marked with the black
dot. Please don't make a mistake and use these to pick your own place of
residence unless you happen to work at the location these maps are centred on!

<h2><a name="traincycle"></a>Public transport vs cycling</h2>

<p>For some people, the dilemma is not between the car and the train, it is
between the bicycle and everything else. This maps comprehensively shows that
if you live anywhere near the centre of this map, it's best to get on a bike if
commuting speed is your main concern.

<p style="text-align: center"><a href="SW1P4DR_20km_cycling_800.png"><img width="400" src="SW1P4DR_20km_cycling_400.png" alt=""></a>
<br><b>Click image for bigger version.</b>

<h2><a name="realtime"></a>How can I get a map?</h2>

<p>There are two ways in which you can get a travel map of this sort centred
on a location of interest to you.

<p>If you're a normal user, you can write to your local transport journey planning
organisation, for example Transport for London or San Francisco BART and
encourage them to work with us to get a system like this working interactively
on those organisation's websites.

<p>If you're a rich user, or company, you can commission us to create bespoke
maps - we're a non-profit after all and all the money will help run our other
projects. And if you're <strong>*really*</strong> rich, you can work with us to develop a
realtime service of the sort that the transport agencies should be doing.
Francis Irving from mySociety has written a <a href="realtime.php">technical
review</a> on the challenges of developing a realtime map generation system.

<h2><a name="acknowledgments"></a>Acknowledgments</h2>

<p> Please <a href="/contact">contact us</a> if you have any
questions or comments. If you're interested in this area, please also sign up
to the (fairly low-traffic) <a
href="http://secure.mysociety.org/admin/lists/mailman/listinfo/maps">mySociety
maps mailing list</a>. 

<P>The idea was pioneered by the late and sorely missed Chris Lightfoot. 
All later code developments implemented by Francis Irving. The street maps were
generated by <a href="http://www.zxv.ltd.uk/">ZXV</a> from <a href="http://www.openstreetmap.org/">OpenStreetMap</a>
data. The graphical improvements, flash and general sense of design is thanks
to Tom Carden at <a href="http://stamen.com/">Stamen</a>.  Tom Steinberg of
<a href="http://www.mysociety.org">mySociety</a> herded all the cats together.
The work was funded by the <a href="http://www.dft.gov.uk/">Department for
Transport</a>.

<h2><a name="notes"></a>Technical notes</h2>

<p>Journey times to work are for a week day in 2007. They were generated by screen
scraping the Transport for London and Transport Direct journey planner
websites. All journeys from public transport stops (in the NaPTAN database of
such stops) to the destination were calculated using the journey planner. Points
not immediately on top of a stop or station were interpolated using a walking
speed to get to the nearest public transport stop.   

<p>House prices are based on house sales recorded in the Land Registry for a large
random sample of London postcodes (cost of data &pound;2000). For each point the
median is calculated from the price of sales in a 1km radius round that point.
Sales from all of 2006 are included in calculating this median, but are house
price inflation adjusted to be the price as in December 2006.  

<p>mySociety makes open source software, so you can get the 
<a href="https://secure.mysociety.org/cvstrac/dir?d=mysociety/iso">source
code</a> for the scripts that made these maps, and we can give you copies of
the OpenStreetMap base mapping. Some other data, such as NaPTAN, will require
permission from their owners.

<?php include "../../wordpress/wp-content/themes/mysociety/footer.php"; ?>

