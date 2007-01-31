<?php 
/* XXX can't override the title easily, which will make us look like total
 * morons. For this page it should be, "Travel-time maps". */
include "../../wordpress/wp-blog-header.php";
include "../../wordpress/wp-content/themes/mysociety/header.php"; 
?>

<h1>More travel-time Maps and their Uses</h1>

<p>Chris Lightfoot, mySociety &lt;<a href="mailto:chris@mysociety.org">chris@mysociety.org</a>&gt;<br>
Francis Irving, mySociety &lt;<a href="mailto:francis@mysociety.org">francis@mysociety.org</a>&gt;<br>
Tom Steinberg, mySociety &lt;<a href="mailto:tom@mysociety.org">tom@mysociety.org</a>&gt;<br>
</p>

<p>This work was funded and supported by the <a href="http://www.dft.gov.uk/">Department&nbsp;for&nbsp;Transport</a>.</p>

<ul>
<li><a href="#background">Background</a></li>
<li><a href="#legibilirty">Improving legibility</a></li>
<li><a href="#houseprices">House prices</a></li>
<li><a href="#cartrain">Car vs. public transport</a></li>
<li><a href="#traincycle">Public transport vs. cycling</a></li>
<li><a href="#realtime">Real time maps</a></li>
<li><a href="#acknowledgments">Acknowledgments</a></li>
<li><a href="#data">The data we used</a></li>
</ul>

<!--<p>(See also: <a href="methods.php">description of methods</a>;
<a href="slides.pdf">presentation slides</a>. You may also be interested in
<a href="https://secure.mysociety.org/admin/lists/mailman/listinfo/maps">the
mySociety maps mailing list</a>.)</p> -->

<h2><a name="background"></a>Background</h2>

<p>So, the <a href="/2006/travel-time-maps/">first travel time maps</a>,
built by Chris Lightfoot for mySociety, went down rather well. As well as
briefly making it into the top three most popular new pages for a while on
Del.icio.us, the Evening Standard had a 3/4 page splash of the map of London. 
<p>The Department for Transport then chose to commission us to look into
various further avenues of this work. This page, launched on 1st Feb 2007 is
the primary output of that work. We hope you find it useful as well as
enjoyable.  

<h2><a name="legibility"></a>Improving legibility</h2>

<p>Many of the maps we produced last time were very pretty, but could be
somewhat difficult to interpret. One major task was to read up on how to
display such complex and valuable data in more intellible ways, and the results
can be seen below. 

<p>Old map of London

<p><a href="/2006/travel-time-maps/multimodal-london-20km-1196px.png"><img src="/2006/travel-time-maps/multimodal-london-20km-1196px.png" width="598" height="569" alt="Old map of London from SW1"></a>

<p>New map of London from SW1 

<p>That second map shows travel times to a centre point at the Department for
Transport headquarters.  Here's a map using a very different part of London as
its centre, a hospital in the less well connected Denmark Hill.

<p><a href="southlondon.png"><img src="southlondon_small.png" alt="Travel times to Maudsley Hospital in Denmark Hill SE5"></a>
<br><small>&copy; Crown copyright. All rights reserved. Department&nbsp;for&nbsp;Transport&nbsp;100020237&nbsp;2007</small>

<p>Discrete vs. continuous contours. Better mapping backgrounds.

<p>Travelling to work by 9am

<h2><a name="houseprices"></a>House prices</h2>

<p>Next, it is clearly no good to be told that a location is very convenient
for your work if you can't afford to live there. So we have produced travel
maps that show not just where someone working can live if they want to get to
work swiftly, we can also show what areas they can afford to live in. 

<p>Here is a map which is also centered on the hospital in denmark hill, but
only showing travel times to locations where the average median houseprice is
below 200,000k 

<p>If you're a bit wealthier, you might be interested in a map of London
centered on the same place, but focussing only on houses from 200-300k

<p><!--<a href="rail-cambridge-1500px.png"><img src="rail-cambridge-500px.png" width="288" height="500" alt="Map showing travel times by rail and taxi from Cambridge to other points in Great Britain, starting at 7 o'clock on a weekday morning"></a>
<br><small>&copy; Crown copyright. All rights reserved. Department&nbsp;for&nbsp;Transport&nbsp;100020237&nbsp;2006</small>-->
</p>

