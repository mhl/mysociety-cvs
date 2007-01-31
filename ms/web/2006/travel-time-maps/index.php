<?php 
/* XXX can't override the title easily, which will make us look like total
 * morons. For this page it should be, "Travel-time maps". */
include "../../wordpress/wp-blog-header.php";
include "../../wordpress/wp-content/themes/mysociety/header.php"; 
?>

<h1>Travel-time Maps and their Uses</h1>

<p>Chris Lightfoot, mySociety &lt;<a href="mailto:chris@mysociety.org">chris@mysociety.org</a>&gt;<br>
Tom Steinberg, mySociety &lt;<a href="mailto:tom@mysociety.org">tom@mysociety.org</a>&gt;<br>
</p>

<p>This work was funded and supported by the <a href="http://www.dft.gov.uk/">Department&nbsp;for&nbsp;Transport</a>.</p>

<ul>
<li><a href="#introduction">Introduction</a></li>
<li><a href="#examples">Examples</a>
    <ul>
    <li><a href="#nationalrail">Rail travel in Great Britain</a></li>
    <li><a href="#cambridgeshire">Bus and rail travel in Cambridge and surrounds</a></li>
    <li><a href="#london">London</a></li>
    </ul>
</li>
<li><a href="#furtherwork">What next? Further work</a></li>
<li><a href="#acknowledgments">Acknowledgments</a></li>
<li><a href="#data">The data we used</a></li>
</ul>

<p>(See also: <a href="methods.php">description of methods</a>;
<a href="slides.pdf">presentation slides</a>. You may also be interested in
<a href="https://secure.mysociety.org/admin/lists/mailman/listinfo/maps">the
mySociety maps mailing list</a>.)</p>

<h2><a name="introduction"></a>Introduction</h2>

<p>Transport maps and timetables help people work out how to get from A to B
using buses, trains and other forms of public transport. But what if you don't
yet know what journey you want to make? How can maps help then?</p>

<p>This may seem a strange question to ask, but it is one we all face in
several situations:</p>

<ul>
<li>Where would I like to work?</li>
<li>Where would I like to live?</li>
<li>Where would I like to go on holiday?</li>
</ul>

<p>These are much more complicated questions than those about individual
journeys, but one thing they all have in common is transport: can I get to and
from the places I'm considering quickly and easily?</p>

<p>The maps on this page show one way of answering that question. Using colours
and contour lines they show how long it takes to travel between one particular
place and every other place in the area, using public transport. They also show
the areas from which no such journey is possible, because the services are not
good enough.</p>

<h2><a name="examples"></a>Examples</h2>

<h3><a name="nationalrail"></a>Rail travel in Great Britain</h3>

<p>Our first example is about rail travel. The map below shows how long it
takes to get from Cambridge Station to every other station in the UK, starting
at seven o'clock on a weekday morning. This could be useful if you lived in
Cambridge, and were wondering where you might go for a long weekend away and
didn't want to travel more than 4 hours. We assume that people will take a taxi
from a convenient train station to their destination, so long as that journey
is no more than an hour. (Please see our <a href="methods.php">methods
page</a> for a more detailed description of our assumptions.) You can click on
any of the maps on this page to see a larger version.</p>

<p><a href="rail-cambridge-1500px.png"><img src="rail-cambridge-500px.png" width="288" height="500" alt="Map showing travel times by rail and taxi from Cambridge to other points in Great Britain, starting at 7 o'clock on a weekday morning"></a>
<br><small>&copy; Crown copyright. All rights reserved. Department&nbsp;for&nbsp;Transport&nbsp;100020237&nbsp;2006</small>
</p>

<p>The white contour lines are drawn at one-hour intervals, so the innermost,
almost circular contour shows destinations up to an hour from Cambridge, the
concentric one two hours, and so forth. (Technically, the contours are
"isochrones", meaning lines of constant time, as for "isobars" for lines of
constant atmospheric pressure on a weather map.) Places, such as Leeds,
which are surrounded by little circular contours are more-accessible "islands"
served by fast trains with infrequent stops; they are therefore quicker to
reach than those in the surrounding areas which require lengthy changes or
journeys on slower services.</p>

<p>The colour scale, shown on the top right of the map, is in hours of total
travel time. Warm colours indicate short travel time&mdash;red for four hours
or less, orange and yellow for four to eight hours&mdash;and cool colours
longer journeys. The longest journey times of all, to destinations in the far
north and west of Scotland, are over nineteen hours (remember that this
includes waiting time, which could often be overnight). Areas with no colour at
all, such as the area around Hawich on the Scottish Borders or the north-west
coast of Scotland, cannot be reached at all by rail and a taxi journey of up to
one hour.</p>

