<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<title>
Travel time maps: methods
</title>
</head>
<body>

<h1>Summarising public transport information with travel-time maps: Methods</h1>

<p>Chris Lightfoot, mySociety<br>&lt;<a href="mailto:chris@mysociety.org">chris@mysociety.org</a>&gt;</p>

<p>Clearly the travel-time for a particular journey is a function of the origin
and destination points, the time of travel (whether of departure or arrival),
the modes used, and of decisions made by the traveller (for instance whether to
prefer faster or cheaper journeys). Our travel-time maps can only conveniently
display a function of one point (the origin or destination point), so we need
to fix the other arguments so that (a) it describes journey times which are
useful to users in some context, and (b) it is practical to compute.</p>

<p>We evaluate the travel-time function using published the following journey
planners:</p>

<dl>
<dt><a href="http://www.travelinfosystems.com/productrail.php">RailPlanner</a></dt>
<dd>This is off-the-shelf desktop software for planning rail journeys on the national
rail network. It includes a full timetable for rail services in Great Britain.</dd>
<dt><a href="http://www.transportdirect.info/TransportDirect/en/Home.aspx">Transport Direct</a></dt>
<dd>This is a website which provides uniform access to regional journey planner
services operated by local councils and others in different parts of the
country. It will give routes by all modes of public transport and road journeys
throughout the country.</dd>
<dt><a href="http://journeyplanner.tfl.gov.uk/user/XSLT_TRIP_REQUEST2?language=en&ptOptionsActive=1">Transport for London's journey planner</a></dt>
<dd>This is a website which provides the same service as TransportDirect for the
London area.</dd>
</dl>

<p>In each case custom programs were written to drive the journey planner. For
RailPlanner, this took the form of a small Microsoft Windows program which simulates
filling of the text fields for origin, destination and departure time in the
RailPlanner application window, simulates clicking of the button to start a search,
and extracts the results using the Windows debugging API. This allows queries for
routes <em>between rail stations</em> to be computed quickly and conveniently; because
it runs on the local machine, the search is fairly fast, and a few minutes is enough to
compute the journey time from a given starting location to all other railway stations
in the country.</p>

<p>In the other two cases a conventional web "scraper" was written using the
<a href="http://search.cpan.org/~petdance/WWW-Mechanize-1.18/lib/WWW/Mechanize.pm">WWW::Mechanize</a>
perl extension. In these cases we ask for routes between <em>postcodes</em>,
rather than between named bus stops, tube stations, etc. We chose this approach
because, while there is a standard dictionary of bus stop etc. names in the
<a href="http://www.naptan.org.uk/">National Public Transport Access Node
database</a>, we were not confident that those names would be interpreted
unambiguously by the journey planner websites. By contrast, postcodes are
completely unambiguous and since most bus stops etc. are in built-up areas,
nearby postcodes can be used as placeholders for their locations; we offset
travel time by the assumed walking distance from the origin postcode to the
nearby interchange point. Admittedly this is not ideal!</p>

<p>The RailPlanner scraper is very fast: it can find the travel times from a
single station to all the other (c. 2,800) stations in Great Britain in two or
three minutes on a modest desktop PC. The web scrapers are much slower, partly
because they have to call out over the network, partly because the multimodal
route planning problem is much harder than for rail alone, and partly because
those services are of course heavily used by people for real journey planning
rather than experiments. For TransportDirect query times of tens of seconds for
individual journeys are common. We limited the rate at which we sent queries to
ensure that there was no adverse effect on the services for other users.</p>

<p>Most journeys don't start and finish at railway stations or bus stops, so
we need to be able to calculate journey times between arbitrary points; these
are used to estimate the time taken to get from an origin to join a public
transport service, and from its destination to the final destination point.</p>

<p>In the case of the railway travel-times, we did this by assuming that users
would continue from the destination station to their final destination by taxi,
taking ten minutes to change mode. Taxi journey times were assumed to be a
simple function of the distance travelled&mdash;we ignore the effects of the
road network, and of traffic. To form an estimate of this model we simulated a
large number of car journeys using off-the-shelf route-planning software, and
then fit a simple function to the journey time. For long distances we find that
the cross-country speed is about 66km/h; while that seems slow, bear in mind
that the distance in question is the <em>as-the-crow-flies</em> distance. We
assume that people will tolerate a taxi journey of up to one hour, though
obviously this is an arbitrary choice.</p>

<p>In the multimodal case, TransportDirect and the TfL journey planners will
actually compute travel-times for journeys starting and ending at arbitrary
postcodes. However, it's much more efficient to restrict our search to journeys
starting at bus stops, tube stations etc., and then to compute travel times
from arbitrary locations to the appropriate bus stop. In this case we assume
that the user will begin their journey on foot, travelling at 1m/s
cross-country; this matches the assumption made by the journey planner for the
time to (e.g.) walk between nearby bus stops. We let the journey planner site
determine the time taken for the final component of the journey (typically,
from a nearby bus stop to the fixed final destination), since there is no
disadvantage to doing so. We assume that people will tolerate a walk of up to
15 minutes at the start of their journey.</p>