<h2><a name="cartrain"></a>Car vs. public transport</h2>

<p>Many people these days are looking to move to public transport, due to
reasons varying from congestion, to cost, to environmental impact. But where
can you live if you want to have the chance of getting to work speedily? 

<p>The following maps show the places you can live in Edinburgh, Cardiff and
Birmingham if you want to be on optimal commuting routes for the centres
indicated with the black dots. Click on the maps for larger versions.

<h3>Edinburgh University</h3>
<p><a href="ed.png"><img src="ed_small.png" alt="Getting to Edinburgh University by 09:00 - public transport vs road"></a>
<br><small>&copy; Crown copyright. All rights reserved. Department&nbsp;for&nbsp;Transport&nbsp;100020237&nbsp;2007</small>
<h3>Cardiff Central Railway Station</h3>
<p><a href="cardiff.png"><img src="cardiff_small.png" alt="Getting to Cardiff central railway station by 09:00 - public transport vs road"></a>
<br><small>&copy; Crown copyright. All rights reserved. Department&nbsp;for&nbsp;Transport&nbsp;100020237&nbsp;2007</small>
<h3>Birmingham University</h3>
<p><a href="birmingham.png"><img src="birmingham_small.png" alt="Getting to Birmingham University by 09:00 - public transport vs road"></a>
<br><small>&copy; Crown copyright. All rights reserved. Department&nbsp;for&nbsp;Transport&nbsp;100020237&nbsp;2007</small>

<p>Remember, these are not general maps for the whole city, each map is only
useful for the specific target place of work or study marked with the black
dot. Please don't make a mistake and use these to pick your own place of
residence unless you happen to work at the location these maps are centered on!

<h2><a name="traincycle"></a>Public transport vs. cycling</h2>

<p>For some people, the dilemma is not between the car and the train, it is
between the bicycle and everything else. This maps comprehensively shows that
if you live anywhere near the centre of this map, it's best to get on a bike if
commuting speed is your main concern.

<p><a href="cycling-vs-public-transport.png"><img width="450" src="cycling-vs-public-transport.png" alt="Getting to Birmingham University by 09:00 - public transport vs road"></a>
<br><small>&copy; Crown copyright. All rights reserved. Department&nbsp;for&nbsp;Transport&nbsp;100020237&nbsp;2007</small>

<h2><a name="realtime"></a>What next? Further work</h2>

<p>Two places of work (for couples)
<p>Where should I look for work that I can get to easily?
<p>Travel time to nearest hospital

<h2><a name="acknowledgments"></a>Acknowledgments</h2>

<p>Please contact us (email addresses at the top of the page) if you have
any questions or comments. If you're interested in this area, please also
sign up to the (fairly low-traffic)
<a href="http://secure.mysociety.org/admin/lists/mailman/listinfo/maps">mySociety maps
mailing list</a>.</p>

<p>This work was funded by the
<a href="http://www.dft.gov.uk/">Department&nbsp;for&nbsp;Transport</a>, who
also made it possible for us to use
<a href="http://www.ordsvy.co.uk/">Ordnance Survey</a> maps and data through
their licence; without this assistance we would have had to pay expensive fees
to use the underlying mapping data or to produce maps with no landmarks, which
would be almost incomprehensible. DfT also gave us access to their
<a href="http://www.naptan.org.uk/">National Public Transport Access Node</a>
database, which records the locations of train and tube stations and bus stops; without this it would have been difficult to produce any maps at all.</p>

<h2><a name="data"></a>The data we used</h2>

<p>Although the journey planning services and software we used were publicly
accessibly, almost none of the other data is available unless you pay for it,
or your work falls under an existing licencing agreement. So while we set out
to demonstrate how easily we could make travel-time maps from public data, very
little of this work could be cheaply reproduced or extended without assistance
from a government department.</p>

<p>That's unfortunate, because it means that innovative work by outsiders in
this area can only go ahead if it's explicitly sponsored by government. If all
the data we've used had been available for free, somebody else might well have
done what we've done years ago, with no cost to the taxpayer. We'd love it if
others extend the work that we've done, but realistically there aren't very
many people in a position to do this cheaply.</p>

<?php include "../../wordpress/wp-content/themes/mysociety/footer.php"; ?>