<p>The map shows that the fastest journeys are those along the
<a href="http://en.wikipedia.org/East_Coast_Main_Line">East Coast Main Line</a>
north to Edinburgh, and those south to London, which is served by frequent fast
trains. Everywhere in England can be reached within about seven hours (so by
two o'clock in this example), and everywhere in Wales within about ten hours,
though many of the fastest journeys to rural areas of mid-Wales will involve a
long taxi journey. The urban areas of lowland Scotland are similarly
well-connected, but areas further north are much less accessible, or even
inaccessible where there are no stations within an hour's drive of a given
destination.</p>

<h4>Edinburgh</h4>

<p>The next map is for journeys starting from Edinburgh Waverley station, but
otherwise it is the same as the Cambridge map.</p>

<p>
<a href="rail-edinburgh-1500px.png"><img src="rail-edinburgh-500px.png" width="288" height="500" alt="Map showing travel times by rail and taxi from Edinburgh to other points in Great Britain, starting at 7 o'clock on a weekday morning"></a>
<br><small>&copy; Crown copyright. All rights reserved. Department&nbsp;for&nbsp;Transport&nbsp;100020237&nbsp;2006</small>
</p>

<p>Here the East Coast Main Line is even more obvious than in the preceding
map; it appears as a tendril of red and pink stretching south from Edinburgh
down to London.</p>

<h4>Comparing car and train travel</h4>

<p>Again considering journeys starting from Cambridge, this map shows which
parts of the country are quicker to get to by train (red and orange), and which
by car (green and blue). Yellow and light orange show areas where there's no
great difference. This could be useful if you had limited access to a car and
were planning where to go, or wanted to see whether it was worth hiring a car
for a particular trip.</p>

<p>
<a href="rail-differences-cambridge-1500px.png"><img src="rail-differences-cambridge-500px.png" width="288" height="500" alt="Map showing the difference in journey times by rail and taxi, and by road alone, from Cambridge to other points in Great Britain, starting at 7 o'clock on a weekday morning"></a>
<br><small>&copy; Crown copyright. All rights reserved. Department&nbsp;for&nbsp;Transport&nbsp;100020237&nbsp;2006</small>
</p>

<p>This time, contours are drawn for each hour of <em>difference</em> in travel
time. Note also  that the scale is quite asymmetric: the most time you can save
travelling by train is about two hours, but&mdash;for places which are
difficult to reach by train&mdash;you can save six or seven hours travelling by
road.</p>

<p>From this map, journeys to London are quicker by train (the road travel
model takes no account of traffic or urban areas, so it is pessimistic about
the time saving) as are journeys to Leeds, Berwick, Edinburgh, Glasgow and
other points served by trains on the East Coast Main Line. In the west of
England, journeys to Exeter and thereabouts are quicker by rail, but all other
journeys are quicker by road (largely because most westward journeys require a
change at London or a slow cross-country train to Birmingham).</p>

<p>(However, the model of car journey times is very simplistic, so <em>these
results should not be taken too seriously</em>&mdash;we hope to extend the work
with a more realistic model of driving times, which may substantially change
the comparative results.)</p>

<h3><a name="cambridgeshire"></a>Bus and rail travel in Cambridge and surrounds</h3>

<p>Our second example is based on public transport in and around Cambridge,
which chiefly means buses within town and from outlying villages into the city
center. Here we ask how early must you get up and leave your home to reach a
particular place of work by public transport. In this example the destination
we've selected is the University of Cambridge's
<a href="http://www-building.arct.cam.ac.uk/westc/index.html">West Cambridge
Site</a>, which is also home to a number of commercial employers including
<a href="http://www.research.microsoft.com/labs/cam.asp">Microsoft</a>.</p>

<p>
<a href="multimodal-cambridge-center-700px.png"><img src="multimodal-cambridge-center-350px.png" width="350" height="300" alt="Map of Cambridge showing times of departure to reach the West Cambridge site by 9 o'clock on a weekday morning"></a>
<br><small>&copy; Crown copyright. All rights reserved. Department&nbsp;for&nbsp;Transport&nbsp;100020237&nbsp;2006</small>
</p>

<p>This map shows the city center of Cambridge, and the area around the
destination, which is marked by a small black circle (left middle). Again,
warm colours show short journey times&mdash;in this case, later
departures&mdash;but the contour lines are drawn at intervals of ten minutes,
rather than an hour, so that the innermost contour around the destination
corresponds to a start time of about ten to nine. Again, uncoloured areas are
those not served by any services; on this map these are all fields lying
outside the city itself.</p>

<p>Cambridge is a small city with a lot of bus services, so it is not very
surprising that the whole of the city center and much of the suburbs are within
twenty to thirty minutes' travel of the destination, even including waiting and
walking time. Moving further out, though, the picture changes: (selected
villages are labelled for orientation purposes)</p>

<p>
<a href="multimodal-cambridge-surrounds-1333px.png"><img src="multimodal-cambridge-surrounds-666px.png" width="666" height="500" alt="Map of Cambridge and surrounds showing times of departure to reach the West Cambridge site by 9 o'clock on a weekday morning"></a>
<br><small>&copy; Crown copyright. All rights reserved. Department&nbsp;for&nbsp;Transport&nbsp;100020237&nbsp;2006</small>
</p>

<p>The larger map clearly shows the differing level of service to various
outlying villages within 5&ndash;10km of Cambridge. Areas which are connected
to Cambridge by fast roads, such as the A14 which runs through Fenstanton and
Bar&nbsp;Hill, then skirts Cambridge to the north, and continues east via
Stow&nbsp;cum&nbsp;Quy (just south of Swaffham Bulbeck) are much better served
than villages such as Reach, which lies well off the beaten track. Waterbeach
and Great&nbsp;Shelford, to the north and south of the center of Cambridge
respectively, are also served by train services. Even on this scale there are a
few habitations with no or limited bus service and from which it is not
possible to reach the West Cambridge Site for 9 o'clock purely by public
transport without a long walk or an overnight journey (for instance, Rampton,
to the north-east of Longstanton, or Childerley, to the north-west of
Hardwick).</p>

<p>Looking at a yet larger scale shows a similar pattern:</p>

<p>
<a href="multimodal-cambridgeshire-1000px.png"><img src="multimodal-cambridgeshire-500px.png" width="500" height="578" alt="Map of Cambridgeshire and surrounds showing times of departure to reach the West Cambridge site by 9 o'clock on a weekday morning"></a>
<br><small>&copy; Crown copyright. All rights reserved. Department&nbsp;for&nbsp;Transport&nbsp;100020237&nbsp;2006</small>
</p>

<p>This map shares the same colour scheme as the previous one&mdash;warm
colours indicate short journeys, and cool colours long journeys&mdash;but the
contours are at intervals of thirty minutes rather than ten. Towns such as
Huntingdon, Newmarket and Ely are ideal commuter territory, as are some
intermediate villages; but most outlying villages aren't connected at all.</p>


<h3><a name="london"></a>London</h3>

<p>As a comparison with transport around Cambridge, we've also drawn maps for
London, a much more densely-populated area with correspondingly better
transport infrastructure (you will see that there are almost no inaccessible
grey areas). Here the chosen destination is the
Department&nbsp;for&nbsp;Transport (DfT) headquarters on Horseferry in
Westminster. Starting with the most local map:</p>

<p>
<a href="multimodal-london-10km-1000px.png"><img src="multimodal-london-10km-500px.png" width="500" height="500" alt="Map of central London showing times of departure to reach the Department for Transport building by 9 o'clock on a weekday morning"></a>
<br><small>&copy; Crown copyright. All rights reserved. Department&nbsp;for&nbsp;Transport&nbsp;100020237&nbsp;2006</small>
</p>

<p>Again, warm colours indicate short journeys and cool ones longer journeys.
On this map contours are shown at ten-minute intervals, so that the
near-circular one around the destination indicates the area in which you can
get to the DfT by leaving the house at about ten to nine in the morning.</p>

<p>Moving slightly further out, nearby tube stations
(St&nbsp;James's&nbsp;Park, Westminster and Pimlico) and bus routes to the
south and east are important. Further south there are islands of accessibility
around mainline train stations such as Brixton and Clapham Junction. On a
smaller-scale map, the tube and railway lines themselves show up as chains of
such islands:</p>

<p>
<a href="multimodal-london-20km-1196px.png"><img src="multimodal-london-20km-598px.png" width="598" height="569" alt="Map of central London and suburbs showing times of departure to reach the Department for Transport building by 9 o'clock on a weekday morning"></a>
<br><small>&copy; Crown copyright. All rights reserved. Department&nbsp;for&nbsp;Transport&nbsp;100020237&nbsp;2006</small>
</p>

<p>On this scale, particular ill-connected areas of London are clearly visible:
Hackney, Richmond and Dulwich (despite a direct train service to Victoria) both
require an eight o'clock start to arrive at the DfT for our nine o'clock
deadline. Compare these to the region of good connectivity stretching south and
south-west from the center, along the Northern Line and mainline rail line
through Wimbledon, the District line to the west, and the Docklands Light
Railway to the east. On this scale individual bus routes are not particularly
evident, even though they are significant everywhere that rail or tube stations
are too far away to walk to in the model; contrast this with the Cambridgeshire
maps above.</p>

<p>On this final map, of the whole Greater London area and surrounds, the
contour lines are at half-hour intervals:</p>

<p>
<a href="multimodal-london-big-1177px.png"><img src="multimodal-london-big-589px.png" width="589" height="608" alt="Map of Greater London and surrounds showing times of departure to reach the Department for Transport by 9 o'clock on a weekday morning"></a>
<br><small>&copy; Crown copyright. All rights reserved. Department&nbsp;for&nbsp;Transport&nbsp;100020237&nbsp;2006</small>
</p>

<p>At this scale the suburbs of London appear to be arranged along a
southwest&ndash;northeast axis, a result of good rail links to Surbiton
and Twickenham (at the ends of the two red tendrils which stretch away from the
center to lower left). Other rail lines, such as those to Bromley and Orpington
in the southeast, are also visible, as are islands of short journey time such
as Watford (northwest), Hersham and Esher (southwest); these surround individual
locations with fast (c. 1 hour) journey times into central London.</p>

<h2><a name="furtherwork"></a>What next? Further work</h2>

<p>We are considering various possible extensions and improvements, and we're
keen to talk to anyone else interested in the work so far, or any of these
ideas:</p>

<dl>
<dt style="font-weight: bold; padding-top: 0.5em;">Relating journey times to house prices</dt>
<dd>An obvious application for travel time data are to people's decisions about
where to live. By comparing journey time data for particular locations to house
prices in areas nearby it would be possible to tabulate the cheapest areas to
live in within a certain travel time of a desired location, for instance a
person's place of work.</dd>
<dt style="font-weight: bold; padding-top: 0.5em;">Improving the road travel model to better reflect comparative rail and road
journey times</dt>
<dd>At the moment our rail travel model assumes that the final stage of each
journey is by taxi, under the assumption of a uniform and isotropic road
network. This is clearly inadequate; we would like to extend it using journey
planning software (preferably including traffic and time-of-day effects) to
produce more reliable travel time and modal comparison maps.</dd>
<dt style="font-weight: bold; padding-top: 0.5em;">Cost</dt>
<dd>At the moment the maps are constructed on the assumption that users will
always choose the quickest journey under the imposed constraints. Of course in
reality users also respond to other incentives, of which one of the most
importantly is price. If we could obtain fare data we could show journey costs
rather than times, use more realistic constraints (for instance, choosing the
shortest journey cheaper than a certain amount), or comparing the prices for
tickets bought on the day to those bought at varying intervals before travel. 
<dt style="font-weight: bold; padding-top: 0.5em;">Improving the readability of the maps</dt>
<dd>The maps could be made much easier to understand. Improvements could be
made by refinement of the colours used and by replacing the current (OS
Explorer and 1:250,000) base maps with simpler ones showing sufficient
information to allow the viewer to understand the placement of the map without
extraneous detail such as building lines etc.</dd>
<dt style="font-weight: bold; padding-top: 0.5em;">Incorporating reliability information</dt>
<dd>Presently we assume that all public transport services run according to
their published timetable. This means that we are more optimistic about total
travel times than would be regular users of those services, who will know how
often services are late, cancelled or whatever. In some cases&mdash;for
instance, train services&mdash;reliability data are published, but in general
this is probably better handled by a statistical model. Both reliability and
users' tolerance for unpunctuality could be incorporated, so that users could
state the tolerance they have for late arrival at their destination (for
instance, no more than once every month) and journey times computed so as to
meet that target on average.</dd>
<dt style="font-weight: bold; padding-top: 0.5em;">A real-time web service</dt>
<dd>While our approach uses only published data and services (existing public
sector journey planners such as
<a href="http://www.transportdirect.info/TransportDirect/en/Home.aspx">TransportDirect</a>),
the maps are quite slow to construct; for instance, the one of London above
required about ten hours of computer time; further, each one is relevant only
to a particular destination or origin (and points near it). If we could speed
up this process, we could generate maps on demand for visitors to a website;
to do this we would need to work with organisations such as
Transport&nbsp;for&nbsp;London and incorporate more specific information about
services in each area, rather than relying entirely on outside services. This
is an attractive idea, although it would be expensive to build.</dd>
</dl>

<p>Please contact us (email addresses at the top of the page) if you have
any questions or comments. If you're interested in this area, please also
sign up to the (fairly low-traffic)
<a href="http://secure.mysociety.org/admin/lists/mailman/listinfo/maps">mySociety maps
mailing list</a>.</p>

<h2><a name="acknowledgments"></a>Acknowledgments</h2>

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