<p>Therefore, in each case, we compute the maps as follows:</p>

<ul>
<li>Fix an origin and start time (in the case of the rail maps) or a
destination and arrival deadline (in the case of the multimodal maps); and
choose a region of interest; in the case of the rail maps, this was the whole
of Great Britain; in the case of the multimodal maps, a square of side 40km
centered on the destination. This latter is an arbitrary choice; we could pick
a larger area (slower to cover), or an area which doesn't contain the
destination, for instance to ask from what parts of London it is possible to
commute to somewhere outside London.</li>

<li>Iterate over all railway stations (rail maps) or over all transport
interchanges (multimodal) in the region of interest, and compute the earliest
<em>arrival</em> for a departure after the start time (rail) or the latest
<em>departure</em> for an arrival before the deadline (multimodal) and record
it.</li>

<li>Now we have enough information to draw the map. Do this by iterating over a
grid of points in the region of interest (choosing the spacing by the
resolution of the map to be drawn); at each point we search for transport
interchanges within an hour's taxi journey (rail) or 15 minutes' walking
distance (multimodal) of that point, and choose the one which gives the
shortest overall journey time, if any. Record this value.</li>
</ul>

<p>This generates a grid of points at which we know the journey time, or know
that no journey is possible. From this it is trivial to draw a map where each
point is coloured according to journey time, or uncoloured if no journey is
possible. We choose the colours according to a standard scale, but adjust the
colours using
<a href="http://www.cee.hw.ac.uk/hipr/html/histeq.html">histogram equalisation</a>
so that each colour covers approximately the same area of map.</p>

<p>Drawing the contours, which are essential to making the map comprehensible,
is slightly more subtle, because the function to contour (the travel-time) is
not actually defined everywhere in the region of interest. We fix this up by
extrapolating the values of the travel time outside the domain of the
function, contouring the extrapolated function, and then clipping the contours
agains the domain of the function. Our extrapolation is a solution to Laplace's
equation, fixing its value to the value of the travel-time on the boundary of
its domain, and fixing the normal derivative at zero on the boundary of the
region of interest. Though there is no real justification for this approach it
produces acceptable results.</p>

<p>For the national rail travel maps, the coloured fields and contours were
generated using the University&nbsp;of&nbsp;Hawaii's
<a href="http://gmt.soest.hawaii.edu/">Generic&nbsp;Mapping&nbsp;Tools</a>,
which generate PostScript output; this was then manually composited with raster
base-map data in an image-processing program. Unfortunately it is hard to
produce satisfactory results by this means, so for the other maps a custom tool
was developed to plot and contour maps into raster graphics files which were
therefore correctly aligned with the base map data. The overlays are rendered
with alpha of around 50% (adjusted by eye for contrast with the different base
maps).</p>

<h2>Software used</h2>

<dl>
<dt>custom software in C,
<a href="http://www.mingw.org/">mingw and msys</a>,
Windows 2000,
VMWare,
<a href="http://www.railplanner.co.uk/productrail.php">RailPlanner</a></dt>
<dd>For computing rail travel-times.</dd>
<dt>custom software in <a href="http://www.perl.com/">perl</a>,
<a href="http://search.cpan.org/~petdance/WWW-Mechanize-1.18/lib/WWW/Mechanize.pm">WWW::Mechanize</a></dt>
<dd>For computing multimodal travel-times.</dd>
<dt><a href="http://gmt.soest.hawaii.edu/">GMT</a>,
custom software written in C,
<a href="http://www.gimp.org/">GIMP</a></dt>
<dd>For producing maps.</dd>
</dl>

<h2>Summary of data used</h2>

<p>Excludes timetable data supplied through RailPlanner and the journey
planning websites.</p>

<dl>
<dt><a href="http://www.naptan.org.uk/">NaPTAN</a> (National Public Transport
Access Node database)</dt>
<dd>For locations of railway stations, bus stops etc.</dd>
<dt><a href="http://www.ordnancesurvey.co.uk/products/codepoint/">CodePoint</a>
(Ordnance Survey database of postcode centroid locations)</dt>
<dd>Postcodes were used to describe origin and destination points as input to
the two web scrapers, as described above.</dd>
<dt><a href="http://www.ordnancesurvey.co.uk/products/25kraster/">1:25,000
Scale Colour Raster Maps</a> (Ordnance Survey)</dt>
<dd>For use as large-scale base mapping.</dd>
<dt><a href="http://www.ordnancesurvey.co.uk/products/250kraster/">1:250,000
Scale Colour Raster Maps</a> (Ordnance Survey)</dt>
<dd>For use as small-scale base mapping.</dd>
</dl>

<p>These data were kindly supplied by agreement with the
<a href="http://www.dft.gov.uk/">Department&nbsp;for&nbsp;Transport</a>.</p>

</body>
</html>
