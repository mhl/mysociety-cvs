<?php 
/* XXX can't override the title easily, which will make us look like total
 * morons. For this page it should be, "Travel-time maps". */
include "../../wordpress/wp-blog-header.php";
include "../../wordpress/wp-content/themes/mysociety/header.php"; 
?>

<h1>More travel-time maps and their uses</h1>

<p>
Richard Pope, mySociety &lt;<a href="mailto:richard@mysociety.org">richard@mysociety.org</a>&gt;<br>
Chris Lightfoot, mySociety &lt;<a href="mailto:chris@mysociety.org">chris@mysociety.org</a>&gt;<br>
Francis Irving, mySociety &lt;<a href="mailto:francis@mysociety.org">francis@mysociety.org</a>&gt;<br>
Tom Steinberg, mySociety &lt;<a href="mailto:tom@mysociety.org">tom@mysociety.org</a>&gt;<br>
</p>

<p>This work was funded and supported by the <a href="http://www.dft.gov.uk/">Department&nbsp;for&nbsp;Transport</a>.</p>

<ul>
<li><a href="#background">Background</a></li>
<li><a href="#beware">Buyer beware</a></li>
<li><a href="#legibility">Improving legibility and clarity</a></li>
<li><a href="#houseprices">House prices</a></li>
<li><a href="#cartrain">Car vs. public transport</a></li>
<li><a href="#traincycle">Public transport vs. cycling</a></li>
<li><a href="#acknowledgments">Acknowledgments</a></li>
<li><a href="#data">The data we used</a></li>
</ul>

<!--<p>(See also: <a href="methods.php">description of methods</a>;
<a href="slides.pdf">presentation slides</a>. You may also be interested in
<a href="https://secure.mysociety.org/admin/lists/mailman/listinfo/maps">the
mySociety maps mailing list</a>.)</p> -->

<h2><a name="background"></a>Background</h2>

<p>In 2006 Chris Lightfoot produced a series of time travel contour maps, after
the Department for Transport approached mySociety about experimenting with
novel ways of re-using public sector data. 

<p>If you have not seen this previous work it is important that you now take a <a
href="/2006/travel-time-maps/">read through the original page</a> to see what
we are building on. 

<p>The original maps were very popular online, and the Evening Standard even
published a large article with a copy of one of the maps which covered greater
London. 

<p>The Department for Transport asked us to show them how this work could be taken
further, and that is what we are showing here today.

<h2><a name="beware"></a>Buyer beware</h2>

<p>Remember, each of these maps are useful for only <em>one destination</em>.
They are proof of concept for a system or systems that could deliver custom
maps for each user. They should not be taken as a basis for making important
decisions on where to live or work in their current form.

<h2><a name="legibility"></a>Improving legibility and clarity</h2>
 
<p>Many of the maps we produced last time were very pretty, but could be somewhat
difficult to interpret. One major task was to read up on how to display such
complex and valuable data in more intellible ways, and the results can be seen
below.

<h3>Old map of London</h3>

<p>Showing travel times to work at the Department for Transport in Pimlico, arriving at 9AM

<p><a href="oldmap.png"><img src="oldmap_small.png" alt="Old map of London showing travel times to work at the Department for Transport in Pimlico, arriving at 9AM"></a>
<br><em>Click image for bigger version.</em><br><small>&copy; Crown copyright. All rights reserved. Department&nbsp;for&nbsp;Transport&nbsp;100020237&nbsp;2007</small>

<h3>New map of London</h3>
<p>Showing travel times to work at the Maudsley Hospital, Denmark Hill also arriving at 9AM

<p><a href="southlondon.png"><img src="southlondon_small.png" alt="New map of London showing travel times to work at the Maudsley Hospital, Denmark Hill also arriving at 9AM"></a>
<br><em>Click image for bigger version.</em><br><small>&copy; Crown copyright. All rights reserved. Department&nbsp;for&nbsp;Transport&nbsp;100020237&nbsp;2007</small>

<h2><a name="houseprices"></a>House prices</h2>

