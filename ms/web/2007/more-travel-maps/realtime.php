<?php 

$body_id = 'moretravel';

# XXX This is hideous
ob_start();
include "../../wordpress/wp-blog-header.php";
include "../../wordpress/wp-content/themes/mysociety/header.php"; 
$header = ob_get_clean();
$header = str_replace('<title>mySociety', '<title>mySociety &raquo; Travel-time maps &raquo; Real time travel maps', $header);
header('HTTP/1.0 200 OK');
print $header;
?>

<h1>Real time travel maps</h1>

<h2><a name="introduction"></a>Introduction</h2>

<p>After seeing our travel time maps (<a href="/2006/travel-time-maps/">original
report from 2006</a>
and <a href="./">the current report</a>), the next thing that everyone asks is &ldquo;can I
have one for my journey to work?&rdquo;. We investigated in detail two ways
of providing real time versions of these maps, and we suggest a third way
which requires new data.</p>

<h2><a name="screenscraping"></a>Better screen scraping</h2>

<p>Suppose we want to create a time contour map of journey time to work by 9am
for any selected postcode in the UK.  How long this takes depends on where in
the country the map is centred. In particular, it depends on the density of bus
stops and railway stations. First, some background explanation.</p>

<h3>Basic screen scraping</h3>

<p>&ldquo;Basic screen scraping&rdquo; is the technique which we used to generate the
example travel time maps which you&rsquo;ve seen. This was done by &ldquo;screen scraping&rdquo;
the <a href="http://www.transportdirect.info/">Transport Direct</a> website.
That is, writing a computer program which operated the normal web interface of
the site to calculate journey times between lots of points and the destination
postcode.</p>

<p>The obvious thing to do would be to fetch the journey between every single
point on the final diagram and the destination postcode.  However, this would
involve far too many queries. Instead we only queried for the journey between
every public transport stop and the destination postcode. We then used our own
replication of part of the Transport Direct algorithm to calculate the journey
time from a specific point to the destination postcode. This is done by adding
the walking time to the appropriately nearest/fastest public transport stop.</p>

<p>So, we have the journey time from every point to the destination postcode.
This takes a long time to generate, as the query to the website for each
journey takes 8 seconds. For example, there are about 1,900 public transport
stops in a 20km square around Cardiff central railway station. That makes
in total about 4 hours and 15 minutes for Cardiff. From that point on, the
contour maps are fairly quick to produce.</p>

<p>This table shows the calculation time:</p>

<table border="1">
<tr><th>City</th><th>Public transport stops<br />in 20km square (approx)</th><th>Basic screen scraping<br />Generation time (estimate)</th></tr>
<tr><td>Cardiff</td><td>1900</td><td>4 hours 15 mins</td></tr>
<tr><td>Edinburgh</td><td>2700</td><td>6 hours</td></tr>
<tr><td>Birmingham</td><td>6600</td><td>14 hours 45 mins</td></tr>
<tr><td>London</td><td>10100</td><td>22 hours 30 mins</td></tr>
</table>

<h3>Parallel screen scraping</h3>

<p>The slow generation time was not a problem for making a few maps.  However,
we would very much like to be able to offer everyone who wants it their own
map. Things can be sped up a bit by running parallel screen scraping processes,
to make fuller use of the Transport Direct servers. We ran brief experiments at
3 o&rsquo;clock in the morning to measure this without affecting other users of the
service:</p>

<table border="1">
<tr><th>Number of parallel screen scrapers</th><th>Wall clock time Transport Direct takes to deal with each query(approx) </th><th>Average time between query responses from any process (approx)</th></tr>
<tr><td> 1 process  </td> <td>8 seconds</td> <td>8.00 seconds</td></tr>
<tr><td> 2 processes</td> <td>11 seconds</td> <td>5.50 seconds</td></tr>
<tr><td> 4 processes</td> <td>14 seconds</td> <td>3.50 seconds</td></tr>
<tr><td> 8 processes</td> <td>17 seconds</td> <td>2.13 seconds</td></tr>
<tr><td>16 processes</td> <td>25 seconds</td> <td>1.56 seconds</td></tr>
<tr><td>32 processes</td> <td>40 - 50 seconds</td> <td>1.40 seconds</td></tr>
<tr><td>64 processes</td> <td>110 -120 seconds</td> <td>1.79 seconds</td></tr>
</table>