<p>Next, it is clearly no good to be told that a location is very convenient for
your work if you can't afford to live there. So we have produced travel maps
that show not just where someone working can live if they want to get to work
swiftly, we can also show what areas they can afford to live in. 

<p>The next three maps show different bands of house prices PLUS time travel
contours to the DfT building. However, in areas which are outside the desired
price band, the contours are greyed out. Let's start at the bottom of the
London market, less than &pound;200,000 median price.

<p><a href="house-200.png"><img src="house-200_small.png" alt="Travel times to the Department for Transport and house prices less than &pound;200,000"></a>
<br><em>Click image for bigger version.</em><br><small>&copy; Crown copyright. All rights reserved. Department&nbsp;for&nbsp;Transport&nbsp;100020237&nbsp;2007</small>

<p>Oh dear! It seems there's almost nowhere for under &pound;200,000 median
anywhere within 40 minutes of our target. Let's up the price band.

<p><a href="house-300.png"><img src="house-300_small.png" alt="Travel times to the Department for Transport and house prices less than &pound;300,000"></a>
<br><em>Click image for bigger version.</em><br><small>&copy; Crown copyright. All rights reserved. Department&nbsp;for&nbsp;Transport&nbsp;100020237&nbsp;3007</small>

<p>Now much more is clearly available, although most of it 30-40 minutes away.
But what if I want to exclude both prices that are too high and too low?  This
map shows only areas where the median price is between &pound;300,000 and &pound;400,000.

<p><a href="house-300-400.png"><img src="house-300-400_small.png" alt="Travel times to the Department for Transport and median house prices between &pound;300,000 and &pound;400,000"></a>
<br><em>Click image for bigger version.</em><br><small>&copy; Crown copyright. All rights reserved. Department&nbsp;for&nbsp;Transport&nbsp;100020237&nbsp;300-4007</small>

<h2><a name="cartrain"></a>Car vs. public transport</h2>

<p>Many people these days are looking to move to public transport, due to
reasons varying from congestion, to cost, to environmental impact. But where
can you live if you want to have the chance of getting to work speedily? 

<p>The following maps show the areas around three cities where getting to work
(shown by the black dot) is faster by car, and where getting to work by public
transport is better. Such maps would enable people to choose suitable areas
according to their needs and preferences around transport.

<h3>Edinburgh University</h3>
<p><a href="ed.png"><img src="ed_small.png" alt="Getting to Edinburgh University by 09:00 - public transport vs road"></a>
<br><em>Click image for bigger version.</em><br><small>&copy; Crown copyright. All rights reserved. Department&nbsp;for&nbsp;Transport&nbsp;100020237&nbsp;2007</small>
<h3>Cardiff Central Railway Station</h3>
<p><a href="cardiff.png"><img src="cardiff_small.png" alt="Getting to Cardiff central railway station by 09:00 - public transport vs road"></a>
<br><em>Click image for bigger version.</em><br><small>&copy; Crown copyright. All rights reserved. Department&nbsp;for&nbsp;Transport&nbsp;100020237&nbsp;2007</small>
<h3>Birmingham University</h3>
<p><a href="birmingham.png"><img src="birmingham_small.png" alt="Getting to Birmingham University by 09:00 - public transport vs road"></a>
<br><em>Click image for bigger version.</em><br><small>&copy; Crown copyright. All rights reserved. Department&nbsp;for&nbsp;Transport&nbsp;100020237&nbsp;2007</small>

<p>Remember, these are not general maps for the whole city, each map is only
useful for the specific target place of work or study marked with the black
dot. Please don't make a mistake and use these to pick your own place of
residence unless you happen to work at the location these maps are centered on!

<h2><a name="traincycle"></a>Public transport vs. cycling</h2>

<p>For some people, the dilemma is not between the car and the train, it is
between the bicycle and everything else. This maps comprehensively shows that
if you live anywhere near the centre of this map, it's best to get on a bike if
commuting speed is your main concern.

<p><a href="cycling.png"><img width="400" src="cycling_small.png" alt=""></a>
<br><em>Click image for bigger version.</em><br><small>&copy; Crown copyright. All rights reserved. Department&nbsp;for&nbsp;Transport&nbsp;100020237&nbsp;2007</small>

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