<p>As you can see, if we use too few processes, we are not making full use of
the servers. If we use too many processes, we overload them, and things get
slightly slower again. The optimum is somewhere near 32 processes. Roughly,
it takes about 1.5 seconds per query. This is over 5 times quicker than using
basic screen scraping:</p>

<table border="1">
<tr><th>City</th><th>Public transport stops<br />in 20km square (approx)</th><th>Parallel screen scraping<br />Generation time (estimate)</th></tr>
<tr><td>Cardiff</td><td>1900</td><td>47 mins</td></tr>
<tr><td>Edinburgh</td><td>2700</td><td>1 hour 8 mins</td></tr>
<tr><td>Birmingham</td><td>6600</td><td>2 hours 45 mins</td></tr>
<tr><td>London</td><td>10100</td><td>4 hours 12 minutes</td></tr>
</table>

<h3>Smarter algorithm</h3>

<p>The times above are still not quick enough, even though they would fully
load the Transport Direct servers. </p>

<p>We can make our algorithm slightly smarter.  </p>

<p>It takes only slightly longer when requesting a journey to also get the
route, including which bus stops and train stations you change at, and how long
each leg of the journey takes. This will give you the destination time at
intermediate points, which you then do not have to separately query. </p>

<p>We estimate that this will speed things up again by a factor of at best 5
times, and probably about 3 times. This means Cardiff will take about 15
minutes to generate.</p>

<p>Clearly, a faster source of data is needed than the Transport Direct website.</p>

<h2><a name="railplanner"></a>Using RailPlanner</h2>

<p>One way to speed things up is to run an application on the user&rsquo;s desktop,
which has all the data available. We created such an application, based upon the
<a href="http://www.railplanner.co.uk/productrail.php">Rail Planner software</a>
for Microsoft Windows. Rail Planner can very quickly return a train journey
given start, destination and arrival or departure time.</p>

<p>Here is a screenshot of our application, which runs on top of Rail Planner.</p>

<p><a href="ttm-screenshot.png"><img src="ttm-screenshot_small.png" alt="Realtime isochrone maps" /></a>
<br /><em>Click image for bigger version.</em><br /><small>&copy; Crown copyright. All rights reserved. Department&nbsp;for&nbsp;Transport&nbsp;100020237&nbsp;2007</small></p>

<p>After you enter a postcode, it starts immediately filling in the map. It does
this by running a copy of Rail Planner separately in the background, and
programmatically querying it for journey times. As the data arrives, the
contours on the map become more complete. It takes about 10 minutes to generate
a complete map of the whole country.</p>

<p>This shows that on a computer with all the routing information for a simpler
subset (rail only), maps can be generated reasonably quickly.</p>

<h2><a name="google"></a>Interactive Google maps</h2>

<p>All of the above ideas rely on existing route finding. Much better can be
done with access to the underlying transport model. The way it calculates routes
can then be optimised.</p>

<p>For example, <a href="http://maps.google.com/">Google Maps</a> has a new
interactive feature. It lets you drag end or via points of a route in real
time. It is optimised to do this, and uses Google&rsquo;s cluster of servers, so
can calculate 10 or 15 routes per second.</p>

<p>This is maybe 20 times quicker than the above, so it could generate a map
of Cardiff in perhaps 2 minutes.</p>

<h2><a name="background"></a>Future</h2>

<p>There are two clear options for providing custom generation of transport maps.</p>

<h3>Local application</h3>

<p>Create a desktop application, such as the rail one above, only including bus
and car routes. This would require availability of the underlying time table
data. With optimisation, running on modern computers, it would be able to
generate a map in 5 or 10 minutes, with useful intermediate information much
quicker than that.</p>

<h3>Customised servers</h3>

<p>Instead of querying the existing Transport Direct site, create a special
service just for generating these maps. It would have access to the same
underlying data as Transport Direct, but use it in a more optimal manner
for the task.</p>

<p><a href="./">Main page explaining these maps</a></p>

<?php include "../../wordpress/wp-content/themes/mysociety/footer.php"; ?>

